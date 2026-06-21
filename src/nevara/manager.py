from langchain_core.documents import Document
from pathlib import Path

from nevara.components.vector_db import InMemoryDB
from nevara.utils import document_utils
from configs import get_config
import data

class BaseManager:
    def prompt_generation(self) -> str: return ''
    
class DocManager(BaseManager):
    def __init__(self):
        self.vector_store = InMemoryDB()
        self.documentHandler = document_utils.DocumentHandler()
        
        self.documents_folder = Path(data.__file__).parent / "temporary_document"
        
        self.process_document()
    
    ### internal
    def _read_tempory_folder(self) -> list[Path]:
        documents = []
        for document in self.documents_folder.glob('*'):
            if document.is_file(): documents.append(document)
            
        return documents
    
    def _list_to_str(self, obj: list[Path]):
        return '\n'.join(f"{index}) {str(x.name)}" for index, x in enumerate(obj, start=1))
    
    ### external
    def process_document(self):
        documents = self._read_tempory_folder()
        for document in documents:
            if document.suffix == '.txt': processed_document    = self.documentHandler.txtProcess  (document.absolute())
            elif document.suffix == '.pdf': processed_document  = self.documentHandler.pdfProcess  (document.absolute())
            elif document.suffix == '.docx': processed_document = self.documentHandler.docxProcess (document.absolute())
            elif document.suffix == '.ppt': processed_document  = self.documentHandler.pptProcess  (document.absolute())
            else: continue
        
            self.vector_store.push_docs(processed_document)
        
    def prompt_generation(self) -> str:
        documents = self._read_tempory_folder()
        files = self._list_to_str(documents)
        
        return f"[Tempory Retrival Files]\n{files}"
    
    ## tools
    def search_on_all_doc(self, query: str) -> list[Document]:
        """
        Retrieves contents of documents from all documents in vector store.
       
        Args:
        query: perticular topic that needed to be retrieve.
        """
        return self.vector_store.retrieve_docs(query)
        
    def search_on_doc(self, query: str, document: str) -> list[Document]:
        """
        Retrieves contents from specific document in vector store.
       
        Args:
        query: perticular topic that needed to be retrieve.
        document: name of the document.
        """
        retrieved_documents = self.vector_store.retrieve_docs(query)
        
        filtered_document = []
        for retrieved_document in retrieved_documents:
            if document == Path(retrieved_document.metadata.get('source', '')).name:
                filtered_document.append(retrieved_document)
                
        return filtered_document
    
class FSManager(BaseManager):
    def __init__(self):
        config = get_config()
        self.DEFAULT_DIR = Path(config['special_config']['working_directory'])
        self.current_dir: Path = self.DEFAULT_DIR
        
    ## internal
    def _change_dir(self, path: Path):
        self.current_dir = path
        
    def _list_dir(self, path: Path):
        files, sub_directory = [], []
        for item in path.iterdir():
            if item.is_file(): files.append(item)
            else: sub_directory.append(item)
        return files, sub_directory
    
    def _list_to_str(self, obj: list[Path]):
        return ', '.join(str(x.name) for x in obj)
    
    def _path_switch(self, path: Path):
        if not path.is_absolute() : path = self.current_dir / path
        return path
    
    ## external    
    def prompt_generation(self, path: Path | None = None):
        if path == None: path = self.current_dir
        files, sub_dir = self._list_dir(path)
        
        files_str = self._list_to_str(files)
        sub_directory_str = self._list_to_str(sub_dir)
        
        return f"[File System State]\ncurrent_dir: {path}\nfiles: {files_str}\nsub directory: {sub_directory_str}\n"
    
    ## agent tools
    def read_file(self, path: str):
        """
        Read and return the contents of a text file.
        path should contain file name.
       
        Args:
        path: Path to the file.
        """
        try:
            access_path = self._path_switch(Path(path))
            with open(access_path, 'r') as f: return f.read()
        except Exception: print(f"Problem Occured during reading: {path}")
        
    def write_file(self, path: str, content: str):
        """
        Write content into given path file.
        
        Args:
        path: Path to the file.
        content: content to be written into file.
        """
        try:
            access_path = self._path_switch(Path(path))
            with open(access_path, 'w') as f:
                f.write(content)
                return f"Successfully wrote content into {path}"
        except Exception: print(f"Problem Occured during writing: {path}")
        
    def create_file(self, path: str):
        """
        Created a empty file.
        
        Args:
        path: Path to the file.
        """
        try:
            access_path = self._path_switch(Path(path))
            access_path.touch()
            return f"Successfully created {path}"
        except Exception: print(f"Problem Occured during writing: {path}")
        
    def delete_file(self, path: str):
        """
        Deletes the file.
        
        Args:
        path: Path to the file.
        """
        try:
            access_path = self._path_switch(Path(path))
            access_path.unlink()
            return f"Succesfully removed {path}"        
        except Exception: print(f"Problem Occured during writing: {path}")
        
    def create_directory(self, path: str):
        """
        creates the directory in given path.
        
        Args:
        path: Path to the directory.
        """
        try: 
            access_path = self._path_switch(Path(path))
            access_path.mkdir(parents=True, exist_ok=True)
            return f"Succesfully created {path} directory"  
        except Exception: print(f"Problem Occured during writing: {path}")
    
    def delete_directory(self, path: str):
        """
        Deletes the directory in given path.
        
        Args:
        path: Path to the directory.
        """
        try: 
            access_path = self._path_switch(Path(path))
            access_path.rmdir()
            return f"Succesfully removed {path} directory"  
        except Exception: print(f"Problem Occured during writing: {path}")
        
    def change_directory(self, path: str):
        """
        change the current working directory.
        
        Args:
        path: Path to the directory.
        """
        try:
            self.current_dir = self._path_switch(Path(path))
            return f"Succesfully changed current directory to {path}"  
        except Exception: print(f"Problem Occured during writing: {path}")
        
    def list_directory(self, path: str):
        """
        lists files and directory from provided path.
        
        Args:
        path: Path to the directory.
        """
        try:
            access_path = self._path_switch(Path(path))
            return self.prompt_generation(access_path)
        except Exception: print(f"Problem Occured during listing directory: {path}")
        
        
### defination
fs_manager = FSManager()
doc_manager = DocManager()
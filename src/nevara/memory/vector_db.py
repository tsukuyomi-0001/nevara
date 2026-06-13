from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from pathlib import Path
import faiss

from nevara.agent.LM import EmbeddingModel
from nevara.modules.util import datetime_formater

class BaseVectorDB:
    def __init__(self, path_to_db, db_name):
        self.db_path = Path(path_to_db) / db_name
        self.embedding_dimension = EmbeddingModel.dimensions if EmbeddingModel.dimensions else len(EmbeddingModel.embed_query("H"))
        
    def _create_db(self):
        self.index = faiss.IndexFlatL2(self.embedding_dimension)
        
        self.vectorStore = FAISS(
            index = self.index,
            embedding_function=EmbeddingModel,
            docstore=InMemoryDocstore(),
            index_to_docstore_id={}
        )
    
    def save_db(self):
        self.vectorStore.save_local(str(self.db_path))
    
    def load_db(self):
        if not self.db_path.exists(): return self._create_db()
        
        self.vectorStore = FAISS.load_local(
            str(self.db_path),
            EmbeddingModel,
            allow_dangerous_deserialization=True
        )

class HistoryDB(BaseVectorDB):
    def __init__(self, path_to_db, db_name):
        super().__init__(path_to_db, db_name)
        self.load_db()
        
    def push_docs(self, documents: list[str]):
        self.load_db()
        self.vectorStore.add_documents([Document(page_content=document) for document in documents])
        self.save_db()
        
    def push_stamp_docs(self, document: list[str] | str):
        if isinstance(document, str): document = [document]
        stamped_doc = datetime_formater(document)
        self.push_docs(stamped_doc)
        return stamped_doc
    
    def retrieve_doc(self, query: str):
        retriever = self.vectorStore.as_retriever()
        docs = retriever.invoke(query)
        return docs
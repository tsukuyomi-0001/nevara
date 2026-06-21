### class for doc management tool and state, reading docx like txt, pdf, docx, ppt, save with vecDB.
from langchain_community.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader, UnstructuredPowerPointLoader
from langchain_core.documents import Document
from pathlib import Path

class DocumentHandler:
    def txtProcess (self, path: Path) -> list[Document]: 
        return TextLoader(path).load()
    def pdfProcess (self, path: Path) -> list[Document]:
        return PyPDFLoader(path).load()
    def docxProcess(self, path: Path) -> list[Document]:
        return Docx2txtLoader(path).load()
    def pptProcess (self, path: Path) -> list[Document]:
        return UnstructuredPowerPointLoader(path).load()
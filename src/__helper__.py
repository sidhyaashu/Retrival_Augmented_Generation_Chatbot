from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from transformers import AutoTokenizer, AutoModel



model_name = "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

#Function for load pdf
def pdf_loader(data):
    try:
        loader =DirectoryLoader(data,glob="*.pdf",loader_cls=PyPDFLoader)
        document = loader.load()

        return document
    except Exception as e:
        print(f"An error occurred while loading the PDF(s): {e}")
        return None
    

extracted_data = pdf_loader("../data")


#To create chunks of each tex
def text_split(data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 120, chunk_overlap = 20)
    text_chunks = text_splitter.split_documents(data)
    return text_chunks



def download_hugging_face_embeddings():
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    return embeddings
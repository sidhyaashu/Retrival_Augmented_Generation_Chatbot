from src.helper import pdf_loader, text_split, download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore 
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
import os

load_dotenv()


PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')


extracted_data = pdf_loader("./data/nmd.pdf")
text_chunks = text_split(extracted_data)
embeddings = download_hugging_face_embeddings()



pinecone_api_key = os.environ.get('PINECONE_API_KEY')
pc = Pinecone(api_key=pinecone_api_key) 

index_name = "college-project"
DIMENTION = 384


if index_name not in pc.list_indexes().names():
    try:
        pc.create_index(
            name=index_name,
            dimension=DIMENTION,
            metric="cosine",
            spec=ServerlessSpec(
                cloud='aws', 
                region='us-east-1'
            ) 
        )
        while not pc.describe_index(index_name).status['ready']:
            time.sleep(1)
        print("Index created successfully.")
    except pc.exceptions.ForbiddenException as e:
        print("Forbidden: Check your API key and permissions.")
    except pc.exceptions.AlreadyExistsException as e:
        print("Index already exists.")
    except Exception as e:
        print(f"An error occurred while creating the index: {e}")

else:
    print("Index already exists.")  


# wait for index to be initialized  
while not pc.describe_index(index_name).status['ready']:
    time.sleep(1)


# connect to index
index = pc.Index(index_name)
time.sleep(1)
index.describe_index_stats()  

namespace = "wondervector5000"


docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks,
    index_name=index_name,
    embedding=embeddings, 
    namespace=namespace 
)

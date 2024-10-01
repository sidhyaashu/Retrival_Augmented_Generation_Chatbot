from src.helper import download_hugging_face_embeddings
from src.prompt import prompt_template
from langchain_pinecone import PineconeVectorStore 
from pinecone import Pinecone, ServerlessSpec
from flask import Flask, render_template,jsonify,request

from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers
from langchain_pinecone import PineconeVectorStore 
from langchain.chains import RetrievalQA
from langchain.llms import CTransformers

import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')

pinecone_api_key = os.environ.get('PINECONE_API_KEY')
pc = Pinecone(api_key=pinecone_api_key) 

index_name = "college-project"
DIMENTION = 384


embedding = download_hugging_face_embeddings()


vectorstore = PineconeVectorStore.from_existing_index(index_name,embedding)

PROMPT=PromptTemplate(template=prompt_template, input_variables=["context", "question"])

chain_type_kwargs={"prompt": PROMPT}

llm=CTransformers(model="./model/llama-2-7b-chat.ggmlv3.q4_0.bin",
                  model_type="llama",
                  config={'max_new_tokens':512,
                          'temperature':0.8})

qa = RetrievalQA.from_chain_type(  
    llm=llm,  
    chain_type="stuff",  
    retriever=vectorstore.as_retriever()  
)  


@app.route("/")
def index():
    return render_template('./templates/chat.html')



if __name__ == '__main__':
    app.run(debug=True)
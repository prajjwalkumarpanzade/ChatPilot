from django.shortcuts import render
from django.http import JsonResponse
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain.chains.query_constructor.base import AttributeInfo
from qdrant_client import QdrantClient
import json
from django.conf import settings
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.files import File
from fastembed import TextEmbedding

def process_pdf(request):
  decoded = (request.body).decode('utf-8')
  data = json.loads(decoded)
  
  pdf_loader = PyPDFLoader(data['file_url'])
  documents = pdf_loader.load()
  #Split document into chungs
  text_splitter =  CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
  docs = text_splitter.split_documents(documents)
  # #Create Embeddings 
  embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
  qdrant = Qdrant.from_documents(
        docs,
        embeddings,
        url=settings.QDRANT_URL,
        prefer_grpc=True,
        api_key=settings.QDRANT_API_KEY,
        collection_name="my_documents",
    )
  return JsonResponse({'Message':'ok'})


def search_query(request):
    qdrant_client = QdrantClient(url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY)
    query = request.GET.get('query')
    embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
    query_v = embeddings.embed_query(str(query))  
    search_result = qdrant_client.search(collection_name="my_documents", query_vector=query_v, limit=1)
    serialized_results = []
    print(search_result)
    serialized_results = []
    for result in search_result:
        result_dict = {
            'score': result.score,
            'payload': result.payload
        }
        serialized_results.append(result_dict)
    
    
    return JsonResponse({"res": serialized_results})

  
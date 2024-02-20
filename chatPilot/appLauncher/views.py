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
  uploaded_pdf = request.FILES.get('pdf_file')
  file_path = default_storage.save('temp_file.pdf',ContentFile(uploaded_pdf.read()))
  #Load PDF
  pdf_loader = PyPDFLoader(file_path)
  documents = pdf_loader.load()
  #Split document into chungs
  text_splitter =  CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
  docs = text_splitter.split_documents(documents)
  #Create Embeddings 
  embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
  qdrant = Qdrant.from_documents(
        docs,
        embeddings,
        url=settings.QDRANT_URL,
        prefer_grpc=True,
        api_key=settings.QDRANT_API_KEY,
        collection_name="my_documents",
    )
  
  query = "What Are IDEs and Code Editors?"
  found_docs = qdrant.similarity_search(query)


  os.remove(file_path)
  # return JsonResponse({'found_docs': found_docs[0].page_content})
  return JsonResponse({'found_docs'},qdrant)


def search_query(request):
    # Initialize the Qdrant client with your URL and API key
    qdrant_client = QdrantClient(url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY)
    data = json.loads(request.body)
    query :str = data.get('query')
    embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
    query_v = embeddings.embed_query(query)  
    search_result = qdrant_client.search(collection_name="my_documents", query_vector=query_v)
    return JsonResponse({"Results": search_result[0].payload['page_content']})

  
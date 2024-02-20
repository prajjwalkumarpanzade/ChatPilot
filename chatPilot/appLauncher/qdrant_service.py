from qdrant_client import QdrantClient

class QdrantService:
    def __init__(self, url, api_key, collection_name=None):
        self.client = QdrantClient(url, api_key)
        self.collection_name = collection_name
        

    def search(self, query):
        if self.collection_name is None:
            raise ValueError("Collection name is not specified")
        return self.client.search(collection=self.collection_name, query=query)

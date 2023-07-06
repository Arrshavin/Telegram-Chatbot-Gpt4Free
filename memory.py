import chromadb

class Memory:
    def __init__(self, name):
        self.name = name
        self.client = chromadb.Client(chromadb.Settings(chroma_db_impl="duckdb+parquet", persist_directory="./persist"))
        try:
            self.collection = self.client.create_collection(name)
        except ValueError:
            self.collection = self.client.get_collection(name)

    def insert(self, data, uuid):
        self.collection.insert_one({"_id": uuid, **data})
    
    def find(self, query):
        return self.collection.query(query_texts=[query], n_results=2)['documents']
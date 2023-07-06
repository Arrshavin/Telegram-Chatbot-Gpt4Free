from chromadb import Client, Settings

class Memory:
    client = Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="./persist"))
    def __init__(self, name):
        self.name = name
        try:
            self.collection = self.client.create_collection(name)
        except ValueError:
            self.collection = self.client.get_collection(name)
    def insert(self, data, uuid):
        try:
            self.collection.add(documents=[data], ids=[uuid])
        except Exception as e:
            print(f"Error inserting data: {e}")
    def find(self, query):
        try:
            q = self.collection.query(query_texts=[query], n_results=2)
            return q['documents']
        except Exception as e:
            print(f"Error finding data: {e}")
            return []
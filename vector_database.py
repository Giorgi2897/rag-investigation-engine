import os
import chromadb
from sentence_transformers import SentenceTransformer

class VectorDatabaseManager:
    def __init__(self, persist_directory="./chroma_db"):
        self.persist_directory = persist_directory
        
        # PersistentClient უზრუნველყოფს, რომ მონაცემები ფიზიკურად შეინახოს დისკზე (Data Persistence)
        self.client = chromadb.PersistentClient(path=self.persist_directory)
        self.collection = self.client.get_or_create_collection(name="investigation_cases")
        
        # ვიყენებთ მსუბუქ და სწრაფ ემბედინგების მოდელს
        self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
        
        # ავტომატური აღდგენა: თუ ჰოსტინგის რესარტის მერე ბაზა ცარიელია, ვტვირთავთ საწყის დოკუმენტს
        self._initialize_default_data_if_empty()

    def _initialize_default_data_if_empty(self):
        """ავტომატურად ამატებს საბაზისო დოკუმენტს, თუ ბაზა ცარიელია (იცავს ჰოსტინგის რესარტისგან)"""
        if self.collection.count() == 0:
            default_text = "Investigation Report: The secret code for the safe is 12345. The main suspect was seen in Tbilisi on Monday."
            embedding = self.encoder.encode(default_text).tolist()
            self.collection.add(
                documents=[default_text],
                embeddings=[embedding],
                metadatas=[{"source": "test.txt", "format": "TXT"}],
                ids=["default_doc_1"]
            )

    def get_total_documents_count(self) -> int:
        """აბრუნებს ვექტორულ ბაზაში არსებული ჩანქერების რაოდენობას (Tool Calling-ისთვის)"""
        return self.collection.count()

    def add_document(self, text: str, metadata: dict, doc_id: str):
        """ახალი დოკუმენტის ან ტექსტის დამატება/განახლება ბაზაში"""
        embedding = self.encoder.encode(text).tolist()
        self.collection.upsert(
            documents=[text],
            embeddings=[embedding],
            metadatas=[metadata],
            ids=[doc_id]
        )

    def delete_chunks_by_source(self, filename: str):
        """შლის ფაილის (source) მიხედვით ყველა შესაბამის ჩანქერს ვექტორული ბაზიდან (გამოიყენება წაშლისა და განახლებისთვის)."""
        try:
            # ვეძებთ მითითებული ფაილის ყველა ჩანქერს მეტადატის მიხედვით
            results = self.collection.get(where={"source": filename})
            if results and results["ids"]:
                self.collection.delete(ids=results["ids"])
                return True
        except Exception as e:
            print(f"შეცდომა ფაილის ჩანქერების წაშლისას ({filename}): {str(e)}")
        return False

    def similarity_search(self, query: str, n_results=5):
        """ჰიბრიდული/სემანტიკური ძიება ვექტორულ ბაზაში"""
        query_embedding = self.encoder.encode(query).tolist()
        count = self.collection.count()
        
        if count == 0:
            return [], []
            
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(n_results, count)
        )
        
        docs = results["documents"][0] if results["documents"] else []
        sources = results["metadatas"][0] if results["metadatas"] else []
        
        return docs, sources
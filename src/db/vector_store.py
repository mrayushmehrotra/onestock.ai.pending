import chromadb
from chromadb.config import Settings
import os
from typing import List, Dict, Any

class VectorStore:
    def __init__(self, db_path: str = "./data/chroma_db"):
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(name="market_news")

    def add_news(self, news_items: List[Dict[str, Any]]):
        """
        Adds news articles to the vector store for RAG.
        """
        ids = [item['url'] for item in news_items]
        documents = [f"{item['title']}. {item.get('summary', '')}" for item in news_items]
        metadatas = [{
            "source": item['source'],
            "scraped_at": item['scraped_at'],
            "tickers": ",".join(item.get('tickers', []))
        } for item in news_items]

        self.collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )

    def search_news(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Searches news based on semantic similarity.
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results

if __name__ == "__main__":
    store = VectorStore()
    # store.add_news([{"url": "test1", "title": "Reliance gains", "source": "ET", "scraped_at": "now"}])
    # print(store.search_news("Reliance"))

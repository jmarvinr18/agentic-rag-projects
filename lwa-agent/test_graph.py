# test_retriever.py
from app.embeddings.local.faiss import get_retriever

retriever = get_retriever()
docs = retriever.invoke("Donato Zarate")
print(f"Found {len(docs)} documents:")
for doc in docs:
    print(f"  - {doc.page_content[:100]}...")

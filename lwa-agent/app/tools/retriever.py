from langchain_core.tools.retriever import create_retriever_tool
from app.embeddings.local.faiss import get_retriever

def retriever_tool():

    """
    Retrieve from the vector store.
    Use this to look up information from the Langchain blog.
    """

    retriever_tool_langchain=create_retriever_tool(
        get_retriever(),
        "retriever_vector_langchain_blog",
        "Search and run information about Langchain"
    )

    # print(f"RETRIEVER TOOL RESPONSE: {retriever_tool_langchain}")

    return retriever_tool_langchain
from assistant_rag.indexing.documents import load_documents
from assistant_rag.indexing.storage import get_storage_context
from assistant_rag.indexing.embeddings import get_embed_model

from llama_index.core import VectorStoreIndex
from llama_index.core import Settings


def build_index():
    docs = load_documents()
    storage_context = get_storage_context()
    embed_model = get_embed_model()

    Settings.embed_model = embed_model

    for doc in docs:
        VectorStoreIndex.from_documents(
            [doc],
            storage_context=storage_context,
            show_progress=True,
        )

if __name__ == "__main__":
    build_index()

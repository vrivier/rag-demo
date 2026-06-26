import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import VectorStoreIndex
from assistant_rag.rag.config import get_args

def get_index():
    args = get_args()

    # Connecter au client ChromaDB existant
    chroma_client = chromadb.PersistentClient(path=args.database_location)
    chroma_collection = chroma_client.get_collection(args.collection_name)

    # Créer le vector store
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

    # Charger l'index sans re-indexer
    index = VectorStoreIndex.from_vector_store(vector_store)

    return index

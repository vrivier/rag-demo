import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from assistant_rag.indexing.config import get_args

def get_storage_context():
    args = get_args()
    chroma_client = chromadb.PersistentClient(path=args.database_location)
    chroma_collection = chroma_client.create_collection(args.collection_name)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    return storage_context

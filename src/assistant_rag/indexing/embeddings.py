from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from assistant_rag.indexing.config import get_args

def get_embed_model():
    args = get_args()
    return HuggingFaceEmbedding(
      model_name="BAAI/bge-small-en-v1.5",
      cache_folder=args.embeddings_cache_folder,
      device="cuda",
    )
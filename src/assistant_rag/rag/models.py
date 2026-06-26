from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from assistant_rag.rag.config import get_args

def define_models():
    args = get_args()

    Settings.llm = Ollama(
        model="qwen3:4b",
        request_timeout=120.0,
        context_window=4096,
    )

    Settings.embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-small-en-v1.5",
        cache_folder=args.embeddings_cache_folder,
        device="cuda",
    )

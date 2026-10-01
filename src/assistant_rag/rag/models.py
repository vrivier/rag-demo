from llama_index.core import Settings
from dotenv import load_dotenv
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from assistant_rag.rag.config import get_args

def define_models():
    args = get_args()

    # Reads OPENAI_API_KEY from the environment or from a local .env file.
    load_dotenv()

    Settings.llm = OpenAI(
        model=args.llm_model,
        temperature=0.1,
        timeout=120.0,
    )

    Settings.embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-small-en-v1.5",
        cache_folder=args.embeddings_cache_folder,
        device="cuda",
    )

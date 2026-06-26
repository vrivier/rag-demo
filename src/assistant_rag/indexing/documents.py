from llama_index.core import SimpleDirectoryReader
from llama_index.readers.file import PyMuPDFReader
from assistant_rag.indexing.config import get_args

def load_documents():
    args = get_args()
    return SimpleDirectoryReader(
        input_dir=args.pdf_documents_folder,
        file_extractor={".pdf": PyMuPDFReader()}
    ).load_data()
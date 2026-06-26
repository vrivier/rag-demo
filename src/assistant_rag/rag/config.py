import argparse

_args = None

def get_args():
    global _args
    if _args is None:
        _args = _parse()
    return _args


def _parse():
    parser = argparse.ArgumentParser(
        description="Start chat with HR RAG system.",
        fromfile_prefix_chars="@",
    )

    parser.add_argument( 
        "database_location", 
        help="Vector index location.", 
    )
    parser.add_argument(
        "collection_name", 
        help="Name of the collection to request.", 
    )
    parser.add_argument(
        "-e", "--embeddings_cache_folder", 
        help="Embedding model cache folder, which might be needed for model loading.", 
        default=None,
    )

    _args = parser.parse_args()

    return _args

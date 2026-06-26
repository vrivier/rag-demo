import argparse
import sys
from pathlib import Path

_args = None

def get_args():
    global _args
    if _args is None:
        _args = _parse()
        _validate(_args)
    return _args


def _parse():
    parser = argparse.ArgumentParser(
        description="Build a vector index database from a pdf documents folder.",
        fromfile_prefix_chars="@",
    )

    parser.add_argument( 
        "pdf_documents_folder", 
        help="Path of the folder containing pdfs to vectorize.", 
        type=Path
    )
    parser.add_argument( 
        "database_location", 
        help="Path where the database will be written.", 
    )
    parser.add_argument(
        "collection_name", 
        help="How to name the collection within the database.", 
    )
    parser.add_argument(
        "-e", "--embeddings_cache_folder", 
        help="Embedding model cache folder, which might be needed for model loading.", 
        default=None,
    )

    _args = parser.parse_args()

    return _args


def _validate(args):
    errors = []

    if not args.pdf_documents_folder.exists():
        errors.append(f"pdf_documents_folder introuvable : {args.pdf_documents_folder}")

    if not args.pdf_documents_folder.is_dir():
        errors.append(f"pdf_documents_folder n'est pas un dossier : {args.pdf_documents_folder}")

    if errors:
        for e in errors:
            print(f"Erreur : {e}", file=sys.stderr)
        sys.exit(1)

from assistant_rag.rag.models import define_models
from assistant_rag.rag.index import get_index
from assistant_rag.rag.system_prompt import get_system_prompt


def get_query_engine():
    define_models()
    index = get_index()
    system_prompt = get_system_prompt()
    query_engine = index.as_query_engine(text_qa_template=system_prompt)
    return query_engine

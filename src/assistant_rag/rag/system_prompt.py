from llama_index.core.prompts import RichPromptTemplate

def get_system_prompt():

    system_prompt = """
    {% chat role='system' %}
    Tu réponds toujours en français.
    {% endchat %}
    {% chat role='user' %}
    Contexte : {{ context_str }}
    Question : {{ query_str }}
    {% endchat %}
    """
    qa_template = RichPromptTemplate(system_prompt)
    return qa_template

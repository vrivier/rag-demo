from assistant_rag.rag.engine import get_query_engine

def chat(query_engine):
    # interagit avec l'utilisateur
    # calcule une réponse à partir de la question de l'utilisateur
    # affiche la réponse et les sources de la réponse

    print("Bonjour, comment puis-je vous aider ?")
    user_query = input()
    while user_query != "non":

        response = query_engine.query(user_query)
        print(response)
        print("Sources :")
        for node in response.source_nodes:
            print(
                "Document", node.metadata['file_name'], 
                ", page", node.metadata['source'],
            )

        print("D'autres questions ?")
        user_query = input()

    print("A bientôt !")

if __name__ == "__main__":
    query_engine = get_query_engine()
    chat(query_engine)

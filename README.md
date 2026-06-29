#### Description :

MVP d'assistant RAG RH permettant aux salariés d'une entreprise d'accéder facilement aux politiques RH de leur entreprise. 

#### Impact métier visé : 
Allègement de la charge de travail RH de réponse aux questions du personnel de l'entreprise.  
Meilleure expérience collaborateur avec disponibilité et facilité d'accès à l'information RH. 

#### Structure du dépôt :  

assistant-rag-rh/  
├── chroma_db/&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ← index vectoriel (données générées)  
├── data/&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;← PDFs source  
├── scripts/&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;← scripts ponctuels  
├── src/  
│&nbsp;&nbsp;&nbsp;└── assistant_rag/  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── indexing/ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;← création d'index  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── rag/&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ← logique de conversation  
└── pyproject.toml

#### Architecture système :

PDF  
 ↓  
Chunking  
 ↓  
Embeddings BGE-small  
 ↓  
ChromaDB  
 ↓  
Retriever  
 ↓  
Qwen3 4B  
 ↓  
Réponse + citations

#### Détail : 

OCR PyMuPDF  
Chunking : 1024 tokens, 20 tokens overlap  
Modèle d'embeddings : bge-small-en-v1.5  
LLM : qwen 3 4b  
top k = 2  
Prompt système : réponse en français

#### Stack : 

llama-index, Ollama

#### Données : 

6 documents RH générés avec Claude

#### Installation : 

installation Ollama (https://ollama.com) 
```bash
git clone https://github.com/vrivier/rag-demo   
ollama pull qwen3:4b  
cd assistant-rag-rh  
pip install -r requirements.txt
```

#### Construction d'index :  
```bash
python src\assistant_rag\indexing\build_index.py <chemin_dossier_pdfs> <chemin_ecriture_base_vectorielle> <nom_collection> <option[-e]: chemin_cache_embeddings>
```
#### Discussion avec l'assistant :  
```bash
python src\assistant_rag\rag\chat.py <base_vectorielle> <nom_collection> <option[-e]: chemin_cache_embeddings>
```

#### Exemples :

<img width="1023" height="256" alt="Capture d&#39;écran 2026-06-29 102545" src="https://github.com/user-attachments/assets/046aed13-203a-49d4-916e-cb2ed3e9eb0c" />
<img width="924" height="425" alt="Capture d&#39;écran 2026-06-29 102557" src="https://github.com/user-attachments/assets/62c057f1-0a2d-4e78-96f7-a95f5adcecfa" />

#### Configuration requise : 
GPU, 5Gb d'espace disque pour le LLM

#### RAG local :
Pas de coûts, confidentialité des données

#### Pistes d'amélioration : 
Interface streamlit  
Gestion des requêtes hors scope documentation  
Seuil de similarité pour le retrieval  
Jeu de données d'évaluation du système  
Agrandissement de la documentation / diminution des chunks (challenge retrieval)  
Reranking  
Conteneurisation Docker  
Interface FastAPI  
Déploiement  


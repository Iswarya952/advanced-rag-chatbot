# 🤖 Advanced Multi-PDF RAG Chatbot

Advanced Retrieval-Augmented Generation (RAG) chatbot capable of answering questions from multiple uploaded PDFs using semantic retrieval and LLM-based generation with source citations.

---

## 🚀 Features

✅ Multi-PDF Upload Support  
✅ Semantic Search using Embeddings  
✅ ChromaDB Vector Storage  
✅ Source Citations  
✅ Persistent Database Support  
✅ Response Caching  
✅ Modular Architecture  
✅ Streamlit UI  
✅ Gemini Integration  
✅ Low Coupling & High Cohesion Design  

---

# 🏗 System Architecture

```mermaid
flowchart TD

A[PDF Upload] --> B[PDF Loader]

B --> C[Text Splitter]

C --> D[Embedding Model]

D --> E[Chroma Vector DB]

E --> F[Retriever]

F --> G[Context Builder]

G --> H[Prompt Generator]

H --> I[Gemini LLM]

I --> J[Response Generation]

J --> K[Source Citation Layer]

K --> L[Streamlit UI]
```

---

# 🔄 RAG Pipeline (Steel Thread Approach)

```mermaid
flowchart LR

A[Rewrite]

--> B[Retrieve]

--> C[Rerank]

--> D[Refine]

--> E[Insert]

--> F[Generate]
```

---

# 📦 Project Structure

```text
advanced-rag-chatbot/

│── app.py

│── requirements.txt

│── README.md

│── .gitignore

│── database/

│   └── chat_history.db

│

│── utils/

│   ├── pdf_loader.py

│   ├── text_splitter.py

│   ├── embeddings.py

│   ├── vectordb.py

│   ├── retriever.py

│   ├── prompt.py

│   ├── llm.py

│   ├── citations.py

│   ├── database.py

│   └── cache_manager.py
```

---

# 🧩 UML Component Diagram

```mermaid
classDiagram

class PDFLoader

class TextSplitter

class EmbeddingModel

class VectorDB

class Retriever

class PromptBuilder

class LLM

class CitationManager

class CacheManager

PDFLoader --> TextSplitter

TextSplitter --> EmbeddingModel

EmbeddingModel --> VectorDB

VectorDB --> Retriever

Retriever --> PromptBuilder

PromptBuilder --> LLM

LLM --> CitationManager

LLM --> CacheManager
```

---

# ⚙ Design Principles

## SOLID Principles

- Single Responsibility Principle
- Open / Closed Principle
- Dependency Separation
- Modular Design
- Low Coupling
- High Cohesion

---

# 🛠 Tech Stack

Python

Streamlit

LangChain

Gemini

ChromaDB

FAISS (optional)

SQLite

---

# ▶ Run Locally

```bash
git clone https://github.com/Iswarya952/advanced-rag-chatbot.git

cd advanced-rag-chatbot

pip install -r requirements.txt

streamlit run app.py
```

---

# 📈 Future Enhancements

- Hybrid Retrieval
- Reranking Layer
- Multi Agent Pipeline
- Graph RAG
- Context Compression
- Abstraction Layer Design
- Persistent Shared Repository
- UML Expansion

---

## 👩‍💻 Author

Iswarya

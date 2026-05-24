import streamlit as st
import os
import time
import glob
import shutil

from utils.pdf_loader import load_pdfs
from utils.text_splitter import split_documents
from utils.embeddings import load_embedding_model
from utils.vectordb import create_vectorstore
from utils.retriever import get_retriever
from utils.prompt import SYSTEM_PROMPT
from utils.llm import load_llm
from utils.database import save_chat, get_history
from utils.cache_manager import (
    get_cached_response,
    save_to_cache
)
from utils.citations import format_sources


# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="Advanced RAG Chatbot",
    page_icon="🤖",
    layout="wide"
)

st.title(
    "🤖 Advanced Multi-PDF RAG Chatbot"
)

st.caption(
    "🚀 Multi-PDF RAG Chatbot with Source Citations"
)


# -----------------------------------
# SESSION STATE
# -----------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "retriever" not in st.session_state:
    st.session_state.retriever = None

if "llm" not in st.session_state:
    st.session_state.llm = None

if "current_pdf" not in st.session_state:
    st.session_state.current_pdf = ""


# -----------------------------------
# SIDEBAR
# -----------------------------------

with st.sidebar:

    st.header("📂 Upload PDFs")

    uploaded_files = st.file_uploader(
        "Upload Multiple PDFs",
        type=["pdf"],
        accept_multiple_files=True
    )

    st.divider()

    if st.button("🗑 Clear Chat"):

        st.session_state.messages = []
        st.session_state.retriever = None
        st.session_state.current_pdf = ""

        st.rerun()

    st.divider()

    st.subheader("📜 Previous Chats")

    history = get_history()

    for chat in history[-5:]:

        st.write(
            f"Q: {chat[1]}"
        )


# -----------------------------------
# DOCUMENT PROCESSING
# -----------------------------------

def process_documents(
    pdf_paths
):

    docs = load_pdfs(
        pdf_paths
    )

    st.write(
        "Documents Loaded:",
        len(docs)
    )

    chunks = split_documents(
        docs
    )

    st.write(
        "Chunks Created:",
        len(chunks)
    )

    if len(chunks) == 0:

        st.error(
            "❌ No text extracted"
        )

        st.stop()

    embeddings = (
        load_embedding_model()
    )

    st.write(
        "Embeddings loaded"
    )

    vectorstore = (
        create_vectorstore(
            chunks,
            embeddings
        )
    )

    st.write(
        "Vector DB created"
    )

    retriever = (
        get_retriever(
            vectorstore
        )
    )

    return retriever


# -----------------------------------
# PDF PROCESSING
# -----------------------------------

if uploaded_files:

    st.session_state.retriever = None
    st.session_state.current_pdf = ""

    os.makedirs(
        "data/uploaded_pdfs",
        exist_ok=True
    )

    # delete old PDFs

    for old in glob.glob(
        "data/uploaded_pdfs/*"
    ):

        os.remove(old)

    # delete old vector db

    if os.path.exists(
        "vectorstore"
    ):

        shutil.rmtree(
            "vectorstore",
            ignore_errors=True
        )

    pdf_paths = []

    for file in uploaded_files:

        path = (
            f"data/uploaded_pdfs/"
            f"{file.name}"
        )

        with open(
            path,
            "wb"
        ) as f:

            f.write(
                file.read()
            )

        pdf_paths.append(
            path
        )

    with st.spinner(
        "📚 Processing PDFs..."
    ):

        retriever = (
            process_documents(
                pdf_paths
            )
        )

        llm = load_llm()

        st.session_state.retriever = (
            retriever
        )

        st.session_state.llm = (
            llm
        )

        st.session_state.current_pdf = (
            str(pdf_paths)
        )

    st.success(
        "✅ PDFs processed successfully!"
    )


# -----------------------------------
# DISPLAY CHAT
# -----------------------------------

for msg in st.session_state.messages:

    with st.chat_message(
        msg["role"]
    ):

        st.markdown(
            msg["content"]
        )


# -----------------------------------
# CHAT INPUT
# -----------------------------------

query = st.chat_input(
    "Ask questions from uploaded PDFs..."
)


# -----------------------------------
# QUERY PROCESSING
# -----------------------------------

if query:

    retriever = (
        st.session_state.retriever
    )

    llm = (
        st.session_state.llm
    )

    if retriever is None:

        st.warning(
            "⚠ Upload PDF first"
        )

    else:

        with st.chat_message(
            "user"
        ):

            st.markdown(
                query
            )

        with st.chat_message(
            "assistant"
        ):

            with st.spinner(
                "🤖 Thinking..."
            ):

                start = time.time()

                cache_key = (

                    query

                    + "_"

                    + st.session_state.current_pdf

                )

                cached = (
                    get_cached_response(
                        cache_key
                    )
                )

                retrieved_docs = (
                    retriever.invoke(
                        query
                    )
                )

                if cached:

                    answer = cached

                else:

                    context = "\n\n".join([

f"""
Page:
{doc.metadata.get('page',0)+1}

Content:
{doc.page_content}
"""

for doc in retrieved_docs

])

                    final_prompt = f"""

{SYSTEM_PROMPT}

Context:
{context}

Question:
{query}

"""

                    response = (
                        llm.invoke(
                            final_prompt
                        )
                    )

                    answer = (
                        response.content
                    )

                    save_to_cache(
                        cache_key,
                        answer
                    )

                sources = (
                    format_sources(
                        retrieved_docs
                    )
                )

                source_text = "\n".join(
                    sources
                )

                final_answer = f"""

{answer}

---

### 📚 Sources

{source_text}

"""

                st.markdown(
                    final_answer
                )

                end = time.time()

                st.caption(
f"⏱ Response generated in {round(end-start,2)} seconds"
                )

        st.session_state.messages.append(
            {
                "role":"user",
                "content":query
            }
        )

        st.session_state.messages.append(
            {
                "role":"assistant",
                "content":final_answer
            }
        )

        save_chat(
            query,
            final_answer
        )
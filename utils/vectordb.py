import os
import shutil

from langchain_chroma import Chroma


def create_vectorstore(
    chunks,
    embeddings
):

    if os.path.exists(
        "vectorstore"
    ):

        shutil.rmtree(
            "vectorstore",
            ignore_errors=True
        )

    vectorstore = (
        Chroma.from_documents(

            documents=chunks,

            embedding=embeddings,

            persist_directory=
            "vectorstore"

        )
    )

    return vectorstore
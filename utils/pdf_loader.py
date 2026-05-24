from langchain_community.document_loaders import PyPDFLoader


def load_pdfs(pdf_paths):

    documents = []

    for path in pdf_paths:

        loader = PyPDFLoader(path)

        docs = loader.load()

        documents.extend(docs)

    return documents
def format_sources(docs):

    sources=[]

    for doc in docs:

        file = doc.metadata.get(
            "source",
            "Unknown"
        )

        page = doc.metadata.get(
            "page",
            0
        ) + 1

        sources.append(
            f"{file} | Page {page}"
        )

    return list(
        set(sources)
    )
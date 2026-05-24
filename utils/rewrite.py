def rewrite_query(
    query,
    llm
):

    prompt = f"""
Rewrite the query for better retrieval.

Rules:
1. Keep original meaning.
2. Expand abbreviations if needed.
3. Return only improved query.

Query:
{query}
"""

    response = llm.invoke(
        prompt
    )

    return response.content
def refine_answer(
    query,
    docs,
    llm
):

    answer = ""

    for doc in docs:

        prompt = f"""

Current Answer:
{answer}

New Context:
{doc.page_content}

Question:
{query}

Refine answer.
"""

        response = (
            llm.invoke(
                prompt
            )
        )

        answer = (
            response.content
        )

    return answer
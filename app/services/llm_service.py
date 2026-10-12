from groq import Groq

from app.config import GROQ_API_KEY


client = Groq(
    api_key=GROQ_API_KEY
)


def ask_llm(prompt: str) -> str:

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": (
                    "Answer directly and concisely. "
                    "Do not include reasoning, thinking, "
                    "analysis, chain-of-thought, or "
                    "<think> tags. "
                    "Return only the final answer."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0,
        max_tokens=800,
        reasoning_effort="medium",
        reasoning_format="hidden",
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError(
            "LLM returned an empty response."
        )

    return content.strip()
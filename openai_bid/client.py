import os

from openai import OpenAI

BID_SYSTEM_PROMPT = """You are an expert freelancer assistant. For any project description provided, always respond in English, even if the user's prompt is in another language. First, generate a professional bid in a concise paragraph, followed by one short and focused question (1–2 lines) to clarify the client's intentions. Use light marketing: the bid should highlight your value, build trust, and give a reason to choose you (e.g. relevant experience, reliability, or fit). The question should engage the client and show genuine interest so they feel heard and more likely to respond positively and select you. Respect this exact format (plain text, no markdown):

Bid: [your bid text]

Question: [your question text]

Address: 709 Rue Al Massira, Immeuble N° 12, Hay Hassani Casablanca, Morocco

Ensure the question is clear and concise, and the bid is persuasive, professional, tailored to the project, and written to encourage the client to choose you. Always include the Address paragraph with the full address. Do not mention cost, pricing, or project duration in your response. Use plain text only—no markdown formatting (no headers, bold, lists, or other markdown syntax)."""


def generate_bid(project_title: str, project_details: str) -> str:
    """Call OpenAI to generate a bid for the given project. Returns the model response text."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return "Error: OPENAI_API_KEY environment variable is not set."

    client = OpenAI(api_key=api_key)
    user_content = f"Project title: {project_title}\n\nProject details:\n{project_details}"

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": BID_SYSTEM_PROMPT},
                {"role": "user", "content": user_content},
            ],
        )
        return (response.choices[0].message.content or "").strip()
    except Exception as e:
        return f"Error generating bid: {e}"

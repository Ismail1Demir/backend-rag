from openai import OpenAI
from app.config import OPENAI_API_KEY, OPENAI_MODEL
from app.prompts import SYSTEM_PROMPT

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_answer(query: str, context_chunks: list):

    context_text = "\n\n".join([chunk["text"] for chunk in context_chunks])
    
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT.format(context=context_text)},
            {"role": "user", "content": query}
        ],
        temperature=0.0 
    )
    
    return response.choices[0].message.content
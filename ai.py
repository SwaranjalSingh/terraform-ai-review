import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_review(resources):

    prompt = f"""
You are a Terraform infrastructure review assistant.

Analyze the Terraform changes below.

Provide a concise developer-friendly review containing:

1. Overall Impact: LOW / MEDIUM / HIGH / CRITICAL
2. Resource change counts
3. Important configuration changes
4. Destructive changes
5. Potential risks
6. Security concerns if identifiable
7. Developer attention required
8. Final recommendation

Rules:
- Only report information present in the supplied data.
- Never invent changes.
- Highlight DELETE and REPLACE operations.
- Clearly distinguish facts from assumptions.
- Do not expose sensitive information.
- Keep the response concise.

Terraform changes:

{resources}
"""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    return response.text
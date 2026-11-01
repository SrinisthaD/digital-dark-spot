
import os
import json

from dotenv import load_dotenv
from google import genai


# Load the Gemini API key from .env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key) if api_key else None


def analyze_sources(topic, sources):

    # Keep only successfully extracted sources
    successful_sources = [
        source for source in sources
        if source.get("error") is None and source.get("text")
    ]

    failed_sources = [
        source for source in sources
        if source.get("error") is not None
    ]

    if not successful_sources:
        return {
            "topic": topic,
            "summary": "No source content could be collected.",
            "sources_reviewed": 0,
            "information_gaps": [],
            "conflicts": [],
            "outdated_signals": [],
            "unanswered_questions": [],
            "verification_checklist": [
                "Check whether the supplied URLs are correct.",
                "Try accessing the webpages manually.",
                "Add accessible sources and analyze again."
            ],
            "failed_sources": failed_sources
        }

    if client is None:
        return {
            "topic": topic,
            "summary": "Gemini API key is missing.",
            "sources_reviewed": len(successful_sources),
            "information_gaps": [],
            "conflicts": [],
            "outdated_signals": [],
            "unanswered_questions": [],
            "verification_checklist": [
                "Check the GEMINI_API_KEY entry in the .env file."
            ],
            "failed_sources": failed_sources
        }

    # Give every source a unique ID
    source_text = ""

    for index, source in enumerate(successful_sources, start=1):
        source_id = f"S{index}"

        source_text += f"""
SOURCE ID: {source_id}
TITLE: {source.get("title", "Unknown")}
URL: {source.get("url", "Unknown")}
CONTENT:
{source.get("text", "")[:10000]}

--------------------------------
"""

    # Instructions for Gemini
    prompt = f"""
You are the AI research assistant for Digital Dark Spot.

Research topic: {topic}

Analyze the following collected sources:

{source_text}

Your tasks:

1. INFORMATION GAPS:
Identify important aspects of the topic that are not adequately
covered by the provided sources.

2. CONFLICTS:
Identify claims that appear to disagree between sources.
Only report a conflict when you can identify evidence from
at least two different sources.

3. OUTDATED SIGNALS:
Identify claims or information that may need an updated check.
Do not call something outdated merely because it is old.
Explain why verification is needed.

4. UNANSWERED QUESTIONS:
Suggest important research questions that these sources
do not adequately answer.

5. VERIFICATION CHECKLIST:
Create practical verification tasks.
Prioritize them as High, Medium, or Low.

IMPORTANT RULES:
- Use only the supplied source content.
- Never invent facts, quotations, or evidence.
- Do not treat missing information as proof that something is false.
- Do not claim a conflict unless the sources provide evidence.
- Every finding must include relevant source IDs.
- Include short supporting evidence quotes where possible.
- Label findings as potential or uncertain.
- If evidence is insufficient, say so.
- Do not present AI findings as confirmed facts.

Return ONLY valid JSON in this exact structure:

{{
  "summary": "Short summary of the sources",
  "information_gaps": [
    {{
      "issue": "Description of possible gap",
      "explanation": "Why it may be a gap",
      "source_ids": ["S1"],
      "evidence": "Supporting text or empty string",
      "confidence": "Low"
    }}
  ],
  "conflicts": [
    {{
      "claim": "The potentially conflicting claims",
      "explanation": "Why they appear to disagree",
      "source_ids": ["S1", "S2"],
      "evidence": "Supporting evidence",
      "confidence": "Medium"
    }}
  ],
  "outdated_signals": [
    {{
      "issue": "Information that may need updating",
      "explanation": "Reason for checking",
      "source_ids": ["S1"],
      "confidence": "Low"
    }}
  ],
  "unanswered_questions": [
    "Question that needs further research"
  ],
  "verification_checklist": [
    {{
      "task": "What should be verified",
      "priority": "High",
      "reason": "Why this matters"
    }}
  ]
}}

Keep the analysis concise and evidence-based.
Return at most:
- 3 information gaps
- 2 conflicts
- 2 outdated signals
- 3 unanswered questions
- 4 verification checklist items

Keep each explanation to 1-2 sentences.
Do not invent evidence or fill sections with unsupported claims.
Return valid JSON using the required structure.

"""

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "temperature": 0.2
            }
        )

        result = json.loads(response.text)

        # Add source counts and failed URLs
        result["topic"] = topic
        result["sources_reviewed"] = len(successful_sources)
        result["failed_sources"] = failed_sources

        return result

    except Exception as error:
        return {
            "topic": topic,
            "summary": "AI analysis could not be completed.",
            "sources_reviewed": len(successful_sources),
            "information_gaps": [],
            "conflicts": [],
            "outdated_signals": [],
            "unanswered_questions": [],
            "verification_checklist": [
                "Check the Gemini API connection and try again."
            ],
            "failed_sources": failed_sources,
            "analysis_error": str(error)
        }

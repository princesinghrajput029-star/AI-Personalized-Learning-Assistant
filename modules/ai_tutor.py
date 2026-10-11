# modules/ai_tutor.py

import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:3b"


def get_explanation(topic, subject, language, level):
    """
    Generate an AI-powered explanation using local Ollama.
    No OpenAI API key is required.
    """

    # --------------------------------------------------------
    # Language instruction
    # --------------------------------------------------------

    if language == "Hindi":

        language_instruction = """
Respond mainly in simple Hindi.
You may use English technical terms in brackets
where they make the concept easier to understand.
"""

    else:

        language_instruction = """
Respond in clear and simple English.
"""


    # --------------------------------------------------------
    # Level instruction
    # --------------------------------------------------------

    if level == "Beginner":

        level_instruction = """
The student is a beginner.
Explain the concept from the basics.
Use very simple language and everyday examples.
Avoid unnecessary technical complexity.
"""

    elif level == "Intermediate":

        level_instruction = """
The student has intermediate knowledge.
Explain the concept clearly with examples
and moderate technical detail.
"""

    else:

        level_instruction = """
The student is an advanced learner.
Provide a deeper and more technical explanation,
including important details and examples.
"""


    # --------------------------------------------------------
    # AI Prompt
    # --------------------------------------------------------

    prompt = f"""
You are an AI Personalized Learning Assistant.

A student wants to learn the following topic:

Subject: {subject}
Topic: {topic}
Student Level: {level}
Language: {language}

{language_instruction}

{level_instruction}

Your job is to teach this topic accurately and
in an educational way.

Structure your answer using these sections:

1. What is {topic}?
2. Simple Explanation
3. How it works
4. Real-world Example
5. Important Points
6. Quick Summary

Make the explanation engaging and easy for a student
to understand.

Do not say that the topic is unavailable.
Do not use placeholder text.
Always try to provide a useful educational explanation.
"""


    # --------------------------------------------------------
    # Call Ollama
    # --------------------------------------------------------

    try:

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )


        # Check HTTP response
        response.raise_for_status()


        # Read AI response
        data = response.json()

        answer = data.get(
            "response",
            ""
        ).strip()


        # ----------------------------------------------------
        # Successful response
        # ----------------------------------------------------

        if answer:

            return {
                "title": topic.title(),
                "explanation": answer
            }


        # ----------------------------------------------------
        # Empty AI response
        # ----------------------------------------------------

        return {
            "title": topic.title(),
            "explanation": (
                "The AI model returned an empty response. "
                "Please try the topic again."
            )
        }


    # --------------------------------------------------------
    # Connection / Model Error
    # --------------------------------------------------------

    except requests.exceptions.ConnectionError:

        return {
            "title": topic.title(),
            "explanation": """
⚠️ Local AI connection failed.

Please make sure Ollama is running on your computer.

Ollama should be available at:

http://localhost:11434
"""
        }


    except requests.exceptions.Timeout:

        return {
            "title": topic.title(),
            "explanation": """
⚠️ The AI model took too long to respond.

Please try again with a shorter topic.
"""
        }


    except Exception as error:

        return {
            "title": topic.title(),
            "explanation": f"""
⚠️ Something went wrong while generating
the AI explanation.

Error:
{error}
"""
        }
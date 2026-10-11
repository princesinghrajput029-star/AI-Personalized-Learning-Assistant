# modules/quiz_generator.py

import requests
import json
import random
import time


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:3b"


def generate_quiz(topic, subject, language, level):
    """
    Generate a topic-specific, randomized AI quiz
    using local Ollama.

    No OpenAI API is required.
    """

    # --------------------------------------------------------
    # Difficulty
    # --------------------------------------------------------

    if level == "Beginner":

        difficulty = """
Difficulty: Beginner to moderate.

Ask questions that test:
- basic concepts
- understanding
- simple application
- common misconceptions

Do NOT ask extremely easy definition-only questions.
"""

    elif level == "Intermediate":

        difficulty = """
Difficulty: Intermediate to difficult.

Ask questions that test:
- conceptual understanding
- application
- comparison
- reasoning
- examples
- common mistakes

Avoid simple definition-only questions.
"""

    else:

        difficulty = """
Difficulty: Advanced.

Ask challenging questions that test:
- deep conceptual understanding
- reasoning
- application
- analysis
- edge cases
- problem solving
- conceptual traps

Avoid basic definition questions.
"""


    # --------------------------------------------------------
    # Language
    # --------------------------------------------------------

    if language == "Hindi":

        language_instruction = """
Write questions and options in simple Hindi.

English technical terms may be included in brackets
when they are commonly used in the subject.
"""

    else:

        language_instruction = """
Write all questions and options in clear English.
"""


    # --------------------------------------------------------
    # Random attempt identifier
    # --------------------------------------------------------

    random_seed = random.randint(
        100000,
        999999999
    )

    timestamp = int(
        time.time()
    )


    # --------------------------------------------------------
    # AI Prompt
    # --------------------------------------------------------

    prompt = f"""
You are an expert AI teacher and competitive-exam
question generator.

Generate a completely NEW quiz.

SUBJECT:
{subject}

TOPIC:
{topic}

STUDENT LEVEL:
{level}

QUIZ ATTEMPT ID:
{random_seed}-{timestamp}

{difficulty}

{language_instruction}

IMPORTANT:

The questions MUST be directly related to the topic:

"{topic}"

Do NOT ask generic questions such as:

- What subject does this topic belong to?
- Why is practice important?
- What is important when learning this topic?
- Which subject is this topic related to?

Those questions are NOT allowed.

Instead, ask real educational questions about:

"{topic}"

For example, if the topic is Newton's Laws,
ask about force, acceleration, inertia, action-reaction,
real-world situations, calculations or conceptual cases.

If the topic is Reproduction,
ask about actual biological concepts,
processes, organs, mechanisms, differences,
fertilization, reproduction types, etc.

If the topic is Probability,
ask actual probability problems and reasoning questions.

Create exactly 5 questions.

Every question must have exactly 4 options.

Only ONE option can be correct.

Make the questions different from each other.

At least 2 questions should require reasoning
rather than simple memorization.

Make the questions challenging enough for the
student's selected level.

VERY IMPORTANT:

Every time this prompt is called, generate a
DIFFERENT set of questions.

Do NOT reuse common textbook questions.

Do NOT repeat questions from previous attempts.

Return ONLY JSON.

Use exactly this structure:

{{
    "questions": [
        {{
            "question": "Question text",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "answer": "Correct option"
        }}
    ]
}}

There must be exactly 5 question objects.
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
                "stream": False,

                # Randomness makes different attempts
                # generate different questions.
                "options": {
                    "temperature": 0.9,
                    "top_p": 0.95
                },

                "format": "json"
            },
            timeout=180
        )

        response.raise_for_status()

        data = response.json()

        raw_response = data.get(
            "response",
            ""
        ).strip()


        # ----------------------------------------------------
        # Parse JSON
        # ----------------------------------------------------

        quiz_data = json.loads(
            raw_response
        )


        # ----------------------------------------------------
        # Extract questions
        # ----------------------------------------------------

        questions = quiz_data.get(
            "questions",
            []
        )


        if not isinstance(
            questions,
            list
        ):

            raise ValueError(
                "Invalid question format."
            )


        # ----------------------------------------------------
        # Validate questions
        # ----------------------------------------------------

        valid_questions = []

        for question in questions:

            if not isinstance(
                question,
                dict
            ):
                continue


            question_text = question.get(
                "question"
            )

            options = question.get(
                "options"
            )

            answer = question.get(
                "answer"
            )


            # Question validation
            if not question_text:

                continue


            # Options validation
            if not isinstance(
                options,
                list
            ):

                continue


            if len(options) != 4:

                continue


            # Correct answer validation
            if answer not in options:

                continue


            valid_questions.append(
                {
                    "question": question_text,
                    "options": options,
                    "answer": answer
                }
            )


        # ----------------------------------------------------
        # Make sure we have enough questions
        # ----------------------------------------------------

        if len(valid_questions) < 5:

            raise ValueError(
                "AI generated fewer than 5 valid questions."
            )


        # ----------------------------------------------------
        # Shuffle question order
        # --------------------------------------------------------

        random.shuffle(
            valid_questions
        )


        # Shuffle options
        # --------------------------------------------------------

        for question in valid_questions:

            correct_answer = question["answer"]

            random.shuffle(
                question["options"]
            )

            question["answer"] = correct_answer


        return valid_questions[:5]


    # --------------------------------------------------------
    # AI generation error
    # --------------------------------------------------------

    except Exception as error:

        print(
            "Quiz generation error:",
            error
        )

        return create_better_fallback(
            topic,
            subject,
            language
        )


# ============================================================
# BACKUP QUIZ
# ============================================================

def create_better_fallback(
    topic,
    subject,
    language
):
    """
    Minimal backup quiz.

    This should only appear if Ollama fails completely.
    """

    if language == "Hindi":

        return [
            {
                "question": (
                    f"AI quiz generate नहीं हो सका। "
                    f"आपने कौन-सा topic चुना है?"
                ),
                "options": [
                    topic,
                    "अन्य विषय",
                    "कोई topic नहीं",
                    "सामान्य ज्ञान"
                ],
                "answer": topic
            },
            {
                "question": (
                    f"{topic} को अच्छी तरह सीखने के लिए "
                    f"सबसे उपयोगी तरीका कौन-सा है?"
                ),
                "options": [
                    "Concept को समझकर application करना",
                    "केवल answers याद करना",
                    "Topic छोड़ देना",
                    "बिना समझे अनुमान लगाना"
                ],
                "answer": "Concept को समझकर application करना"
            },
            {
                "question": (
                    f"{topic} में improvement के लिए "
                    f"क्या करना चाहिए?"
                ),
                "options": [
                    "Practice और revision",
                    "Practice बंद करना",
                    "Topic ignore करना",
                    "केवल guessing करना"
                ],
                "answer": "Practice और revision"
            }
        ]


    return [
        {
            "question": (
                f"The AI quiz could not be generated. "
                f"Which topic did you select?"
            ),
            "options": [
                topic,
                "Another subject",
                "No topic",
                "General knowledge"
            ],
            "answer": topic
        },
        {
            "question": (
                f"What is the best way to learn {topic}?"
            ),
            "options": [
                "Understand and apply the concepts",
                "Only memorize answers",
                "Skip the topic",
                "Only guess"
            ],
            "answer": "Understand and apply the concepts"
        },
        {
            "question": (
                f"How can a student improve in {topic}?"
            ),
            "options": [
                "Practice and revision",
                "Stop practicing",
                "Ignore the topic",
                "Only guess answers"
            ],
            "answer": "Practice and revision"
        }
    ]
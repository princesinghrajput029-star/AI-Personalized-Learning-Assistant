
import html
import random
from datetime import datetime

import pandas as pd
import streamlit as st

from modules.ai_tutor import get_explanation
from modules.quiz_generator import generate_quiz


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="LearnMate AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# SESSION STATE
# =========================================================

DEFAULTS = {
    "page": "Learn",
    "navigation_radio": "Learn",
    "student_name": "Student",
    "current_topic": "",
    "current_subject": "Computer Science",
    "current_language": "English",
    "current_level": "Beginner",
    "lesson": None,
    "quiz": [],
    "quiz_answers": {},
    "quiz_submitted": False,
    "quiz_topic": "",
    "quiz_subject": "",
    "quiz_language": "English",
    "quiz_level": "Beginner",
    "history": [],
    "topic_stats": {},
    "last_result": None,
    "notice": "",
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# ANIMATED BACKGROUND AND UI STYLING
# =========================================================

st.markdown(
    """
    <style>
    @import url(
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
    );

    .stApp {
        background: #0b1020;
        color: #f3f4f6;
        font-family: 'Inter', sans-serif;
        overflow-x: hidden;
    }

    /* Moving purple, teal and blue background */
    .stApp::before {
        content: "";
        position: fixed;
        inset: -35%;
        z-index: 0;
        pointer-events: none;

        background:
            radial-gradient(
                circle at 20% 30%,
                rgba(125, 70, 255, 0.32),
                transparent 30%
            ),
            radial-gradient(
                circle at 75% 25%,
                rgba(0, 220, 200, 0.22),
                transparent 28%
            ),
            radial-gradient(
                circle at 65% 80%,
                rgba(60, 100, 255, 0.22),
                transparent 32%
            );

        background-size: 160% 160%;
        animation: auroraMove 14s ease-in-out infinite alternate;
    }

    .stApp::after {
        content: "";
        position: fixed;
        inset: 0;
        z-index: 0;
        pointer-events: none;

        background:
            radial-gradient(
                ellipse at 50% 0%,
                rgba(120, 80, 255, 0.09),
                transparent 55%
            );

        animation: glowPulse 7s ease-in-out infinite alternate;
    }

    .stApp [data-testid="stAppViewContainer"],
    .stApp [data-testid="stHeader"] {
        background: transparent;
    }

    .stApp [data-testid="stAppViewContainer"] > .main {
        position: relative;
        z-index: 1;
    }

    [data-testid="stSidebar"] {
        background: rgba(15, 20, 39, 0.97);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }

    @keyframes auroraMove {
        0% {
            transform: translate3d(-4%, -3%, 0)
                       rotate(0deg) scale(1);
            background-position: 0% 0%;
        }

        50% {
            transform: translate3d(3%, 4%, 0)
                       rotate(4deg) scale(1.08);
            background-position: 100% 50%;
        }

        100% {
            transform: translate3d(-2%, 2%, 0)
                       rotate(-3deg) scale(1.03);
            background-position: 20% 100%;
        }
    }

    @keyframes glowPulse {
        0% { opacity: 0.45; }
        100% { opacity: 1; }
    }

    .hero {
        padding: 32px;
        border-radius: 24px;
        background: linear-gradient(
            120deg,
            rgba(48, 32, 100, 0.88),
            rgba(20, 70, 86, 0.82),
            rgba(22, 30, 61, 0.90)
        );
        border: 1px solid rgba(255, 255, 255, 0.13);
        margin-bottom: 24px;
        animation: appear 0.7s ease;
    }

    .hero h1 {
        font-size: clamp(30px, 4vw, 44px);
        font-weight: 800;
        color: white;
        margin-bottom: 10px;
    }

    .hero p {
        color: #d8def5;
        font-size: 16px;
    }

    .eyebrow {
        color: #76e7d2;
        letter-spacing: 2px;
        font-size: 12px;
        font-weight: 800;
    }

    .panel {
        background: rgba(255, 255, 255, 0.045);
        border: 1px solid rgba(255, 255, 255, 0.10);
        padding: 22px;
        border-radius: 18px;
        margin-bottom: 16px;
    }

    .panel h3 {
        color: #c6b8ff;
    }

    .tag {
        display: inline-block;
        background: rgba(118, 231, 210, 0.12);
        color: #76e7d2;
        border: 1px solid rgba(118, 231, 210, 0.25);
        padding: 5px 10px;
        border-radius: 30px;
        font-size: 12px;
        margin: 3px;
    }

    .metric-card {
        padding: 18px;
        border: 1px solid rgba(255, 255, 255, 0.10);
        background: rgba(255, 255, 255, 0.05);
        border-radius: 17px;
        min-height: 110px;
    }

    .metric-label {
        color: #aab4cc;
        font-size: 13px;
    }

    .metric-value {
        font-size: 27px;
        font-weight: 800;
        color: #ffffff;
        margin-top: 8px;
    }

    .stButton > button {
        border-radius: 12px;
        font-weight: 700;
        min-height: 43px;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        border-color: #76e7d2;
        transform: translateY(-1px);
    }

    @keyframes appear {
        from {
            opacity: 0;
            transform: translateY(12px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            animation-duration: 0.01ms !important;
            transition-duration: 0.01ms !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def safe_text(value):
    if value is None:
        return ""
    return str(value)


def normalize_answer(value):
    return " ".join(safe_text(value).strip().casefold().split())


def go_to_progress():
    st.session_state.page = "Progress Dashboard"
    st.session_state.navigation_radio = "Progress Dashboard"


def get_topic_stats(topic):
    key = topic.strip().casefold()
    return st.session_state.topic_stats.get(
        key,
        {
            "topic": topic,
            "attempts": 0,
            "correct": 0,
            "total": 0,
            "scores": [],
        },
    )


def adaptive_level(topic, selected_level):
    stats = get_topic_stats(topic)

    if stats["attempts"] == 0 or stats["total"] == 0:
        return selected_level

    accuracy = stats["correct"] / stats["total"] * 100
    levels = ["Beginner", "Intermediate", "Advanced"]
    index = levels.index(selected_level)

    if accuracy >= 85:
        index = min(index + 1, 2)
    elif accuracy < 50:
        index = max(index - 1, 0)

    return levels[index]


def create_lesson(topic, subject, language, level):
    with st.spinner("AI tutor is preparing your lesson..."):
        result = get_explanation(topic, subject, language, level)

    if isinstance(result, dict):
        title = result.get("title", topic)
        explanation = result.get("explanation", "")
    else:
        title = topic
        explanation = safe_text(result)

    return {
        "title": safe_text(title),
        "explanation": safe_text(explanation),
        "topic": topic,
        "subject": subject,
        "language": language,
        "level": level,
    }


def create_quiz(topic, subject, language, selected_level):
    level = adaptive_level(topic, selected_level)

    with st.spinner(
        f"Generating your {level.lower()} quiz using local AI..."
    ):
        questions = generate_quiz(topic, subject, language, level)

    if not isinstance(questions, list):
        raise ValueError("Quiz generator did not return a valid list.")

    valid_questions = []

    for item in questions:
        if not isinstance(item, dict):
            continue

        question = item.get("question")
        options = item.get("options")
        answer = item.get("answer")

        if not question or not isinstance(options, list):
            continue

        if len(options) != 4 or answer is None:
            continue

        if not any(
            normalize_answer(option) == normalize_answer(answer)
            for option in options
        ):
            continue

        valid_questions.append({
            "question": safe_text(question),
            "options": [safe_text(option) for option in options],
            "answer": safe_text(answer),
        })

    if not valid_questions:
        raise ValueError(
            "No valid quiz questions were generated. "
            "Check Ollama and try again."
        )

    random.shuffle(valid_questions)

    st.session_state.quiz = valid_questions[:5]
    st.session_state.quiz_answers = {}
    st.session_state.quiz_submitted = False
    st.session_state.quiz_topic = topic
    st.session_state.quiz_subject = subject
    st.session_state.quiz_language = language
    st.session_state.quiz_level = level
    st.session_state.last_result = None

    return level


def recommendation_for(score, total, topic):
    if total == 0:
        return "Try a quiz to receive your personalized recommendation."

    accuracy = score / total * 100

    if accuracy >= 85:
        return (
            f"Excellent work on {topic}! Try advanced application questions "
            "or move to a related topic."
        )

    if accuracy >= 60:
        return (
            f"Good progress on {topic}. Review the questions you missed, "
            "then attempt another quiz."
        )

    return (
        f"Revise the basic concepts of {topic}, read the explanation again, "
        "and try a quiz at an easier level."
    )


def save_result(score):
    questions = st.session_state.quiz
    answers = st.session_state.quiz_answers
    topic = st.session_state.quiz_topic
    subject = st.session_state.quiz_subject
    language = st.session_state.quiz_language
    level = st.session_state.quiz_level
    total = len(questions)

    percentage = round(score / total * 100, 1) if total else 0
    key = topic.strip().casefold()

    if key not in st.session_state.topic_stats:
        st.session_state.topic_stats[key] = {
            "topic": topic,
            "attempts": 0,
            "correct": 0,
            "total": 0,
            "scores": [],
        }

    stats = st.session_state.topic_stats[key]
    stats["attempts"] += 1
    stats["correct"] += score
    stats["total"] += total
    stats["scores"].append(percentage)

    missed = []

    for i, question in enumerate(questions):
        selected = answers.get(str(i))
        correct = question["answer"]

        if normalize_answer(selected) != normalize_answer(correct):
            missed.append({
                "question": question["question"],
                "selected": selected or "Not answered",
                "correct": correct,
            })

    result = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "topic": topic,
        "subject": subject,
        "language": language,
        "level": level,
        "score": score,
        "total": total,
        "percentage": percentage,
        "missed": missed,
        "recommendation": recommendation_for(score, total, topic),
    }

    st.session_state.history.append(result)
    st.session_state.last_result = result


def metric_card(label, value, subtitle):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{html.escape(str(label))}</div>
            <div class="metric-value">{html.escape(str(value))}</div>
            <div class="metric-label">{html.escape(str(subtitle))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.markdown("## 🎓 LearnMate AI")
    st.caption("Your personal learning companion")
    st.divider()

    st.radio(
        "Navigation",
        ["Learn", "Progress Dashboard", "About"],
        key="navigation_radio",
        on_change=lambda: setattr(
            st.session_state,
            "page",
            st.session_state.navigation_radio,
        ),
    )

    # Sync the displayed page with the sidebar selection.
    st.session_state.page = st.session_state.navigation_radio

    st.divider()
    st.markdown("### ⚙️ Learning preferences")

    st.session_state.student_name = st.text_input(
        "Your name",
        value=st.session_state.student_name,
        max_chars=40,
    ).strip() or "Student"

    subject = st.selectbox(
        "Subject",
        [
            "Computer Science",
            "Mathematics",
            "Physics",
            "Chemistry",
            "Biology",
            "Environmental Science",
            "English",
            "Other",
        ],
        key="subject_select",
    )

    language = st.selectbox(
        "Learning language",
        ["English", "Hindi"],
        key="language_select",
    )

    selected_level = st.selectbox(
        "Starting difficulty",
        ["Beginner", "Intermediate", "Advanced"],
        key="level_select",
    )

    st.divider()
    st.caption("Local AI: Ollama")
    st.caption("Model: llama3.2:3b")
    st.caption("No paid OpenAI API required")


# =========================================================
# HERO SECTION
# =========================================================

student_name = html.escape(st.session_state.student_name)

st.markdown(
    f"""
    <div class="hero">
        <div class="eyebrow">PERSONALIZED AI LEARNING</div>
        <h1>Learn smarter, {student_name}. ✨</h1>
        <p>
            Understand any topic, practice with AI-generated questions,
            identify learning gaps, and get your next recommendation.
        </p>
        <span class="tag">Hindi + English</span>
        <span class="tag">Adaptive quizzes</span>
        <span class="tag">Local AI</span>
        <span class="tag">Progress tracking</span>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# LEARN PAGE
# =========================================================

if st.session_state.page == "Learn":

    st.header("Start your learning journey")
    st.caption(
        "Enter any topic. You are not restricted to a predefined topic list."
    )

    with st.form("topic_form"):
        topic_input = st.text_input(
            "What do you want to learn?",
            value=st.session_state.current_topic,
            placeholder="Example: Binary search, Newton's laws, photosynthesis",
            max_chars=150,
        )

        generate_lesson_button = st.form_submit_button(
            "✨ Generate my lesson",
            use_container_width=True,
        )

    if generate_lesson_button:
        topic = topic_input.strip()

        if not topic:
            st.warning("Please enter a topic first.")
        else:
            st.session_state.current_topic = topic
            st.session_state.current_subject = subject
            st.session_state.current_language = language
            st.session_state.current_level = selected_level

            try:
                st.session_state.lesson = create_lesson(
                    topic,
                    subject,
                    language,
                    selected_level,
                )
                st.session_state.notice = ""
            except Exception as error:
                st.error(f"Lesson generation failed: {error}")

    lesson = st.session_state.lesson

    if lesson:
        st.divider()

        st.markdown(
            f"""
            <div class="panel">
                <div class="eyebrow">YOUR PERSONALIZED LESSON</div>
                <h2>{html.escape(lesson["title"])}</h2>
                <p>
                    Subject: {html.escape(lesson["subject"])} |
                    Level: {html.escape(lesson["level"])} |
                    Language: {html.escape(lesson["language"])}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.container(border=True):
            st.markdown(lesson["explanation"])

        col1, col2 = st.columns(2)

        with col1:
            if st.button(
                "🧠 Generate a quiz",
                use_container_width=True,
                type="primary",
            ):
                try:
                    used_level = create_quiz(
                        lesson["topic"],
                        lesson["subject"],
                        lesson["language"],
                        selected_level,
                    )
                    st.session_state.notice = (
                        f"Quiz generated at {used_level} difficulty."
                    )
                    st.rerun()
                except Exception as error:
                    st.error(f"Quiz generation failed: {error}")

        with col2:
            if st.button(
                "🔄 Regenerate explanation",
                use_container_width=True,
            ):
                try:
                    st.session_state.lesson = create_lesson(
                        lesson["topic"],
                        lesson["subject"],
                        lesson["language"],
                        selected_level,
                    )
                    st.rerun()
                except Exception as error:
                    st.error(f"Explanation generation failed: {error}")

    if st.session_state.notice:
        st.success(st.session_state.notice)

    # -----------------------------------------------------
    # QUIZ AREA
    # -----------------------------------------------------

    if st.session_state.quiz:
        st.divider()
        st.header("Knowledge check")

        st.caption(
            f"Topic: {st.session_state.quiz_topic} | "
            f"Difficulty: {st.session_state.quiz_level}"
        )

        questions = st.session_state.quiz

        if not st.session_state.quiz_submitted:
            with st.form("quiz_form"):
                answers = {}

                for i, question in enumerate(questions):
                    st.markdown(
                        f"**Q{i + 1}. {question['question']}**"
                    )

                    answers[str(i)] = st.radio(
                        "Select an answer",
                        question["options"],
                        index=None,
                        key=f"answer_{i}",
                        label_visibility="collapsed",
                    )

                    st.write("")

                submit_quiz = st.form_submit_button(
                    "Submit answers",
                    type="primary",
                    use_container_width=True,
                )

            if submit_quiz:
                st.session_state.quiz_answers = answers

                score = 0

                for i, question in enumerate(questions):
                    selected_answer = answers.get(str(i))

                    if (
                        selected_answer is not None
                        and normalize_answer(selected_answer)
                        == normalize_answer(question["answer"])
                    ):
                        score += 1

                save_result(score)
                st.session_state.quiz_submitted = True
                st.rerun()

        else:
            result = st.session_state.last_result

            if result:
                st.markdown(
                    f"""
                    <div class="panel">
                        <div class="eyebrow">QUIZ RESULT</div>
                        <h2>{result["score"]} / {result["total"]} correct</h2>
                        <p>Accuracy: {result["percentage"]}%</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.progress(result["percentage"] / 100)

                if result["percentage"] >= 85:
                    st.success("Excellent! You have a strong understanding.")
                elif result["percentage"] >= 60:
                    st.info("Good effort! Review the missed questions.")
                else:
                    st.warning(
                        "Revise the basics and try another quiz at an easier level."
                    )

            st.subheader("Answer review")

            for i, question in enumerate(questions):
                selected = st.session_state.quiz_answers.get(str(i))
                correct = question["answer"]

                with st.container(border=True):
                    st.markdown(
                        f"**Q{i + 1}. {question['question']}**"
                    )

                    if (
                        selected is not None
                        and normalize_answer(selected)
                        == normalize_answer(correct)
                    ):
                        st.success(f"Your answer: {selected}")
                    else:
                        st.error(
                            f"Your answer: {selected or 'Not answered'}"
                        )
                        st.info(f"Correct answer: {correct}")

            if result:
                st.markdown(
                    f"""
                    <div class="panel">
                        <h3>🎯 Your next recommendation</h3>
                        <p>{html.escape(result["recommendation"])}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            col1, col2 = st.columns(2)

            with col1:
                if st.button(
                    "🔁 Try another quiz",
                    use_container_width=True,
                    type="primary",
                ):
                    try:
                        used_level = create_quiz(
                            st.session_state.quiz_topic,
                            st.session_state.quiz_subject,
                            st.session_state.quiz_language,
                            selected_level,
                        )
                        st.session_state.notice = (
                            f"New quiz generated at {used_level} difficulty."
                        )
                        st.rerun()
                    except Exception as error:
                        st.error(f"Could not generate another quiz: {error}")

            with col2:
                st.button(
                    "📊 View progress",
                    use_container_width=True,
                    on_click=go_to_progress,
                )


# =========================================================
# PROGRESS DASHBOARD
# =========================================================

elif st.session_state.page == "Progress Dashboard":

    st.header("📊 Your progress dashboard")
    st.caption(
        "Review quiz performance, identify weak topics, and plan your next step."
    )

    history = st.session_state.history

    total_attempts = len(history)
    total_questions = sum(item["total"] for item in history)
    total_correct = sum(item["score"] for item in history)

    overall_accuracy = (
        round(total_correct / total_questions * 100, 1)
        if total_questions
        else 0
    )

    total_topics = len(st.session_state.topic_stats)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card("Quiz attempts", total_attempts, "Completed quizzes")

    with c2:
        metric_card("Overall accuracy", f"{overall_accuracy}%", "All attempts")

    with c3:
        metric_card("Topics practiced", total_topics, "Unique topics")

    with c4:
        metric_card("Correct answers", total_correct, "Questions answered correctly")

    st.divider()

    if not history:
        st.info(
            "No quiz attempts yet. Go to Learn, generate a lesson, "
            "complete a quiz, and return here to see your progress."
        )

        if st.button("📚 Go to Learn", type="primary"):
            st.session_state.page = "Learn"
            st.session_state.navigation_radio = "Learn"
            st.rerun()

    else:
        left, right = st.columns(2)

        with left:
            st.subheader("Recent performance")

            recent = history[-10:]

            chart_df = pd.DataFrame({
                "Attempt": [
                    f"Attempt {i + 1}"
                    for i in range(len(recent))
                ],
                "Accuracy (%)": [
                    item["percentage"]
                    for item in recent
                ],
            })

            st.line_chart(
                chart_df.set_index("Attempt"),
                y="Accuracy (%)",
            )

        with right:
            st.subheader("Topic performance")

            topic_rows = []

            for stats in st.session_state.topic_stats.values():
                accuracy = (
                    stats["correct"] / stats["total"] * 100
                    if stats["total"]
                    else 0
                )

                topic_rows.append({
                    "Topic": stats["topic"],
                    "Accuracy (%)": round(accuracy, 1),
                })

            topic_df = pd.DataFrame(topic_rows)

            if not topic_df.empty:
                st.bar_chart(
                    topic_df.set_index("Topic"),
                    y="Accuracy (%)",
                )

        st.divider()
        st.subheader("🎯 Topics needing improvement")

        weak_topics = []

        for stats in st.session_state.topic_stats.values():
            if stats["total"]:
                accuracy = stats["correct"] / stats["total"] * 100

                if accuracy < 60:
                    weak_topics.append((stats["topic"], accuracy))

        if weak_topics:
            for topic_name, accuracy in sorted(
                weak_topics,
                key=lambda item: item[1],
            ):
                st.markdown(
                    f"""
                    <div class="panel">
                        <h3>📌 {html.escape(topic_name)}</h3>
                        <p>Accuracy: {accuracy:.1f}%</p>
                        <p>
                            Recommendation: revise the explanation,
                            solve examples, and retry the quiz.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.success(
                "No weak topics detected yet, or there is not enough "
                "performance data to identify them."
            )

        st.divider()
        st.subheader("Attempt history")

        history_df = pd.DataFrame([
            {
                "Date": item["date"],
                "Topic": item["topic"],
                "Subject": item["subject"],
                "Difficulty": item["level"],
                "Score": f'{item["score"]}/{item["total"]}',
                "Accuracy": f'{item["percentage"]}%',
            }
            for item in reversed(history)
        ])

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True,
        )

        st.download_button(
            "⬇️ Download progress report",
            data=history_df.to_csv(index=False).encode("utf-8-sig"),
            file_name="learnmate_progress.csv",
            mime="text/csv",
        )

    st.caption(
        "Note: progress is currently stored in the active Streamlit session. "
        "It is not permanently saved to a database."
    )


# =========================================================
# ABOUT PAGE
# =========================================================

elif st.session_state.page == "About":

    st.header("About LearnMate AI")

    st.markdown(
        """
        <div class="panel">
            <h3>🎓 Personalized learning for every student</h3>
            <p>
                LearnMate AI helps students learn at their own pace
                through AI-generated explanations, quizzes, performance
                analysis, and adaptive learning recommendations.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    features = [
        ("📚", "Personalized AI tutor"),
        ("🌐", "Hindi and English support"),
        ("🧠", "Topic-based quiz generation"),
        ("📈", "Adaptive quiz difficulty"),
        ("🎯", "Weak-topic detection"),
        ("📊", "Performance dashboard"),
        ("💻", "Local Ollama model"),
    ]

    for icon, feature in features:
        st.markdown(f"- {icon} **{feature}**")

    st.info(
        "Built with Streamlit and Ollama. No paid OpenAI API key is required."
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "LearnMate AI | Personalized Learning Assistant | "
    "SDG 4: Quality Education"
)

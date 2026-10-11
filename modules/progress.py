# modules/progress.py

def initialize_progress():
    return {
        "quizzes": [],
        "topics": [],
        "scores": [],
        "topic_performance": {}
    }


def add_quiz_result(progress, topic, score, total_questions):
    if total_questions <= 0:
        percentage = 0
    else:
        percentage = int((score / total_questions) * 100)

    progress.setdefault("quizzes", [])
    progress.setdefault("topics", [])
    progress.setdefault("scores", [])
    progress.setdefault("topic_performance", {})

    progress["quizzes"].append({
        "topic": topic,
        "score": score,
        "total": total_questions,
        "percentage": percentage
    })

    if topic not in progress["topics"]:
        progress["topics"].append(topic)

    progress["scores"].append(percentage)

    topic_data = progress["topic_performance"].setdefault(
        topic,
        {
            "attempts": 0,
            "total_score": 0,
            "total_questions": 0,
            "scores": []
        }
    )

    topic_data["attempts"] += 1
    topic_data["total_score"] += score
    topic_data["total_questions"] += total_questions
    topic_data["scores"].append(percentage)

    return progress


def get_topic_analysis(progress):
    topic_performance = progress.setdefault(
        "topic_performance", {}
    )

    # Recover older quiz results if topic statistics are missing.
    if not topic_performance:
        for quiz in progress.get("quizzes", []):
            topic = quiz["topic"]

            data = topic_performance.setdefault(
                topic,
                {
                    "attempts": 0,
                    "total_score": 0,
                    "total_questions": 0,
                    "scores": []
                }
            )

            data["attempts"] += 1
            data["total_score"] += quiz["score"]
            data["total_questions"] += quiz["total"]
            data["scores"].append(quiz["percentage"])

    analysis = {}

    for topic, data in topic_performance.items():
        total_questions = data["total_questions"]

        average = (
            int(data["total_score"] * 100 / total_questions)
            if total_questions > 0
            else 0
        )

        if average < 60:
            status = "Weak Topic"
            recommendation = (
                f"Revise {topic}, review the explanation, "
                "and practise beginner-level questions."
            )

        elif average < 80:
            status = "Needs Practice"
            recommendation = (
                f"Practise {topic} again and strengthen "
                "your conceptual understanding."
            )

        else:
            status = "Strong Topic"
            recommendation = (
                f"Great progress in {topic}! Try advanced, "
                "application-based questions."
            )

        analysis[topic] = {
            "attempts": data["attempts"],
            "average_score": average,
            "status": status,
            "recommendation": recommendation
        }

    return analysis


def get_progress_summary(progress):
    quizzes = progress.get("quizzes", [])
    scores = progress.get("scores", [])

    if not quizzes:
        return {
            "total_quizzes": 0,
            "average_score": 0,
            "best_score": 0,
            "topics_completed": 0
        }

    return {
        "total_quizzes": len(quizzes),
        "average_score": (
            int(sum(scores) / len(scores)) if scores else 0
        ),
        "best_score": max(scores) if scores else 0,
        "topics_completed": len(
            set(quiz["topic"] for quiz in quizzes)
        )
    }
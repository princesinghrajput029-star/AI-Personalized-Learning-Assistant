def analyze_performance(score, total_questions, topic):
    """Analyze performance and recommend the next quiz difficulty."""

    if total_questions <= 0:
        return {
            "score": 0,
            "percentage": 0,
            "level": "No Data",
            "status": "No quiz attempted",
            "recommendation": f"Start learning {topic}.",
            "next_difficulty": "Beginner",
            "weakness": "Unknown"
        }

    percentage = int((score / total_questions) * 100)

    if percentage >= 80:
        performance_level = "Excellent"
        status = "Strong understanding"
        weakness = "Low"
        next_difficulty = "Advanced"
        recommendation = (
            f"You understand {topic} well. "
            "Try advanced, application-based questions next."
        )

    elif percentage >= 60:
        performance_level = "Good"
        status = "Needs more practice"
        weakness = "Medium"
        next_difficulty = "Intermediate"
        recommendation = (
            f"Keep practising {topic} and strengthen "
            "your understanding before advancing."
        )

    else:
        performance_level = "Needs Improvement"
        status = "Weak understanding"
        weakness = "High"
        next_difficulty = "Beginner"
        recommendation = (
            f"Review {topic}, revisit the explanation, "
            "and practise easier questions."
        )

    return {
        "score": score,
        "percentage": percentage,
        "level": performance_level,
        "status": status,
        "recommendation": recommendation,
        "next_difficulty": next_difficulty,
        "weakness": weakness
    }

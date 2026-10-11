# 🎓 AI Personalized Learning Assistant

An AI-powered learning platform that helps students understand topics, practice through quizzes, identify learning gaps, and receive personalized learning recommendations.

Built with **Python, Streamlit, and Ollama**, this project uses a local language model to provide an affordable learning assistant without requiring a paid OpenAI API.

[View Repository](https://github.com/princesinghrajput029-star/AI-Personalized-Learning-Assistant)

## ✨ Features

- **Personalized AI Tutor** — Generate easy-to-understand explanations for topics entered by the learner.
- **Bilingual Learning** — Choose between English and Hindi.
- **Multiple Subjects** — Learn Computer Science, Mathematics, Physics, Chemistry, Biology, Environmental Science, English, and other topics.
- **AI-Generated Quizzes** — Practice with multiple-choice questions based on the selected topic.
- **Adjustable Difficulty** — Select Beginner, Intermediate, or Advanced difficulty.
- **Performance Analysis** — Review quiz scores, accuracy, and correct answers.
- **Learning Recommendations** — Receive next-step suggestions based on quiz performance.
- **Progress Dashboard** — Review quiz attempts, overall accuracy, practiced topics, and learning history.
- **Local AI Inference** — Run the assistant using Ollama and the `llama3.2:3b` model.

## 🖥️ Application Screenshots

Screenshots will be added here after capturing the actual running application.

| Learning Interface | Quiz Results |
|---|---|
| `assets/screenshots/learning.png` | `assets/screenshots/quiz-result.png` |

| Progress Dashboard | Learning Recommendations |
|---|---|
| `assets/screenshots/dashboard.png` | `assets/screenshots/recommendations.png` |

## 🔄 How It Works

1. Select a subject, preferred language, and starting difficulty.
2. Enter any topic you want to learn.
3. Generate an AI-powered lesson.
4. Take the quiz generated for that topic.
5. Review your score and answers.
6. Use the recommendations and progress dashboard to decide what to study next.

## 🛠️ Technology Stack

- **Programming Language:** Python
- **Frontend and Application Framework:** Streamlit
- **Local AI Runtime:** Ollama
- **Language Model:** Llama 3.2 (3B)
- **Data Format:** JSON for subject data
- **Version Control:** Git and GitHub

## 🚀 Getting Started

### Prerequisites

- Python installed on your computer
- Git
- [Ollama](https://ollama.com/download) installed
- Sufficient memory and storage to run the selected local AI model

### 1. Clone the repository

```bash
git clone https://github.com/princesinghrajput029-star/AI-Personalized-Learning-Assistant.git
cd AI-Personalized-Learning-Assistant
```

### 2. Create and activate a virtual environment

**Windows PowerShell:**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Python dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Download the Ollama model

```powershell
ollama pull llama3.2:3b
```

Make sure Ollama is running. If it is not already running in the background, start its service using:

```powershell
ollama serve
```

### 5. Launch the application

```powershell
streamlit run app.py
```

Open the local URL printed in the terminal, usually `http://localhost:8501`.

## 📁 Project Structure

```text
AI-Personalized-Learning-Assistant/
├── app.py
├── config/
│   └── config.py
├── data/
│   └── subjects.json
├── modules/
│   ├── ai_tutor.py
│   ├── performance.py
│   ├── progress.py
│   ├── quiz_generator.py
│   └── recommendation.py
├── assets/
│   └── screenshots/
├── requirements.txt
├── .gitignore
└── README.md
```

## 🎯 Project Objective

The objective is to make personalized learning more accessible by helping students study at their own pace, practice concepts, review performance, and identify areas that need additional attention.

The project aligns with **United Nations Sustainable Development Goal 4 (SDG 4): Quality Education**.

## 🔮 Future Enhancements

- More detailed topic-level performance analytics
- Persistent student profiles and learning history
- More robust quiz validation and question diversity
- Exportable progress reports
- Additional Indian languages
- Unit tests and automated quality checks
- Optional online deployment

## ⚠️ Limitations

- AI-generated explanations and answers may occasionally be incorrect; important academic information should be verified.
- Response speed depends on the computer's hardware and the local model.
- Ollama and the required model must be available for AI-powered features to work.
- Performance insights depend on the quiz attempts and data available to the application.

## 👨‍💻 Author

**Prince Singh Rajput**

GitHub: [@princesinghrajput029-star](https://github.com/princesinghrajput029-star)

---

If you find this project useful, consider giving the repository a ⭐ on GitHub.

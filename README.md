
# Interview Practice Partner — AI Voice Mock Interview Agent

Author: Aastha

Repository Link: https://github.com/Aerohika/Interview-Practice-Partner

Demo Video Link : https://drive.google.com/file/d/1zuLtyU3IP6yWc7j29oJM3iNDOZj8i_lq/view?usp=drivesdk

<p align="center">
  <img src="https://img.shields.io/badge/AI%20Interview%20Practice%20Partner-Voice%20Mock%20Interview%20Agent-blue?style=for-the-badge&logo=spark&logoColor=white">
</p>

<p align="center">
  <b>Simulate real job interviews using AI : ask, answer, learn & improve</b><br>
  <sub>Voice-powered mock interview assistant built with Streamlit + Whisper + Gemini</sub>
</p>

---

## 📌 Project Overview

The **Interview Practice Partner** is an AI-powered mock interview system that helps users prepare for real job interviews. It asks dynamic and role-specific questions, listens to voice responses, asks follow-ups intelligently, and finally provides detailed feedback for improvement.

Interaction is **fully voice-enabled** to simulate a realistic interview experience.

---

## 🚀 Key Capabilities

| Capability                              | Description                                                    |
| --------------------------------------- | -------------------------------------------------------------- |
| 🎙 Voice-only interaction               | Users answer verbally — no typing required                     |
| 🔊 Auto-played interviewer audio        | Every question is spoken like a real interview                 |
| 💬 Follow-up questions based on answers | Interviewer adapts dynamically using Gemini                    |
| 📚 Role-specific interviews             | Candidate sets the target job role                             |
| 🧠 Whisper speech-to-text               | Converts verbal answers into text for AI evaluation            |
| 📊 Post-interview report                | Feedback on communication, technical depth & improvement areas |

---

## 🏗 Architecture

```
User (Voice Response)
   ↓
Streamlit Microphone Recorder
   ↓
Whisper (Speech → Text)
   ↓
Gemini Interview Engine
 ▪ Generates next question
 ▪ Evaluates responses
   ↓
pyttsx3 (Text → Speech)
   ↓
Final Feedback + Actionable Tips
```

---

## 📂 Repository Contents

```
📦 Interview-Practice-Partner
│
├── interview_partner.py       # Main application
├── requirements.txt           # Dependencies
├── README.md                  # Project documentation
└── .env                       # (local only — not uploaded)
```

---

## ⚙️ Setup Guide

### 1️⃣ Clone the project

```bash
git clone https://github.com/<your-username>/<repository-name>.git
cd <repository-name>
```

### 2️⃣ Create and activate a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate      # Linux / Mac
venv\Scripts\activate         # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Add your Gemini API key

Create a `.env` file in the project folder:

```
GEMINI_API_KEY=YOUR_API_KEY
```

Get the key at: [https://aistudio.google.com](https://aistudio.google.com)

### 5️⃣ Launch the Interview Agent

```bash
streamlit run interview_partner.py
```

---

## 🧪 User Flow

1️⃣ Enter your **target job role**

2️⃣ Interview begins — the **first question plays automatically**

3️⃣ User answers **using voice only**

4️⃣ Whisper transcribes → Gemini asks the next follow-up question

5️⃣ When the user says **“end interview”**, feedback is displayed automatically

---

## 🔮 Future Enhancements (Roadmap)

| Feature                            | Value                                 |
| ---------------------------------- | ------------------------------------- |
| Spoken feedback summary            | End-to-end audio experience           |
| Confidence & filler-word scoring   | Public-speaking improvement           |
| downloadable PDF report            | Useful for placement prep             |
| Resume upload → tailored interview | Personalized question difficulty      |
| Multi-interviewer modes            | HR / Hiring Manager / Technical Panel |

---

## 🛡 License

This project is intended for **learning and educational purposes**.
Forks and contributions are welcome.

---

## 🙌 Acknowledgements

* Google Gemini
* OpenAI Whisper
* Streamlit
* pyttsx3
* pydub

---

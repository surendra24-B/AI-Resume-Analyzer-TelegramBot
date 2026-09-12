# 🤖 AI Resume Analyzer Telegram Bot

An AI-powered Telegram bot that analyzes one or multiple resumes against a given Job Description and provides an ATS/Job Compatibility Score, skill-gap analysis, candidate ranking, resume improvement suggestions, and personalized course recommendations.

The project combines **Python, Telegram Bot API, deterministic ATS logic, and Google Gemini AI** to automate resume screening and candidate comparison.

---

## 🚀 Features

### 📄 Resume Analysis

- Upload resumes in **PDF, DOCX, or TXT** format.
- Extract resume text automatically.
- Analyze resumes against a given Job Description.
- Supports analyzing **multiple resumes in a single session**.

### 📊 ATS / Compatibility Analysis

The system evaluates resumes based on:

- Skill matching
- Job-description keywords
- Experience relevance
- Education match
- Resume quality

### 🔍 Skill Gap Analysis

Identifies:

- ✅ Matched skills
- ❌ Missing skills
- 📌 Required skills
- 📈 Areas where the candidate can improve

### 🤖 AI-Powered Analysis

Google Gemini analyzes the resume and provides:

- Candidate summary
- Strengths
- Weaknesses
- Experience gaps
- Education match
- Resume improvement suggestions
- Recommended learning courses

### 🏆 Candidate Ranking

When multiple resumes are uploaded, candidates are automatically ranked according to their compatibility score.

Example:

```text
🏆 CANDIDATE RANKING

🥇 candidate3.pdf
📊 ATS Score: 86.5%

🥈 candidate1.pdf
📊 ATS Score: 81.2%

🥉 candidate4.pdf
📊 ATS Score: 76.8%

4. candidate2.pdf
📊 ATS Score: 69.4%
````

### 🔐 Temporary File Handling

Uploaded resumes are temporarily stored for processing and automatically deleted after analysis.

---

# 🏗️ System Architecture

```text
                    ┌──────────────────┐
                    │   Telegram User  │
                    └────────┬─────────┘
                             │
                             ▼
                 ┌──────────────────────┐
                 │   Telegram Bot       │
                 │ python-telegram-bot  │
                 └──────────┬───────────┘
                            │
                Job Description + Resumes
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Resume Text Extractor│
                 │   PDF / DOCX / TXT   │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │    ATS Engine        │
                 │                      │
                 │ • Skill Matching     │
                 │ • Keyword Matching   │
                 │ • Score Calculation  │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │    Gemini AI         │
                 │  Gemini 3.6 Flash    │
                 │                      │
                 │ • Resume Analysis    │
                 │ • Skill Gaps         │
                 │ • Improvements       │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Candidate Ranking    │
                 │                      │
                 │ 🥇 Candidate 1       │
                 │ 🥈 Candidate 2       │
                 │ 🥉 Candidate 3       │
                 └──────────┬───────────┘
                            │
                            ▼
                    ┌─────────────────┐
                    │ Telegram Result │
                    └─────────────────┘
```

---

# 🛠️ Tech Stack

| Technology          | Purpose                         |
| ------------------- | ------------------------------- |
| Python              | Core programming language       |
| Flask               | Web application backend         |
| Google Gemini       | AI-powered resume analysis      |
| python-telegram-bot | Telegram bot integration        |
| PyPDF               | PDF text extraction             |
| python-docx         | DOCX text extraction            |
| Scikit-learn        | Machine learning utilities      |
| Requests            | HTTP/API communication          |
| python-dotenv       | Environment variable management |

---

# 📁 Project Structure

```text
resume-ai-chatbot/
│
├── app.py
├── config.py
├── requirements.txt
├── .env
│
├── services/
│   ├── __init__.py
│   ├── extractor.py
│   ├── ats_engine.py
│   ├── analyzer.py
│   ├── course_recommender.py
│   └── chatbot.py
│
├── integrations/
│   ├── __init__.py
│   ├── telegram_bot.py
│   └── whatsapp.py
│
├── templates/
│   └── index.html
│
├── static/
│   └── style.css
│
└── uploads/
```

---

# ⚙️ How It Works

## Step 1 — Send Job Description

The user sends the Job Description to the Telegram bot.

```text
User
 ↓
/start
 ↓
Job Description
```

---

## Step 2 — Upload Resumes

The user can upload multiple resumes.

```text
Resume 1
Resume 2
Resume 3
Resume 4
...
```

The bot supports up to **10 resumes per analysis session**.

---

## Step 3 — Start Analysis

After uploading all resumes, the user sends:

```text
/analyze
```

The bot then:

1. Extracts text from each resume.
2. Extracts relevant skills.
3. Compares resume skills with the Job Description.
4. Calculates compatibility scores.
5. Sends resume content to Gemini for semantic analysis.
6. Generates recommendations.
7. Ranks candidates.
8. Returns the results through Telegram.

---

# 📊 ATS Scoring

The current compatibility score uses a weighted scoring approach:

```text
Skill Match       → 40%
Experience        → 25%
Education         → 15%
Keyword Match     → 10%
Resume Quality    → 10%
```

Formula:

```text
ATS Score =
    Skill Score × 0.40
  + Experience Score × 0.25
  + Education Score × 0.15
  + Keyword Score × 0.10
  + Resume Quality × 0.10
```

> **Note:** The score is an application-specific resume–job compatibility score and is not intended to exactly reproduce the proprietary scoring of commercial ATS platforms.

---

# 🤖 AI Analysis

Gemini AI receives the Job Description and extracted resume text.

The AI is instructed to:

* Use only information available in the resume.
* Avoid inventing candidate information.
* Identify genuine skill gaps.
* Analyze the candidate's strengths and weaknesses.
* Provide actionable resume improvements.
* Recommend relevant learning areas.

Example output:

```text
Candidate Summary:
Strong Python developer with practical machine learning experience.

Strengths:
• Python
• Machine Learning
• SQL
• Flask
• Pandas

Missing Skills:
• Docker
• AWS
• LangChain

Resume Improvements:
• Add measurable project outcomes.
• Highlight REST API development.
• Include relevant AI/ML technologies.
```

---

# 📚 Course Recommendation

The system recommends learning areas based on missing skills.

For example:

```text
Missing Skill → Recommended Learning

Python
→ Python Programming Fundamentals

SQL
→ SQL Fundamentals

Docker
→ Docker Fundamentals

AWS
→ AWS Cloud Fundamentals

Machine Learning
→ Machine Learning Fundamentals
```

---

# 📱 Telegram Bot Commands

| Command    | Description                  |
| ---------- | ---------------------------- |
| `/start`   | Start a new analysis session |
| `/help`    | Display instructions         |
| `/analyze` | Analyze all uploaded resumes |
| `/cancel`  | Cancel the current session   |

---

# 🔑 Environment Variables

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=your_gemini_api_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
```

Optional WhatsApp configuration:

```env
WHATSAPP_TOKEN=your_whatsapp_token
WHATSAPP_PHONE_ID=your_whatsapp_phone_id
```

> **Important:** Never commit your `.env` file or API keys to GitHub.

Add this to `.gitignore`:

```text
.env
__pycache__/
*.pyc
uploads/
```

---

# 📦 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/your-username/ai-resume-analyzer-telegram-bot.git
```

Move into the project directory:

```bash
cd ai-resume-analyzer-telegram-bot
```

---

## 2. Install Dependencies

```bash
py -m pip install -r requirements.txt
```

If `google-genai` is not installed:

```bash
py -m pip install -U google-genai
```

---

# 🔐 Configure Gemini API

Create a Gemini API key and add it to `.env`:

```env
GEMINI_API_KEY=your_api_key
```

The application uses:

```text
Gemini 3.6 Flash
```

for AI-powered resume analysis.

---

# 🤖 Configure Telegram Bot

Create a Telegram bot using **BotFather** and obtain the bot token.

Add the token to `.env`:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
```

---

# ▶️ Run the Telegram Bot

From the project root:

```bash
py -m integrations.telegram_bot
```

You should see:

```text
🤖 AI Resume Telegram Bot is running...
📄 Maximum resumes: 10
Press Ctrl+C to stop.
```

---

# 🧪 Example Usage

Start the bot:

```text
/start
```

Send:

```text
Job Description
```

Upload multiple resumes:

```text
candidate1.pdf
candidate2.pdf
candidate3.docx
candidate4.pdf
```

Then:

```text
/analyze
```

The bot returns:

```text
🏆 CANDIDATE RANKING

🥇 candidate3.pdf
ATS Score: 87%

🥈 candidate1.pdf
ATS Score: 82%

🥉 candidate4.pdf
ATS Score: 75%

4. candidate2.pdf
ATS Score: 68%
```

Detailed analysis is then provided for each candidate.

---

# 🎯 Use Cases

This project can be used for:

* 👨‍💼 Recruiter candidate screening
* 🏢 HR resume filtering
* 🎓 College placement preparation
* 💼 Job application analysis
* 🧑‍💻 Technical hiring
* 🏆 Hackathon demonstrations
* 📄 Resume improvement
* 📚 Skill-gap identification

---

# 🔮 Future Improvements

* [ ] WhatsApp integration
* [ ] Web dashboard for recruiters
* [ ] Database for candidate history
* [ ] Advanced NLP-based skill extraction
* [ ] Required vs. preferred skill classification
* [ ] Experience scoring based on actual resume data
* [ ] Education scoring based on Job Description requirements
* [ ] Skill aliases and semantic matching
* [ ] Resume ranking dashboard
* [ ] Candidate comparison charts
* [ ] Confidence scores
* [ ] Better course recommendations
* [ ] OCR support for scanned resumes
* [ ] Authentication and role-based access
* [ ] Rate limiting and production security
* [ ] Automated testing
* [ ] Redis/PostgreSQL for scalable session management

---

# ⚠️ Limitations

The current version is designed primarily as a **hackathon/MVP project**.

Some limitations include:

* Skill extraction currently uses a predefined skill dictionary.
* Keyword matching is relatively simple.
* Some scoring components can use default values.
* Gemini availability and API limits can affect AI analysis.
* Telegram session data is maintained temporarily.
* The system should not be used as the sole decision-maker for real-world hiring.

Human review should always be used for final recruitment decisions.

---

# 🔒 Privacy & Security

The system is designed to minimize storage of uploaded resumes.

* Resumes are temporarily stored for processing.
* Files are deleted after analysis.
* API keys are stored in environment variables.
* `.env` should never be committed to GitHub.
* Resume information should be treated as sensitive data.

---

# 🏆 Hackathon Highlights

This project demonstrates:

```text
✅ Artificial Intelligence
✅ Generative AI
✅ Natural Language Processing
✅ Resume Parsing
✅ ATS Scoring
✅ Skill Gap Analysis
✅ Candidate Ranking
✅ Telegram Bot Development
✅ Multi-Resume Processing
✅ API Integration
```

The main goal is to demonstrate how **Generative AI and traditional programmatic analysis can work together** to create a practical recruitment assistant.

---

# 👨‍💻 Author

**Surendra**

AI/ML & Software Development Enthusiast

---

# 📄 License

This project is intended for educational and hackathon purposes.

You can add an appropriate open-source license such as the MIT License if you plan to make the project publicly reusable.

```
```

# catallyst-synopses-scorer
A FastAPI app that scores and gives LLM-based feedback on synopsis quality vs. its article. Upload files, get a score and feedback via Together AI (LLaMA 3). Includes anonymization and basic password protection.  Run: python app.py
🛡️ GenAI Synopsis Evaluator

A privacy-conscious GenAI-powered web app that evaluates the quality of a synopsis against its source article. It uses anonymization, custom scoring, and LLM feedback from Together AI's LLaMA 3 model to generate constructive feedback for users — without exposing sensitive information.

---

🚀 Features

* 🔒 *Privacy-first*: Anonymizes uploaded text before processing
* 📊 *Custom Scoring*: Evaluates synopsis quality based on content coverage, clarity, and coherence
* 🧠 *LLM Feedback*: Uses Together AI's `LLaMA 3.3 70B` for feedback generation
* 🌐 *Web Interface*: Upload files via a simple FastAPI-based frontend
* 🔑 *Password-Protected*: Basic authentication for access

---
🧩 Project Structure

```
.
├── app.py                # FastAPI app
├── templates/
│   └── index.html        # HTML frontend
├── anonymizer.py         # Text anonymization logic
├── parser.py             # File parsing utility
├── scorer.py             # Custom evaluation logic
├── .env                  # API keys and secrets
└── requirements.txt      # Dependencies
```

---
⚙️ How It Works

1. *User Uploads Files*: An article and its synopsis (PDF, DOCX, or TXT)
2. *Text Processing*: The files are parsed and anonymized
3. *Scoring*: A custom evaluation score is computed
4. *LLM Feedback*: Together AI’s LLaMA 3 model provides 2–3 sentence feedback
5. *Results Displayed*: Score and feedback are shown on the webpage

---

🧪 Installation
1. Clone the repository
```bash
git clone https://github.com/Dipak703/catallyst-synopses-scorer.git
cd catallyst-synopses-scorer
```

2. Set up the environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Add your `.env` file
Create a `.env` file in the root directory with:
```env
TOGETHER_API_KEY=your_together_api_key
```
---

🧷 Running the App
```bash
python app.py
```
App will be live at: `https://dialumin.com/api/remote`
---

🔐 Default Access Password
To access the evaluation page, enter:

```text
1234
```

---
📦 Dependencies

* `fastapi`
* `jinja2`
* `python-dotenv`
* `uvicorn`
* `together`
* `anonymizer`, `parser`, `scorer` – custom modules

Install all using:
```bash
pip install -r requirements.txt
```
---
📁 File Support
Supports:
* `.txt`
* `.pdf`
Make sure your `parser.py` handles these formats correctly.
---
📌 Notes
* This project is for **evaluation and learning** purposes.
* Do not upload any personally identifiable or sensitive information.
* Together AI’s free LLaMA 3 model is used under their platform's limitations.
---

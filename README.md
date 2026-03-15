# 🛡️ ML Auditor Pro

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Interface-Streamlit-red?logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![AI Powered](https://img.shields.io/badge/AI_Powered-OpenAI-black)

**ML Auditor Pro** is an open-source static analysis tool designed to detect silent, critical bugs in Machine Learning code **before they reach production**.

Traditional linters check syntax.  
**ML Auditor Pro checks machine learning logic.**

It identifies issues such as:

- Data Leakage
- Metric Misuse
- Missing Reproducibility Settings
- Poor ML experiment practices

Think of it as a **"Linter for Machine Learning Pipelines."**

---

# 🌟 Key Features

### 📁 Flexible Input
Upload either:

- Python scripts (`.py`)
- Jupyter Notebooks (`.ipynb`)

---

### 🧠 Hybrid AI Engine

**Offline Mode (Default)**  
- Static code analysis using AST
- Detects ML logic bugs instantly
- No API key required

**Online Mode (Optional)**  
- Connect an OpenAI API key
- Get AI-generated explanations and code fixes

---

### 🔍 Smart Bug Detection

ML Auditor Pro currently detects:

- **Data Leakage**
  - Example: `StandardScaler.fit()` before `train_test_split`

- **Reproducibility Issues**
  - Missing `random_state` in ML models or dataset splits

- **Metric Misuse**
  - Example: Using `accuracy` on imbalanced datasets

---

### 🤖 AI Assistant

The integrated **AI ASSIST** chatbot can:

- Explain ML errors
- Summarize audit results
- Suggest code improvements
- Provide ML engineering guidance

---

### 📊 PDF Audit Reports

Generate professional reports containing:

- Audit Score
- Issue descriptions
- Code snippets
- Recommended fixes

Perfect for:

- Documentation
- Academic submissions
- ML project reviews

---

### 💎 Modern UI

Built with **Streamlit** and designed with a clean **dark theme dashboard**.

---

# 🛠️ Tech Stack

**Frontend**
- Streamlit

**Backend**
- Python
- AST-based static analysis

**AI Integration**
- OpenAI GPT API

**Reporting**
- FPDF

---

# 📋 How to Use

1️⃣ Go to the **Auditor Tool**

2️⃣ Upload your `.py` or `.ipynb` file

3️⃣ Click **Run Audit**

4️⃣ Review the **Health Score** and detected issues

5️⃣ Use **AI ASSIST** for explanations or help fixing the bugs

6️⃣ Download the **PDF audit report**

---

# ⚙️ Configuration (Optional)

The application works fully in **offline mode**.

To enable **AI generated fixes**, you can add an OpenAI API key.

---

## Option A — Running Locally

Create a `.env` file:

```

OPENAI_API_KEY="your-api-key"

````

---

## Option B — Streamlit Cloud Deployment

If you deploy the app on Streamlit Cloud:

1. Go to **App Settings**
2. Open **Secrets**
3. Add:

```toml
OPENAI_API_KEY = "your-api-key"
````

---

# 🏃 Running the Project Locally

### 1️⃣ Clone the repository

```bash
git clone https://github.com/DilaknaH/ml-auditor.git
cd ml-auditor
```

---

### 2️⃣ Create a virtual environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux**

```bash
python -m venv venv
source venv/bin/activate
```

---

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Run the application

```bash
streamlit run app.py
```

The app will open in your browser.

---

# 📁 Project Structure

```
ml-auditor/
│
├── app.py
├── requirements.txt
├── README.md
│
├── ml_auditor/
│   │
│   ├── engine.py
│   ├── reporter.py
│   │
│   ├── checkers/
│   │   ├── leakage.py
│   │   ├── reproducibility.py
│   │   └── metrics.py
│   │
│   └── llm/
│       ├── explainer.py
│       └── chatbot.py
│
├── tests/
│   └── sample_notebooks/
│
└── .github/
    └── workflows/
        └── ml-audit.yml
```

---

# 📄 License

This project is licensed under the **MIT License**.

---

# 🙏 Acknowledgements

Built with:

* Python
* Streamlit
* OpenAI

```




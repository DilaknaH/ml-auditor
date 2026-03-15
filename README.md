# 🛡️ ML Auditor Pro

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Interface-Streamlit-red?logo=streamlit)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![AI Powered](https://img.shields.io/badge/AI-Powered%20by%20OpenAI-black)](https://openai.com/)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-success)](https://ml-auditor-pro.streamlit.app/)

**ML Auditor Pro** is an open-source static analysis tool designed to detect silent, critical bugs in Machine Learning code **before they reach production**.

Traditional linters check syntax.
**ML Auditor Pro checks machine learning logic.**

It identifies issues such as:

* Data Leakage
* Metric Misuse
* Missing Reproducibility Settings
* Poor ML experiment practices

Think of it as a **“Linter for Machine Learning Pipelines.”**

---

# Live Application

You can try the deployed application here:

**Live Demo:**
https://ml-auditor-pro.streamlit.app/

⚠️ The deployed demo currently runs in **Offline Mode** (no OpenAI key attached).
This means **static ML bug detection works fully**, while **AI-generated fixes require users to provide their own API key**.

---

# Key Features

### Flexible Input

Upload either:

* Python scripts (`.py`)
* Jupyter Notebooks (`.ipynb`)

---

### Hybrid AI Engine

**Offline Mode (Default)**

* Static code analysis using AST
* Detects ML logic bugs instantly
* No API key required

**Online Mode (Optional)**

* Connect an OpenAI API key
* Get AI-generated explanations and code fixes

---

### Smart Bug Detection

ML Auditor Pro currently detects:

**Data Leakage**

Example:
`StandardScaler.fit()` before `train_test_split`

**Reproducibility Issues**

Missing `random_state` in ML models or dataset splits.

**Metric Misuse**

Example: using `accuracy` on imbalanced datasets.

---

### AI Assistant

The integrated **AI ASSIST** chatbot can:

* Explain ML errors
* Summarize audit results
* Suggest code improvements
* Provide ML engineering guidance

---

### PDF Audit Reports

Generate professional reports containing:

* Audit Score
* Issue descriptions
* Code snippets
* Recommended fixes

Useful for:

* Documentation
* Academic submissions
* ML project reviews

---

### Modern UI

Built with **Streamlit** and designed with a clean **dark theme dashboard**.

---

# Tech Stack

**Frontend**

* Streamlit

**Backend**

* Python
* AST-based static analysis

**AI Integration**

* OpenAI GPT API (optional)

**Reporting**

* FPDF

---

# How to Use

1️⃣ Go to the **Auditor Tool**

2️⃣ Upload your `.py` or `.ipynb` file

3️⃣ Click **Run Audit**

4️⃣ Review the **Health Score** and detected issues

5️⃣ Use **AI ASSIST** for explanations or help fixing bugs

6️⃣ Download the **PDF audit report**

---

# Configuration (Optional)

The application works fully in **Offline Mode**.

To enable **AI-generated explanations and code fixes**, an **OpenAI API key** can be provided.

---

## Option A — Running Locally

Create a `.env` file in the project root:

```
OPENAI_API_KEY="your-api-key"
```

---

## Option B — Streamlit Cloud Deployment (Optional)

If someone deploys **their own version of this project**, they can enable AI features using **Streamlit Secrets Manager**.

1. Open the **Streamlit Cloud Dashboard**
2. Click the deployed app
3. Click **Settings**
4. Open **Secrets**
5. Add the following configuration:

```toml
OPENAI_API_KEY = "sk-proj-your-real-key-here"
```

6. Click **Save**

The application will restart and AI features will be enabled.

⚠️ **Note:**
The official deployed demo of this repository **does not include a stored OpenAI key**.

---

# Running the Project Locally

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

**Mac / Linux**

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

The application will open automatically in your browser.

---

# Project Structure

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

# License

This project is licensed under the **MIT License**.

---

# Acknowledgements

Built with:

* Python
* Streamlit
* OpenAI

## Author
Dilakna Godagamage

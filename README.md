# 🧬 Cancer Biomarker Identification

An AI-powered web application designed to identify potential cancer-associated biomarkers. This project leverages a **React** frontend, a **Python (Flask + Streamlit)** backend, and a trained **machine learning model** to analyze input gene data and return relevant biomarker predictions.

---

## 📚 Table of Contents

- [🧾 Project Description](#-project-description)
- [⚙️ Tech Stack](#-tech-stack)
- [🚀 Getting Started](#-getting-started)
  - [1️⃣ Clone the Repository](#1️⃣-clone-the-repository)
  - [2️⃣ Set Up the Backend](#2️⃣-set-up-the-backend)
  - [3️⃣ Run the Frontend](#3️⃣-run-the-frontend)
  - [4️⃣ Start All Services](#4️⃣-start-all-services)
- [📦 Prerequisites](#-prerequisites)

---

## 🧾 Project Description

This application offers an intuitive interface for identifying cancer-associated biomarkers. It combines biomedical NLP techniques with deep learning models to analyze gene data and surface insights using a web interface.

---

## ⚙️ Tech Stack

- **Frontend**: React, Tailwind CSS
- **Backend**: Flask, Streamlit, Python
- **ML Models**: BioBERT, OncoKB integration
- **Other Tools**: pandas, scikit-learn, torch

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/AnishMane/Cancer-Associated-Biomarker-Identification.git
cd Cancer-Associated-Biomarker-Identification
```

---

### 2️⃣ Set Up the Backend

```bash
cd backend
python -m venv venv         # Use `python3` if needed
venv/Scripts/activate       # or `source venv/bin/activate` on macOS/Linux
pip install -r requirements.txt
```

---

### 3️⃣ Run the Frontend

```bash
cd frontend
npm install
npm run dev
```

---

### 4️⃣ Start All Services

Ensure you are in the `backend` folder and your virtual environment is activated:

```bash
# In one terminal (inside backend/)
python streamlit_app.py

# In a second terminal (inside backend/)
python inference.py

# In a third terminal (inside backend/)
python app.py
```

Your frontend should now be running on `http://localhost:5173` and backend services (APIs and Streamlit dashboard) should be active.

---

## 📦 Prerequisites

- **Node.js & npm** – [Download here](https://nodejs.org/)
- **Python 3.x & pip**
- **virtualenv** (optional but recommended)
  


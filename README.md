# Cancer Biomarker Identification Project

This project aims to identify cancer biomarkers using a Python backend (Flask API) and a React frontend, incorporating machine learning capabilities for predictions.

## Table of Contents
- [Project Description](#project-description)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Setting Up the Backend (Python and Flask)](#2-setting-up-the-backend-python-and-flask)
  - [3. Setting Up the Frontend (React)](#3-setting-up-the-frontend-react)

## Project Description

This project provides an interface for identifying potential cancer biomarkers. It uses a Python backend powered by Flask, where the machine learning models are hosted, and a React frontend that allows users to interact with the model and view results.

## Prerequisites

- **Node.js and npm** (for frontend)
- **Python 3 and pip** (for backend)
- `virtualenv` (recommended for managing Python dependencies)

## Setup Instructions

### 1. Clone the Repository

Clone the repository to your local machine and navigate into the project directory:

```bash
    git clone https://github.com/AnishMane/Cancer-Associated-Biomarker-Identification.git
    cd Cancer-Associated-Biomarker-Identification
```

### 2. Setting Up the Backend (Python and Flask)

```bash
    cd backend
    python -m venv venv   # (or `python3 -m venv venv` for Mac)
    venv/Scripts/activate  # (or `source venv\bin\activate` for Mac)
    pip install -r requirements.txt
```

### 3. Setting Up the Frontend (React)

```bash
    cd frontend
    npm install
    npm start
```

## STAR Approach

**S – Situation:**

There is a growing need for early and accurate identification of cancer biomarkers to assist in diagnosis and treatment planning. Existing tools lacked precision and scalability for complex datasets, particularly in handling diverse data types from research articles, mutation databases, and raw genetic data.

**T – Task:**

I aimed to build a modern, full-stack application for cancer biomarker identification, combining a robust Python backend with a sophisticated React frontend. The system needed to provide an intuitive user interface for data input, real-time processing, and visualization of results, while maintaining high performance and scalability.

**A – Action:**

- **Frontend Development:**
  - Built a modern React application using Vite and TypeScript for enhanced development experience
  - Implemented a responsive UI using TailwindCSS and shadcn/ui components
  - Created interactive data visualizations using Recharts
  - Integrated React Query for efficient data fetching and state management
  - Implemented form handling with React Hook Form and Zod validation
  - Added toast notifications using Sonner for better user feedback

- **Backend Implementation:**
  - Developed a Flask-based REST API for handling biomarker analysis
  - Implemented data processing pipelines for biomarker identification
  - Created secure endpoints for data submission and retrieval
  - Integrated machine learning models for biomarker prediction
  - Set up proper error handling and logging mechanisms

- **System Architecture:**
  - Implemented a clean separation between frontend and backend services
  - Used TypeScript for type safety and better code maintainability
  - Set up proper development tooling (ESLint, Prettier) for code quality
  - Implemented proper routing using React Router
  - Created reusable components for consistent UI/UX

**R – Result:**

- Successfully delivered a modern, full-stack application for cancer biomarker identification
- Created an intuitive user interface with real-time data visualization capabilities
- Implemented robust error handling and user feedback mechanisms
- Established a scalable architecture that can be easily extended
- Built a maintainable codebase with proper TypeScript integration and modern development practices
- Set up a development environment that promotes code quality and consistency
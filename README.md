# El-Maze 2026

**Automating PCB Designing with AI**

to do

---

## Features

- **to do**

---

## Tech Stack

- **Frontend:** React (Vite), JavaScript
- **Backend:** Python 3.12.7, FastAPI
- **Package Management:** `pip` (Python), `npm` (Node.js)

---

## Prerequisites

Before you begin, ensure you have the following installed on your machine:
- [Python 3.12.7](https://www.python.org/downloads/) 
- [Node.js](https://nodejs.org/) & npm

---

## Getting Started

Follow these steps to set up the project locally.

### 1. Clone the Repository

```bash
git clone [https://github.com/attu0/Elmaze.git](https://github.com/attu0/Elmaze.git)
cd Elmaze
```

### 2. Backend Setup
Navigate to the backend folder and create a virtual environment to manage dependencies.

```bash
cd backend
```
Create Virtual Environment:

Windows:
```bash
python -m venv venv
```

macOS/Linux:

```bash
python3 -m venv venv
```

Activate Virtual Environment:

Windows:

```bash
.\venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

Install Dependencies:

```bash
pip install -r requirements.txt
```

### 3. Frontend Setup
Open a new terminal, navigate to the frontend folder, and install the required packages.

```bash
cd ../frontend
npm install
```

## Usage
To run the application, you will need two terminal windows open.

Terminal 1: Start the Backend Server

```bash
cd backend
# Ensure venv is active
uvicorn main:app --reload
```
The API will be available at http://localhost:8000

Terminal 2: Start the Frontend Client

```bash
cd frontend
npm run dev
```
The UI will be available at http://localhost:5173

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.
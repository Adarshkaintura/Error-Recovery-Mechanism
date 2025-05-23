# 🔧 Compiler Error Recovery Simulator

A simple web-based simulator built using **Flask** and **HTML** to demonstrate **error recovery mechanisms** used by compilers during the syntax analysis phase. This tool is designed to help learners visualize how compilers detect and recover from syntax errors.

---

## 🚀 Features

- Simulates **panic mode** and **phrase level** error recovery.
- Web-based UI built with HTML forms.
- Displays parse errors and how the system responds to them.
- Helps understand concepts from the syntax analysis phase of a compiler.

---

## 🛠 Tech Stack

- **Backend**: Python (Flask)
- **Frontend**: HTML, CSS (optional)

---

## 📁 Project Structure

- error_recovery_simulator/
- ├── main.py # Flask backend handling routes and logic
- ├── templates/
- │ └── index.html # Main frontend file
- ├── static/
- │ └── style.css # (Optional) CSS styles
- └── README.md


---

## 🧪 How to Run Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/error-recovery-simulator.git
   cd error-recovery-simulator
pip install flask
python main.py
Open your browser and go to http://127.0.0.1:5000/

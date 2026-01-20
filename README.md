# DS_Assignment1  
### Multi-Criteria Decision Making using TOPSIS (Python, Package, and Web Service)

This repository contains **Assignment–1** for the Data Science course.  
The assignment is divided into **three parts**, all based on implementing and deploying the **TOPSIS (Technique for Order Preference by Similarity to Ideal Solution)** method.

---

## 📌 Overview of TOPSIS

TOPSIS is a **Multi-Criteria Decision Making (MCDM)** technique used to rank alternatives based on their distance from an **ideal best** and an **ideal worst** solution.

---

## 📂 Repository Structure

DS_Assignment1/
│
├── Part1/
│ └── TOPSIS command-line implementation
│
├── Topsis-Tanishak-102303398/
│ └── Python package uploaded to PyPI
│
├── Topsis_Web/
│ └── Streamlit-based TOPSIS web service
│
└── README.md

yaml
Copy code

---

## 🧩 Part 1: Command-Line TOPSIS Implementation

### ✔ Description
A Python program implementing TOPSIS that runs via the **command line**.

### ✔ Features
- Accepts input CSV file
- Accepts weights and impacts as command-line arguments
- Performs input validation
- Computes TOPSIS score and rank
- Generates output CSV file

### ✔ Usage
```bash
python topsis.py <input.csv> <weights> <impacts> <output.csv>
✔ Example
bash
Copy code
python topsis.py data.csv "1,1,1,2,1" "+,+,+,+,+" result.csv
📦 Part 2: Python Package Development & PyPI Upload
✔ Description
The TOPSIS implementation was converted into a reusable Python package and uploaded to PyPI.

✔ Package Name
Copy code
Topsis-Tanishak-102303398
✔ PyPI Link
👉 https://pypi.org/project/Topsis-Tanishak-102303398/0.0.1/

✔ Installation
bash
Copy code
pip install Topsis-Tanishak-102303398
✔ Command-Line Usage (after installation)
bash
Copy code
topsis data.csv "1,1,1,2,1" "+,+,+,+,+" output.csv
✔ Technologies Used
setuptools

wheel

twine



🌐 Part 3: TOPSIS Web Service (Streamlit)
✔ Description
A web-based TOPSIS service built using Streamlit, allowing users to compute TOPSIS results through a browser interface.

✔ Features
Upload CSV file

Input weights and impacts

Input email ID

Input validation (weights, impacts, email format)

TOPSIS computation

Downloadable result file

Clean and interactive UI

✔ Run the Web App Locally
bash
Copy code
streamlit run app.py
✔ Technologies Used
Streamlit

Pandas

NumPy

🛠 Requirements
Common dependencies:

txt
Copy code
pandas
numpy
streamlit
🎯 Learning Outcomes
Implemented TOPSIS from scratch

Built a command-line data science tool

Created and published a Python package on PyPI

Developed a browser-based data science web service

Learned Python packaging and deployment workflow

👨‍💻 Author
Name: Tanishak
Roll Number: 102303398

📄 License
This project is developed for academic purposes only.









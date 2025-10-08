# 🧠 Textual Metrics Web App (WIP)
A Django-based web interface for evaluating the similarity between two text scripts using various metrics 
(e.g., BLEU, CodeBLEU, ROUGE, and others).
Originally developed as a Python project, now extended into a modular web application. <br>
This web application builds upon my earlier Textual Test Proxy project, which explored the use of textual-similarity 
metrics and machine learning to evaluate the quality of AI-generated code.
___

## 🚀 Features
- Compare two scripts (reference vs. generated variant)
- Measure one or multiple textual metrics
- Keep record of recent comparisons
- Clean, modular structure using Django templates and static files
___

## 🧩 Project Structure
```angular2html
text_site/                  → Main Django project folder
metrics/                    → Core app handling logic and UI
    ├─ analysis.py          → Metric computation logic
    ├─ views.py             → Handles user input and output
    ├─ templates/
    │   ├─ base.html
    │   └─ metrics/form.html
    ├─ static/
    │   ├─ metrics/css/style.css
    │   └─ metrics/js/script.js
    └─ models.py            → Stores comparison results

```
___

⚙️ Installation

```
# Clone repository
git clone git@github.com:sergiu-mocanu/text-metric-web.git
cd text-metric-web

# (Optional) Create and activate environment
conda create -n metrics_env python=3.11 pip
conda activate metrics_env

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Run server
python manage.py runserver --noreload
```
___

## 💡 Usage
1. Open your browser at `http://127.0.0.1:8000/metrics/`
2. Paste your reference and AI-generated scripts
3. Select one or more metrics
4. View the computed similarity scores and recent results

⚠️ Note: in the current app implementation, CodeBLEU metric works only with __Python__ scripts
___

## ⚖️ License
This project is licensed under the MIT License

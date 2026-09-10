# Biosimilar Legitimacy Dashboard

A simple, presentation-ready project for evaluating the scientific and regulatory legitimacy of a biosimilar product.

This app compares a candidate biosimilar against the originator biologic and similar biologics using a synthetic dataset focused on:
- product quality
- analytical comparability
- safety and side effects
- efficacy alignment
- regulatory status and interchangeability
- overall legitimacy score

This is not a commercial launch simulator. It is a biosimilar evaluation dashboard built to assess credibility, quality, and safety.

## Project purpose

The dashboard helps answer questions like:
- Is the biosimilar scientifically comparable to the reference product?
- Is the safety profile acceptable?
- Is the product likely to be considered legitimate based on quality and regulatory evidence?
- How does it compare with originator biologics and other similar biologics?

## Files included

The project keeps only the necessary files for running and presenting the dashboard:

- `app.py` – Streamlit dashboard
- `requirements.txt` – Python dependencies
- `execute.txt` – quick setup and run instructions
- `src/data/generate_legitimacy_dataset.py` – synthetic dataset generator
- `data/raw/biosimilar_legitimacy_dataset.csv` – generated raw dataset
- `outputs/` – dashboard-ready summary files

## Folder structure

```text
usecase2/
├── app.py
├── README.md
├── execute.txt
├── requirements.txt
├── .gitignore
├── data/
│   └── raw/
│       └── biosimilar_legitimacy_dataset.csv
├── outputs/
│   ├── biosimilar_legitimacy_dataset.csv
│   ├── comparability_summary.csv
│   ├── safety_summary.csv
│   ├── regulatory_legitimacy.csv
│   └── biologic_comparison.csv
└── src/
    └── data/
        └── generate_legitimacy_dataset.py
```

## Setup

1. Open PowerShell in the project folder.
2. Create a virtual environment:

```bash
python -m venv .venv
```

3. If PowerShell blocks script execution, run this once in the current terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

4. Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

If you prefer Command Prompt instead of PowerShell:

```cmd
.\.venv\Scripts\activate.bat
```

5. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

6. Generate the dataset:

```bash
python src/data/generate_legitimacy_dataset.py
```

7. Run the dashboard:

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal, usually:

```text
http://localhost:8501
```

## Dashboard views

The app includes:
- overview of legitimacy and quality scores
- safety and side-effect comparison
- regulatory legitimacy and interchangeability
- comparison with originator and peer biologics

## Data note

This project uses synthetic data for demonstration and presentation purposes. It is designed to help explain biosimilar evaluation logic and dashboard structure clearly.

## Quick note for GitHub

This folder is cleaned and organized for simple drag-and-drop upload to GitHub. It contains only the files needed to run and present the biosimilar legitimacy dashboard.

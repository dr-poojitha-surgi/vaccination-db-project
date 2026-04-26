# VaccinationDB — Multi-Facility EHR Integration Dashboard

**Group 5 · IU Indianapolis · Scientific & Clinical Data Management SP26**

## Project Overview

A relational database system that integrates patient, encounter, and immunization data across 3 simulated healthcare organizations (Indiana · Illinois · Ohio) using Synthea synthetic data. The system identifies patients who were eligible for vaccines based on CDC ACIP 2025 guidelines but did not receive them during clinical encounters.

## Live App

> Deployed on Streamlit Community Cloud

## Pages

| Page | Description |
|---|---|
| 🏠 Overview | KPI cards — patients, encounters, immunizations, organizations |
| 📊 Coverage Analysis | CDC-based coverage % by vaccine and hospital system |
| 🔍 Patient Lookup | Search any patient — immunization history, encounters, missing vaccines |
| ⚠️ CDC Gap Analysis | Missed vaccination opportunities using MissedVaccinations VIEW |
| 🏥 Providers & Orgs | Provider and organization-level vaccination activity |
| 📋 Vaccine Guidelines | CDC ACIP 2025 adult vaccine reference + age window chart |
| 📈 Tableau Dashboard | Embedded Tableau Public interactive dashboard |
| 🗄️ SQL Query Runner | Live SQL editor with preset queries + CSV export |

## Tech Stack

- **Database**: MySQL 9.x — 7 tables, 330 patients, 16,444 encounters, 4,955 immunizations
- **Backend**: Python + Streamlit
- **Visualization**: Plotly (in-app) + Tableau Public (embedded)
- **Data**: Synthea synthetic EHR data — Indiana, Illinois, Ohio
- **Guidelines**: CDC ACIP Adult Combined Schedule 2025

## Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/vaccination-db-project
cd vaccination-db-project
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure your database connection
Open `app.py` and update line ~45:
```python
password="your_password_here",   # ← your MySQL password
```

### 4. Make sure your MySQL database is running
Import `vaccination_db_COMPLETE.sql` into MySQL Workbench if not done already.

### 5. Run the app
```bash
streamlit run app.py
```
Opens at `http://localhost:8501`

## Database Schema

```
Patients ──────────┐
Organizations ──┐  ├── Encounters ──── Immunizations
Providers ──────┘  │                        │
                   └────────────────── Vaccines
                                            │
                                   VaccineGuidelines
```

## Key SQL Objects

- `MissedVaccinations` VIEW — core analytical object identifying encounter-level gaps
- CDC ACIP 2025 guidelines loaded in `VaccineGuidelines` table (8 adult vaccine rules)

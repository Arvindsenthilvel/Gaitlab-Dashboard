# GaitLab Dashboard

An interactive multimodal gait analysis dashboard built with Streamlit, visualising the effects of smartphone use on human walking biomechanics.

> **Study:** Single-task vs Dual-task (Smartphone) Gait Analysis  
> **Institution:** SRMIST, KTR · CAMERA LAB  
> **Authors:** Arvind, Dr. Varshini Karthik  
> **Participants:** N = 25 healthy young adult males, Age 18–25

---

## 📋 Table of Contents

- [About the Study](#about-the-study)
- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Deployment on Streamlit Cloud](#deployment-on-streamlit-cloud)
- [Known Issues & Fix](#known-issues--fix)
- [Data Description](#data-description)
- [Key Findings](#key-findings)
- [Tech Stack](#tech-stack)

---

## About the Study

This dashboard presents results from a biomechanics study comparing normal walking (control) against walking while using a smartphone (dual-task). Gait was recorded using:

- **Qualisys** — 3D motion capture (kinematics)
- **Bertec** — Force plates (kinetics)
- **Delsys** — EMG (muscle activation)

Statistical analysis was performed in **Jamovi** (α = 0.05) using Wilcoxon signed-rank tests and paired t-tests depending on normality (Shapiro-Wilk).

---

## Features

The dashboard has 10 pages accessible from the sidebar:

| Page | Description |
|------|-------------|
| **Overview** | Summary metrics and significant findings at a glance |
| **Subjects** | Demographic info for all 25 anonymised participants |
| **Spatiotemporal** | Walking speed, cadence, stride length, double support, variability |
| **Kinematic** | Hip, knee, and ankle joint angles |
| **Kinetic** | Braking and propulsion impulse from force plate data |
| **EMG** | Gastrocnemius RMS activation (n=13 with EMG data) |
| **Statistics** | Full statistical results table with effect sizes and p-values |
| **Charts** | Interactive Plotly charts comparing control vs smartphone |
| **Raw Data** | Filterable table with CSV download |
| **Key Inferences** | Novel findings and PPT-ready slide bullets |

---

## Project Structure

```
gaitlab-dashboard/
│
├── app.py                  # Main Streamlit application
├── subjects_data.json      # Anonymised participant data (N=25)
└── README.md               # This file
```

---

## Getting Started

### Prerequisites

- Python 3.9 or higher (tested up to 3.13)
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/gaitlab-dashboard.git
cd gaitlab-dashboard

# Install dependencies
pip install streamlit pandas numpy plotly
```

### Run Locally

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## Deployment on Streamlit Cloud

1. Push this repo to GitHub (ensure both `app.py` and `subjects_data.json` are in the root).
2. Go to [share.streamlit.io](https://share.streamlit.io) and click **New app**.
3. Select your repo, branch, and set the main file path to `app.py`.
4. Click **Deploy**.

### Required files in root of repo

```
app.py
subjects_data.json
```

---

## Known Issues & Fix

### NameError on Streamlit Cloud (Python 3.14)

**Error:**
```
NameError at app.py line 72 inside load_data()
```

**Cause:** The original `load_data()` function contained an inline Python list literal with JSON `null` values. `null` is not valid Python — Python uses `None`. This raises a `NameError` on newer Python versions.

**Fix applied:** Replace the hardcoded inline data with a JSON file load:

```python
# In app.py, lines 71–72 — replace load_data() with:
@st.cache_data
def load_data():
    with open("subjects_data.json", "r") as f:
        return json.load(f)
```

Make sure `subjects_data.json` is present in the same directory as `app.py`. The `json` module is already imported in the app.

---

## Data Description

All participants are anonymised as Subject 1–25. Each subject has the following fields in `subjects_data.json`:

| Field | Description | Unit |
|-------|-------------|------|
| `age`, `height`, `weight` | Demographics | years, cm, kg |
| `Walking_speed_ctrl/smart` | Walking speed | m/s |
| `Cadence_ctrl/smart` | Steps per minute | spm |
| `Stride_length_ctrl/smart` | Stride length | m |
| `Double_support_ctrl/smart` | Double support time | % |
| `Stride_variability_ctrl/smart` | Stride variability | % |
| `Peak_hip/knee_flexion_ctrl/smart` | Peak joint angles | degrees |
| `Peak_ankle_df_ctrl/smart` | Peak ankle dorsiflexion | degrees |
| `Braking_impulse_ctrl/smart` | Braking ground reaction force impulse | N·s |
| `Propulsion_impulse_ctrl/smart` | Propulsion ground reaction force impulse | N·s |
| `EMG_RMS_ctrl/smart` | Gastrocnemius RMS activation (n=13 only) | mV |

`null` values in the JSON indicate missing data (EMG was only collected for 13 of 25 subjects).

---

## Key Findings

- **Walking speed ↓ 16.4%** (p < 0.001, RBC = 0.991 — near-perfect effect size)
- **Stride length ↓ 12.1%** (Cohen's d = 1.398 — Huge effect)
- **Double support ↑ 34.6%** and **stride variability ↑ 62.9%** — conservative fall-avoidance gait
- **Ankle dorsiflexion ↑ 8.1%** despite slower speed — novel distal CNS compensation
- **Propulsion impulse ↓ 18.2%** — mechanical explanation for speed loss
- **Net impulse sign reversal**: Control = +0.9 N·s (propulsive) → Smartphone = −0.7 N·s (decelerative)
- **EMG ↑ 11.6% yet propulsion ↓ 18.2%** — neuromuscular inefficiency (underpowered, n=13)

---

## Tech Stack

- [Streamlit](https://streamlit.io) — Dashboard framework
- [Pandas](https://pandas.pydata.org) — Data manipulation
- [NumPy](https://numpy.org) — Numerical operations
- [Plotly](https://plotly.com/python/) — Interactive charts
- [Jamovi](https://www.jamovi.org) — Statistical analysis (offline)

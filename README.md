# Academic Performance Analytics System

A Software Engineering course-project prototype that summarizes student marks, attendance and assessment performance, shows dashboards, analyzes trends and flags students who may need academic intervention.

## Technology
- Python 3.11+
- Streamlit
- Pandas
- Plotly
- SQLite
- pytest
- GitHub Actions

## Run locally
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python seed_data.py
streamlit run app.py
```

Run tests:
```bash
pytest -q
```

## Prototype analytics assumptions
Score = 40% exam + 25% assignment + 20% attendance + 15% internal assessment.
Intervention flag: score < 50 OR attendance < 75% OR trend is Declining.
Trend: latest score is at least 10 points below/above the previous period for Declining/Improving.

These are project assumptions, not institutional policy. Replace with instructor-approved criteria if provided. The seed data is synthetic.

## Project Team

| Team Member | SRN |
|---|---|
| Saransh Mittal | PES1UG24AM254 |
| TB Akash | PES1UG24AM299 |
| Sanapala Maneesh | PES1UG24AM247 |
| Suhas MK | PES1UG24AM290 |

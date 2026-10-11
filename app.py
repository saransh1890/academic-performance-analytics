import pandas as pd
import plotly.express as px
import streamlit as st
from database import init_db, get_conn
from analytics import performance_score, trend_status, intervention_status

st.set_page_config(page_title="Academic Performance Analytics", layout="wide")
init_db()
st.title("Academic Performance Analytics System")
st.caption("Prototype using synthetic data. Risk rules are configurable project assumptions.")

with get_conn() as conn:
    students = pd.read_sql_query("SELECT * FROM students ORDER BY student_id", conn)
    records = pd.read_sql_query("""
        SELECT r.*, s.name, s.program
        FROM academic_records r JOIN students s ON s.student_id=r.student_id
    """, conn)

if students.empty or records.empty:
    st.warning("No records found. Run `python seed_data.py` and refresh.")
    st.stop()

role = st.sidebar.selectbox("Demo view", ["Faculty", "Student", "Admin"])

def summary_for(sid):
    data = records[records.student_id == sid].sort_values("period")
    latest = data.iloc[-1]
    previous = data.iloc[-2] if len(data) > 1 else None
    score = performance_score(latest.exam_score, latest.assignment_score,
                              latest.attendance_pct, latest.internal_score)
    prev_score = (performance_score(previous.exam_score, previous.assignment_score,
                 previous.attendance_pct, previous.internal_score) if previous is not None else None)
    trend = trend_status(prev_score, score)
    status, reasons = intervention_status(score, latest.attendance_pct, trend)
    return data, score, trend, status, reasons

if role == "Student":
    sid = st.sidebar.selectbox("Select demo student", students.student_id.tolist())
    data, score, trend, status, reasons = summary_for(sid)
    name = students.loc[students.student_id == sid, "name"].iloc[0]
    st.subheader(f"{name}'s Performance")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Performance score", score)
    c2.metric("Attendance", f"{data.iloc[-1].attendance_pct:.1f}%")
    c3.metric("Trend", trend)
    c4.metric("Status", status)
    if reasons:
        st.warning("Intervention reasons: " + ", ".join(reasons))
    melted = data.melt(id_vars=["period"],
        value_vars=["assignment_score","internal_score","exam_score"],
        var_name="Assessment", value_name="Score")
    st.plotly_chart(px.line(melted, x="period", y="Score", color="Assessment", markers=True),
                    use_container_width=True)
    st.dataframe(data[["period","attendance_pct","assignment_score","internal_score","exam_score"]],
                 use_container_width=True)
elif role == "Faculty":
    rows = []
    for sid in students.student_id.tolist():
        data, score, trend, status, reasons = summary_for(sid)
        rows.append({"Student": data.iloc[-1]["name"], "Score": score,
                     "Attendance": data.iloc[-1].attendance_pct, "Trend": trend,
                     "Status": status, "Reasons": ", ".join(reasons)})
    df = pd.DataFrame(rows)
    c1,c2,c3 = st.columns(3)
    c1.metric("Students", len(df))
    c2.metric("Needs intervention", int((df.Status == "Needs Intervention").sum()))
    c3.metric("Average score", round(df.Score.mean(), 2))
    st.dataframe(df, use_container_width=True)
    st.plotly_chart(px.bar(df, x="Student", y="Score", color="Status"), use_container_width=True)
else:
    st.subheader("Admin overview")
    st.metric("Students", len(students))
    st.metric("Academic records", len(records))
    st.dataframe(students, use_container_width=True)

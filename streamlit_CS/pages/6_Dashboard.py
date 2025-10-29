import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Page configuration
st.set_page_config(page_title="Student Performance Dashboard", layout="wide")

# Title
st.title("Student Performance Factors")

# Generate sample data for demonstration
np.random.seed(42)
n_students = 100
data = pd.DataFrame({
    'hours_studied': np.random.randint(1, 10, n_students),
    'exam_score': np.random.randint(50, 100, n_students),
    'activity_level': np.random.randint(1, 6, n_students),
    'sleep_hours': np.random.randint(4, 10, n_students)
})

# Add some correlation
data['exam_score'] = data['hours_studied'] * 5 + np.random.randint(-10, 10, n_students)
data['exam_score'] = data['exam_score'].clip(50, 100)

st.divider()
# ROW 1: 
col1_r1, col2_r1 = st.columns([2, 1])

with col1_r1:
    st.subheader("Hours Studied Vs Exam Score")
    st.caption("Scatter plot + trendline")

with col2_r1:
    st.subheader("Heading")
    st.write("Big Copy")

st.divider()
# ROW 2:
col1_r2, col2_r2, col3_r2 = st.columns(3)

with col1_r2:
    st.subheader("Activity Vs Exam Score Heatmap")

with col2_r2:
    st.subheader("Heading")
    st.write("Big Copy")

with col3_r2:
    st.subheader("Sleep Vs Exam Score Heatmap")
    st.write("Big Copy")

st.divider()
# ROW 3:
col1_r3, col2_r3 = st.columns([1, 2])

with col1_r3:
    st.subheader("Heading")
    st.write("Big Copy")

with col2_r3:
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    with btn_col1:
        st.write("Big Copy")
    
    with btn_col2:
        st.write("Big Copy")
    
    with btn_col3:
        st.write("Big Copy")

# Footer
st.divider()
st.caption("Data source")

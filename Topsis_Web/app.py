import streamlit as st
import pandas as pd
import numpy as np
import os
import re

# Create folders if not present
os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

st.title("TOPSIS Web Service")

# ---------------------------
# INPUT FORM
# ---------------------------
uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
weights_input = st.text_input("Weights (comma separated)", "1,1,1,1")
impacts_input = st.text_input("Impacts (comma separated)", "+,+,+,+")
email = st.text_input("Email ID")

submit = st.button("Submit")

# ---------------------------
# VALIDATION & PROCESSING
# ---------------------------
if submit:
    # Email validation
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        st.error("Invalid Email ID")
        st.stop()

    if uploaded_file is None:
        st.error("Please upload a CSV file")
        st.stop()

    try:
        df = pd.read_csv(uploaded_file)
    except:
        st.error("Invalid CSV file")
        st.stop()

    if df.shape[1] < 3:
        st.error("CSV must contain at least 3 columns")
        st.stop()

    data = df.iloc[:, 1:]

    if not np.all(data.map(lambda x: isinstance(x, (int, float)))):
        st.error("All criteria values must be numeric")
        st.stop()

    weights = list(map(float, weights_input.split(",")))
    impacts = impacts_input.split(",")

    if len(weights) != data.shape[1] or len(impacts) != data.shape[1]:
        st.error("Number of weights and impacts must match number of criteria")
        st.stop()

    for i in impacts:
        if i not in ['+', '-']:
            st.error("Impacts must be + or -")
            st.stop()

    # ---------------------------
    # TOPSIS CALCULATION
    # ---------------------------
    norm = data / np.sqrt((data ** 2).sum())
    weighted = norm * weights

    ideal_best = []
    ideal_worst = []

    for i in range(len(impacts)):
        if impacts[i] == '+':
            ideal_best.append(weighted.iloc[:, i].max())
            ideal_worst.append(weighted.iloc[:, i].min())
        else:
            ideal_best.append(weighted.iloc[:, i].min())
            ideal_worst.append(weighted.iloc[:, i].max())

    dist_best = np.sqrt(((weighted - ideal_best) ** 2).sum(axis=1))
    dist_worst = np.sqrt(((weighted - ideal_worst) ** 2).sum(axis=1))

    score = dist_worst / (dist_best + dist_worst)

    df["Topsis Score"] = score
    df["Rank"] = score.rank(ascending=False).astype(int)

    output_path = os.path.join("outputs", "topsis_result.csv")
    df.to_csv(output_path, index=False)

    st.success("TOPSIS calculation completed successfully!")
    st.download_button("Download Result", data=df.to_csv(index=False), file_name="topsis_result.csv")

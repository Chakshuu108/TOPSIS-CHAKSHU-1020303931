import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="TOPSIS", layout="centered")

st.title("🧮📊TOPSIS Calculator")

with st.form("topsis_form"):
    input_file = st.file_uploader("File Name", type=["csv"])
    weights_input = st.text_input("Weights", value="1,1,1,1")
    impacts_input = st.text_input("Impacts", value="+,+,-,+")
    email_id = st.text_input("Email Id")

    submit_btn = st.form_submit_button("Submit")


if submit_btn:
    if input_file is None:
        st.error("Please upload a CSV file")
        st.stop()

    try:
        df = pd.read_csv(input_file)
    except Exception:
        st.error("Invalid CSV file")
        st.stop()

    weights = weights_input.split(",")
    impacts = impacts_input.split(",")

    if len(df.columns) < 3:
        st.error("File must contain at least 3 columns")
        st.stop()

    if len(weights) != len(df.columns) - 1 or len(impacts) != len(df.columns) - 1:
        st.error("Weights and impacts count must match criteria columns")
        st.stop()

    try:
        weights = np.array(weights, dtype=float)
        weights = weights / weights.sum()
        df.iloc[:, 1:] = df.iloc[:, 1:].astype(float)
    except:
        st.error("Invalid numeric values in file or weights")
        st.stop()

    decision_matrix = df.iloc[:, 1:].values
    norm_matrix = decision_matrix / np.sqrt((decision_matrix ** 2).sum(axis=0))
    weighted_matrix = norm_matrix * weights

    ideal_best, ideal_worst = [], []

    for i in range(len(impacts)):
        if impacts[i] == "+":
            ideal_best.append(weighted_matrix[:, i].max())
            ideal_worst.append(weighted_matrix[:, i].min())
        else:
            ideal_best.append(weighted_matrix[:, i].min())
            ideal_worst.append(weighted_matrix[:, i].max())

    ideal_best = np.array(ideal_best)
    ideal_worst = np.array(ideal_worst)

    dist_best = np.sqrt(((weighted_matrix - ideal_best) ** 2).sum(axis=1))
    dist_worst = np.sqrt(((weighted_matrix - ideal_worst) ** 2).sum(axis=1))

    score = dist_worst / (dist_best + dist_worst)

    df["Topsis Score"] = score.round(6)
    df["Rank"] = df["Topsis Score"].rank(ascending=False, method="dense").astype(int)

    st.success("TOPSIS calculation completed")
    st.dataframe(df)

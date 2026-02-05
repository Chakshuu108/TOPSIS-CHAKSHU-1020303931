import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="TOPSIS Calculator", layout="centered")

st.title("📊 TOPSIS Decision Making Tool")
st.write("Upload a CSV file and compute TOPSIS scores")

# File upload
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("Input Data")
    st.dataframe(df)

    cols = df.columns.tolist()

    st.subheader("TOPSIS Parameters")

    weights = st.text_input(
        "Enter weights (comma separated)",
        placeholder="1,1,1,1"
    )

    impacts = st.text_input(
        "Enter impacts (comma separated)",
        placeholder="+,+,-,+"
    )

    if st.button("Calculate TOPSIS"):
        try:
            weights = np.array(list(map(float, weights.split(","))))
            impacts = impacts.split(",")

            data = df.iloc[:, 1:].values.astype(float)

            # Step 1: Normalize
            norm = data / np.sqrt((data ** 2).sum(axis=0))

            # Step 2: Weighted normalized
            weighted = norm * weights

            # Step 3: Ideal best & worst
            ideal_best = []
            ideal_worst = []

            for i in range(len(impacts)):
                if impacts[i] == "+":
                    ideal_best.append(weighted[:, i].max())
                    ideal_worst.append(weighted[:, i].min())
                else:
                    ideal_best.append(weighted[:, i].min())
                    ideal_worst.append(weighted[:, i].max())

            ideal_best = np.array(ideal_best)
            ideal_worst = np.array(ideal_worst)

            # Step 4: Distance
            d_pos = np.sqrt(((weighted - ideal_best) ** 2).sum(axis=1))
            d_neg = np.sqrt(((weighted - ideal_worst) ** 2).sum(axis=1))

            # Step 5: Score
            score = d_neg / (d_pos + d_neg)

            df["TOPSIS Score"] = score
            df["Rank"] = df["TOPSIS Score"].rank(ascending=False)

            st.subheader("Result")
            st.dataframe(df)

            # Download
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "⬇️ Download Result CSV",
                csv,
                "result.csv",
                "text/csv"
            )

        except Exception as e:
            st.error(f"Error: {e}")

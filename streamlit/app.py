import streamlit as st
import pandas as pd
import numpy as np
import smtplib
from email.message import EmailMessage
import tempfile

# ---------------- EMAIL CONFIG ----------------
SENDER_EMAIL = "yourgmail@gmail.com"
APP_PASSWORD = "your_app_password"
# ---------------------------------------------


st.set_page_config(
    page_title="TOPSIS Tool",
    page_icon="📊",
    layout="centered"
)

# ---------------- CSS ----------------
st.markdown("""
<style>
.main {
    background-color: #f4f6f9;
}
.card {
    background-color: white;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.08);
}
.stButton>button {
    background-color: #ff9800;
    color: white;
    font-weight: bold;
    width: 100%;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

st.title("📊 TOPSIS Decision Making Tool")
st.caption("Technique for Order Preference by Similarity to Ideal Solution")

st.markdown('<div class="card">', unsafe_allow_html=True)

with st.form("topsis_form"):
    uploaded_file = st.file_uploader("📁 File Name", type=["csv"])
    weights_input = st.text_input("⚖ Weights", value="1,1,1,1")
    impacts_input = st.text_input("📈 Impacts", value="+,+,-,+")
    user_email = st.text_input("📧 Email Id")

    submit_btn = st.form_submit_button("Submit")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- LOGIC ----------------
if submit_btn:

    if uploaded_file is None or user_email.strip() == "":
        st.error("Please upload CSV file and enter email id")
        st.stop()

    try:
        df = pd.read_csv(uploaded_file)
    except:
        st.error("Invalid CSV file")
        st.stop()

    weights = weights_input.split(",")
    impacts = impacts_input.split(",")

    if len(df.columns) < 3:
        st.error("CSV must contain at least 3 columns")
        st.stop()

    if len(weights) != len(df.columns) - 1 or len(impacts) != len(df.columns) - 1:
        st.error("Weights and impacts count mismatch")
        st.stop()

    try:
        df.iloc[:, 1:] = df.iloc[:, 1:].astype(float)
        weights = np.array(weights, dtype=float)
        weights = weights / weights.sum()
    except:
        st.error("Numeric error in weights or CSV data")
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

    # -------- SAVE RESULT TEMPORARILY --------
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        df.to_csv(tmp.name, index=False)
        result_path = tmp.name

    # -------- SEND EMAIL --------
    try:
        msg = EmailMessage()
        msg["Subject"] = "TOPSIS Result Report"
        msg["From"] = SENDER_EMAIL
        msg["To"] = user_email
        msg.set_content("Please find attached the TOPSIS result generated from your uploaded CSV file.")

        with open(result_path, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="octet-stream",
                filename="TOPSIS_Result.csv"
            )

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(msg)

        st.success("✅ Result sent successfully to your email!")
        st.dataframe(df)

    except Exception as e:
        st.error("Failed to send email. Please check email configuration.")

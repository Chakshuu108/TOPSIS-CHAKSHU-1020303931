import streamlit as st
import pandas as pd
import numpy as np
import smtplib
from email.message import EmailMessage
import tempfile
import os

# ---------------- EMAIL CONFIG ----------------
SENDER_EMAIL = st.secrets["SENDER_EMAIL"]
APP_PASSWORD = st.secrets["APP_PASSWORD"]

# ---------------------------------------------

st.set_page_config(
    page_title="TOPSIS Tool",
    page_icon="📊",
    layout="centered"
)

# ---------------- REVOLUTIONARY CSS ----------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800;900&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Animated gradient background */
    .main {
        background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe, #00f2fe);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        padding: 0;
        min-height: 100vh;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Floating particles background */
    .main::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 20% 50%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(255, 255, 255, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 40% 20%, rgba(255, 255, 255, 0.08) 0%, transparent 50%);
        pointer-events: none;
        animation: float 20s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    
    .block-container {
        padding-top: 4rem;
        padding-bottom: 4rem;
        max-width: 950px;
    }
    
    /* Liquid glass morphism container */
    .liquid-glass {
        position: relative;
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(30px) saturate(180%);
        -webkit-backdrop-filter: blur(30px) saturate(180%);
        padding: 3rem;
        border-radius: 32px;
        border: 2px solid rgba(255, 255, 255, 0.25);
        box-shadow: 
            0 8px 32px 0 rgba(0, 0, 0, 0.2),
            inset 0 1px 0 0 rgba(255, 255, 255, 0.3),
            0 0 60px rgba(255, 255, 255, 0.1);
        margin: 2rem 0;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        overflow: hidden;
    }
    
    .liquid-glass::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s;
    }
    
    .liquid-glass:hover::before {
        left: 100%;
    }
    
    .liquid-glass:hover {
        transform: translateY(-5px);
        box-shadow: 
            0 12px 48px 0 rgba(0, 0, 0, 0.25),
            inset 0 1px 0 0 rgba(255, 255, 255, 0.4),
            0 0 80px rgba(255, 255, 255, 0.15);
        border-color: rgba(255, 255, 255, 0.4);
    }
    
    /* Neon title with text animation */
    h1 {
        color: white !important;
        text-align: center;
        font-weight: 900 !important;
        margin-bottom: 0 !important;
        font-size: 4.5rem !important;
        letter-spacing: -2px !important;
        text-shadow: 
            0 0 10px rgba(255, 255, 255, 0.8),
            0 0 20px rgba(255, 255, 255, 0.6),
            0 0 40px rgba(102, 126, 234, 0.8),
            0 0 80px rgba(118, 75, 162, 0.6),
            0 5px 25px rgba(0, 0, 0, 0.3);
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from {
            text-shadow: 
                0 0 10px rgba(255, 255, 255, 0.8),
                0 0 20px rgba(255, 255, 255, 0.6),
                0 0 40px rgba(102, 126, 234, 0.8),
                0 0 80px rgba(118, 75, 162, 0.6);
        }
        to {
            text-shadow: 
                0 0 20px rgba(255, 255, 255, 1),
                0 0 30px rgba(255, 255, 255, 0.8),
                0 0 60px rgba(102, 126, 234, 1),
                0 0 100px rgba(118, 75, 162, 0.8);
        }
    }
    
    /* Cyberpunk caption */
    .caption {
        text-align: center;
        color: rgba(255, 255, 255, 0.95) !important;
        font-size: 1.3rem;
        margin-bottom: 3rem;
        font-weight: 400;
        letter-spacing: 3px;
        text-transform: uppercase;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }
    
    /* Floating label animation */
    .stTextInput label, .stFileUploader label {
        color: white !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
        letter-spacing: 0.5px;
        text-transform: uppercase;
        animation: labelFloat 3s ease-in-out infinite;
    }
    
    @keyframes labelFloat {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-2px); }
    }
    
    /* Neon input fields with 3D depth */
    .stTextInput input {
        border-radius: 16px !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        background: rgba(0, 0, 0, 0.2) !important;
        backdrop-filter: blur(20px) !important;
        color: white !important;
        font-weight: 500 !important;
        font-size: 1rem !important;
        padding: 0.9rem 1.2rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 
            inset 0 2px 8px rgba(0, 0, 0, 0.3),
            0 0 20px rgba(255, 255, 255, 0.1);
    }
    
    .stTextInput input::placeholder {
        color: rgba(255, 255, 255, 0.5) !important;
        font-weight: 400;
    }
    
    .stTextInput input:focus {
        border-color: rgba(255, 255, 255, 0.9) !important;
        background: rgba(255, 255, 255, 0.15) !important;
        box-shadow: 
            inset 0 2px 8px rgba(0, 0, 0, 0.2),
            0 0 0 4px rgba(255, 255, 255, 0.2),
            0 0 40px rgba(102, 126, 234, 0.5),
            0 8px 24px rgba(0, 0, 0, 0.2) !important;
        transform: translateY(-2px);
    }
    
    /* Futuristic file uploader */
    .stFileUploader {
        background: rgba(0, 0, 0, 0.2) !important;
        backdrop-filter: blur(20px) !important;
        border-radius: 20px !important;
        border: 3px dashed rgba(255, 255, 255, 0.3) !important;
        padding: 2rem !important;
        transition: all 0.3s ease !important;
        position: relative;
        overflow: hidden;
    }
    
    .stFileUploader::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        animation: scan 3s linear infinite;
    }
    
    @keyframes scan {
        0% { transform: translate(-50%, -50%) rotate(0deg); }
        100% { transform: translate(-50%, -50%) rotate(360deg); }
    }
    
    .stFileUploader:hover {
        border-color: rgba(255, 255, 255, 0.6) !important;
        background: rgba(255, 255, 255, 0.1) !important;
        box-shadow: 0 0 30px rgba(255, 255, 255, 0.2);
    }
    
    .uploadedFile {
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 12px !important;
        padding: 0.8rem !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    
    /* Holographic submit button */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%) !important;
        color: white !important;
        font-weight: 900 !important;
        width: 100% !important;
        border-radius: 20px !important;
        padding: 1.2rem 2.5rem !important;
        border: none !important;
        font-size: 1.3rem !important;
        letter-spacing: 2px !important;
        text-transform: uppercase;
        margin-top: 2rem !important;
        position: relative;
        overflow: hidden;
        box-shadow: 
            0 10px 40px rgba(102, 126, 234, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    .stButton>button::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        transform: rotate(45deg);
        transition: all 0.6s;
    }
    
    .stButton>button:hover::before {
        left: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-4px) scale(1.02);
        box-shadow: 
            0 15px 50px rgba(102, 126, 234, 0.6),
            inset 0 1px 0 rgba(255, 255, 255, 0.5),
            0 0 60px rgba(118, 75, 162, 0.5);
    }
    
    .stButton>button:active {
        transform: translateY(-2px) scale(0.98);
    }
    
    /* Neon results card */
    .results-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 3rem;
        border-radius: 28px;
        box-shadow: 
            0 20px 60px rgba(0, 0, 0, 0.3),
            0 0 80px rgba(102, 126, 234, 0.3);
        margin: 2.5rem 0;
        border: 2px solid rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .results-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb, #4facfe);
        background-size: 200% 100%;
        animation: gradientMove 3s linear infinite;
    }
    
    @keyframes gradientMove {
        0% { background-position: 0% 0%; }
        100% { background-position: 200% 0%; }
    }
    
    .results-card h3 {
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800 !important;
        margin-bottom: 2rem !important;
        font-size: 2rem !important;
    }
    
    /* Success/Error messages with neon glow */
    .stAlert {
        border-radius: 16px !important;
        margin-top: 1.5rem !important;
        backdrop-filter: blur(10px) !important;
        border-left: 4px solid !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
    }
    
    /* DataFrame with 3D effect */
    .dataframe {
        border-radius: 16px !important;
        overflow: hidden !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1) !important;
    }
    
    .stForm {
        border: none !important;
        background: transparent !important;
    }
    
    .row-widget.stHorizontal {
        gap: 1.5rem;
    }
    
    /* Holographic download button */
    .stDownloadButton>button {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%) !important;
        color: white !important;
        font-weight: 800 !important;
        border-radius: 16px !important;
        padding: 1rem 2rem !important;
        border: none !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 8px 24px rgba(79, 172, 254, 0.3);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stDownloadButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 32px rgba(79, 172, 254, 0.5) !important;
    }
    
    /* Spinner customization */
    .stSpinner > div {
        border-top-color: rgba(255, 255, 255, 0.9) !important;
    }
    
    /* Footer with neon line */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
        margin: 4rem 0 2rem 0;
        box-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
    }
    
    /* Column headers glow */
    thead tr th {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2, #f093fb);
    }
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.title("⚡ TOPSIS")
st.markdown('<p class="caption">Advanced Decision Intelligence System</p>', unsafe_allow_html=True)

# ---------------- FORM ----------------
st.markdown('<div class="liquid-glass">', unsafe_allow_html=True)

with st.form("topsis_form", clear_on_submit=False):
    uploaded_file = st.file_uploader("🚀 Upload Decision Matrix", type=["csv"], help="Upload your CSV file with alternatives and criteria")
    
    col1, col2 = st.columns(2)
    with col1:
        weights_input = st.text_input("⚖️ Weights", value="", placeholder="1,1,1,1")
    with col2:
        impacts_input = st.text_input("📊 Impacts", value="", placeholder="+,+,-,+")
    
    user_email = st.text_input("✉️ Email Address", placeholder="your.email@example.com")

    submit_btn = st.form_submit_button("⚡ Generate Results")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- LOGIC ----------------
if submit_btn:

    if uploaded_file is None or user_email.strip() == "":
        st.error("⚠️ Please upload a CSV file and enter your email address")
        st.stop()
    
    if weights_input.strip() == "" or impacts_input.strip() == "":
        st.error("⚠️ Please enter weights and impacts")
        st.stop()

    if "@" not in user_email or "." not in user_email:
        st.error("⚠️ Please enter a valid email address")
        st.stop()

    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"❌ Invalid CSV file: {str(e)}")
        st.stop()

    weights = weights_input.split(",")
    impacts = impacts_input.split(",")

    if len(df.columns) < 3:
        st.error("❌ CSV must contain at least 3 columns (1 for names, 2+ for criteria)")
        st.stop()

    if len(weights) != len(df.columns) - 1 or len(impacts) != len(df.columns) - 1:
        st.error(f"❌ Number of weights and impacts must match number of criteria. Expected {len(df.columns) - 1}, got {len(weights)} weights and {len(impacts)} impacts")
        st.stop()

    for impact in impacts:
        if impact.strip() not in ['+', '-']:
            st.error("❌ Impacts must be either '+' or '-'")
            st.stop()

    try:
        df.iloc[:, 1:] = df.iloc[:, 1:].astype(float)
        weights = np.array([float(w.strip()) for w in weights], dtype=float)
        weights = weights / weights.sum()
    except Exception as e:
        st.error(f"❌ Numeric error in weights or CSV data: {str(e)}")
        st.stop()

    # TOPSIS Calculation
    decision_matrix = df.iloc[:, 1:].values
    norm_matrix = decision_matrix / np.sqrt((decision_matrix ** 2).sum(axis=0))
    weighted_matrix = norm_matrix * weights

    ideal_best, ideal_worst = [], []

    for i in range(len(impacts)):
        if impacts[i].strip() == "+":
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

    # Display results
    st.markdown('<div class="results-card">', unsafe_allow_html=True)
    st.subheader("⚡ Analysis Results")
    st.dataframe(df, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Save result temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode='w') as tmp:
        df.to_csv(tmp.name, index=False)
        result_path = tmp.name

    # Send email
    if SENDER_EMAIL == "yourgmail@gmail.com" or APP_PASSWORD == "your_app_password":
        st.warning("⚠️ Email functionality is not configured. Please set up SENDER_EMAIL and APP_PASSWORD.")
        st.info("📥 You can download the results below:")
        
        csv_data = df.to_csv(index=False)
        st.download_button(
            label="⬇️ Download Results",
            data=csv_data,
            file_name="TOPSIS_Result.csv",
            mime="text/csv"
        )
    else:
        try:
            with st.spinner("📧 Sending email..."):
                msg = EmailMessage()
                msg["Subject"] = "TOPSIS Result Report"
                msg["From"] = SENDER_EMAIL
                msg["To"] = user_email
                msg.set_content(f"""
Hello,

Please find attached the TOPSIS result generated from your uploaded CSV file.

Summary:
- Total Alternatives: {len(df)}
- Top Ranked: {df.iloc[df['Rank'].idxmin(), 0]} (Score: {df['Topsis Score'].max():.6f})

Best regards,
TOPSIS Decision Making Tool
                """)

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

            st.success(f"✅ Results sent successfully to {user_email}!")
            
            csv_data = df.to_csv(index=False)
            st.download_button(
                label="⬇️ Download Results",
                data=csv_data,
                file_name="TOPSIS_Result.csv",
                mime="text/csv"
            )

        except Exception as e:
            st.error(f"❌ Failed to send email: {str(e)}")
            st.info("💡 Please check your email configuration or use the download button below:")
            
            csv_data = df.to_csv(index=False)
            st.download_button(
                label="⬇️ Download Results",
                data=csv_data,
                file_name="TOPSIS_Result.csv",
                mime="text/csv"
            )
            
        finally:
            try:
                os.unlink(result_path)
            except:
                pass

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: rgba(255, 255, 255, 0.9); font-size: 1rem; letter-spacing: 2px;'>⚡ POWERED BY ADVANCED ANALYTICS ⚡</p>",
    unsafe_allow_html=True
)

import streamlit as st
import pandas as pd
import numpy as np
import smtplib
from email.message import EmailMessage
import tempfile
import os

# ---------------- EMAIL CONFIG ----------------
# Use Streamlit secrets or environment variables for production
SENDER_EMAIL = st.secrets["SENDER_EMAIL"]
APP_PASSWORD = st.secrets["APP_PASSWORD"]


# ---------------------------------------------


st.set_page_config(
    page_title="TOPSIS Tool",
    page_icon="📊",
    layout="centered"
)

# ---------------- ENHANCED CSS ----------------
st.markdown("""
<style>
    /* Main background */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 0;
    }
    
    /* Remove default Streamlit padding */
    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 900px;
    }
    
    /* Glass card styling */
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        padding: 2.5rem;
        border-radius: 24px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
        margin-bottom: 2rem;
    }
    
    /* Title styling */
    h1 {
        color: white !important;
        text-align: center;
        font-weight: 800 !important;
        margin-bottom: 0.5rem !important;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
        font-size: 3.5rem !important;
    }
    
    /* Caption styling */
    .caption {
        text-align: center;
        color: rgba(255, 255, 255, 0.95) !important;
        font-size: 1.2rem;
        margin-bottom: 3rem;
        font-weight: 300;
        letter-spacing: 1px;
    }
    
    /* Input labels */
    .stTextInput label, .stFileUploader label {
        color: white !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    
    /* Input fields */
    .stTextInput input {
        border-radius: 12px !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(10px) !important;
        color: white !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput input::placeholder {
        color: rgba(255, 255, 255, 0.6) !important;
    }
    
    .stTextInput input:focus {
        border-color: rgba(255, 255, 255, 0.8) !important;
        box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.2) !important;
        background: rgba(255, 255, 255, 0.2) !important;
    }
    
    /* File uploader */
    .stFileUploader {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 12px !important;
        border: 2px dashed rgba(255, 255, 255, 0.3) !important;
        padding: 1rem !important;
    }
    
    .stFileUploader label {
        color: white !important;
    }
    
    .uploadedFile {
        background: rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 8px !important;
        padding: 0.5rem !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
    }
    
    /* Submit button */
    .stButton>button {
        background: rgba(255, 255, 255, 0.95) !important;
        color: #667eea !important;
        font-weight: 800 !important;
        width: 100% !important;
        border-radius: 16px !important;
        padding: 1rem 2rem !important;
        border: none !important;
        font-size: 1.2rem !important;
        letter-spacing: 1px !important;
        transition: all 0.3s ease !important;
        margin-top: 1.5rem !important;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2) !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.3) !important;
        background: white !important;
    }
    
    /* Results card */
    .results-card {
        background: rgba(255, 255, 255, 0.98);
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
        margin: 2rem 0;
    }
    
    /* Success/Error messages */
    .stAlert {
        border-radius: 12px !important;
        margin-top: 1rem !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* DataFrame styling */
    .dataframe {
        border-radius: 10px !important;
        overflow: hidden !important;
    }
    
    /* Remove white box around form */
    .stForm {
        border: none !important;
        background: transparent !important;
    }
    
    /* Column spacing */
    .row-widget.stHorizontal {
        gap: 1rem;
    }
    
    /* Download button */
    .stDownloadButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        border: none !important;
        transition: all 0.3s ease !important;
    }
    
    .stDownloadButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* Subheader in results */
    .results-card h3 {
        color: #667eea !important;
        font-weight: 700 !important;
        margin-bottom: 1.5rem !important;
    }
    
    /* Footer */
    hr {
        border: none;
        height: 1px;
        background: rgba(255, 255, 255, 0.2);
        margin: 3rem 0 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.title("📊 TOPSIS")
st.markdown('<p class="caption">Technique for Order Preference by Similarity to Ideal Solution</p>', unsafe_allow_html=True)

# ---------------- FORM ----------------
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

with st.form("topsis_form", clear_on_submit=False):
    uploaded_file = st.file_uploader("📁 Upload CSV File", type=["csv"], help="Upload your decision matrix")
    
    col1, col2 = st.columns(2)
    with col1:
        weights_input = st.text_input("⚖️ Weights", value="", placeholder="e.g., 1,1,1,1")
    with col2:
        impacts_input = st.text_input("📈 Impacts", value="", placeholder="e.g., +,+,-,+")
    
    user_email = st.text_input("📧 Email Address", placeholder="your.email@example.com")

    submit_btn = st.form_submit_button("🚀 Generate TOPSIS Results")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- LOGIC ----------------
if submit_btn:

    if uploaded_file is None or user_email.strip() == "":
        st.error("⚠️ Please upload a CSV file and enter your email address")
        st.stop()
    
    if weights_input.strip() == "" or impacts_input.strip() == "":
        st.error("⚠️ Please enter weights and impacts")
        st.stop()

    # Validate email format
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

    # Validate impacts
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
    st.subheader("📊 TOPSIS Results")
    st.dataframe(df, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # -------- SAVE RESULT TEMPORARILY --------
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode='w') as tmp:
        df.to_csv(tmp.name, index=False)
        result_path = tmp.name

    # -------- SEND EMAIL --------
    # Check if email credentials are configured
    if SENDER_EMAIL == "yourgmail@gmail.com" or APP_PASSWORD == "your_app_password":
        st.warning("⚠️ Email functionality is not configured. Please set up SENDER_EMAIL and APP_PASSWORD.")
        st.info("📥 You can download the results below:")
        
        # Provide download button
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
            
            # Also provide download option
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
            
            # Provide download button as fallback
            csv_data = df.to_csv(index=False)
            st.download_button(
                label="⬇️ Download Results",
                data=csv_data,
                file_name="TOPSIS_Result.csv",
                mime="text/csv"
            )
            
        finally:
            # Clean up temp file
            try:
                os.unlink(result_path)
            except:
                pass

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: rgba(255, 255, 255, 0.9); font-size: 0.95rem;'>Made with ❤️ using Streamlit | TOPSIS Algorithm</p>",
    unsafe_allow_html=True
)

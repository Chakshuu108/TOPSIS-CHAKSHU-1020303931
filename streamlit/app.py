import streamlit as st
import pandas as pd
import numpy as np
import smtplib
from email.message import EmailMessage
import tempfile
import os

# ---------------- EMAIL CONFIG ----------------
# Use Streamlit secrets or environment variables for production
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "yourgmail@gmail.com")
APP_PASSWORD = os.getenv("APP_PASSWORD", "your_app_password")
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
        max-width: 800px;
    }
    
    /* Card styling */
    .card {
        background: rgba(255, 255, 255, 0.95);
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
        margin-bottom: 2rem;
    }
    
    /* Title styling */
    h1 {
        color: white !important;
        text-align: center;
        font-weight: 800 !important;
        margin-bottom: 0.5rem !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    /* Caption styling */
    .caption {
        text-align: center;
        color: rgba(255, 255, 255, 0.9) !important;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    /* Input labels */
    .stTextInput label, .stFileUploader label {
        color: #4a5568 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    
    /* Input fields */
    .stTextInput input, .stFileUploader {
        border-radius: 10px !important;
        border: 2px solid #e2e8f0 !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    /* Submit button */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        width: 100% !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        border: none !important;
        font-size: 1.1rem !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s ease !important;
        margin-top: 1rem !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* File uploader */
    .uploadedFile {
        background-color: #f7fafc !important;
        border-radius: 8px !important;
        padding: 0.5rem !important;
    }
    
    /* Success/Error messages */
    .stAlert {
        border-radius: 10px !important;
        margin-top: 1rem !important;
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
    
    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, #f6f8fb 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        margin: 1.5rem 0;
    }
    
    .info-box h3 {
        color: #667eea;
        margin-top: 0;
        font-size: 1.1rem;
    }
    
    .info-box p {
        color: #4a5568;
        margin-bottom: 0;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.title("📊 TOPSIS Decision Making Tool")
st.markdown('<p class="caption">Technique for Order Preference by Similarity to Ideal Solution</p>', unsafe_allow_html=True)

# ---------------- INFO BOX ----------------
st.markdown("""
<div class="info-box">
    <h3>📝 How to use:</h3>
    <p>
        1️⃣ Upload a CSV file with alternatives and criteria<br>
        2️⃣ Enter weights (comma-separated, e.g., 1,2,1,3)<br>
        3️⃣ Specify impacts (+ for benefit, - for cost, e.g., +,+,-,+)<br>
        4️⃣ Provide your email to receive results
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------- FORM ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)

with st.form("topsis_form", clear_on_submit=False):
    uploaded_file = st.file_uploader("📁 Upload CSV File", type=["csv"], help="Maximum file size: 200MB")
    
    col1, col2 = st.columns(2)
    with col1:
        weights_input = st.text_input("⚖️ Weights", value="1,1,1,1", help="Comma-separated values")
    with col2:
        impacts_input = st.text_input("📈 Impacts", value="+,+,-,+", help="Use + or - for each criterion")
    
    user_email = st.text_input("📧 Email Address", placeholder="your.email@example.com")

    submit_btn = st.form_submit_button("🚀 Generate TOPSIS Results")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- LOGIC ----------------
if submit_btn:

    if uploaded_file is None or user_email.strip() == "":
        st.error("⚠️ Please upload a CSV file and enter your email address")
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
    st.markdown('<div class="card">', unsafe_allow_html=True)
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
    "<p style='text-align: center; color: white; opacity: 0.8;'>Made with ❤️ using Streamlit | TOPSIS Algorithm</p>",
    unsafe_allow_html=True
)

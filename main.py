import streamlit as st
import json
import requests
import base64
from PIL import Image
import io
import os
import pandas as pd

IMAGE_URL = "https://cdn.cancercenter.com/-/media/ctca/images/others/blogs/2016/08-august/09-news-cell-wars-fb.jpg"
# CONSTANTS
PREDICTED_LABELS = ['High squamous intra-epithelial lesion', 
                    'Low squamous intra-epithelial lesion', 
                    'Negative for Intraepithelial malignancy', 
                    'Squamous cell carcinoma']
PREDICTED_LABELS.sort()
UPLOAD_DIR = "uploaded_images"
RECORDS_FILE = "patient_records.json"

os.makedirs(UPLOAD_DIR, exist_ok=True)

# Load user credentials from secrets
USER_CREDENTIALS = st.secrets["users"]
url = st.secrets["url"]["url"]

# Initialize session state variables
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = None
if "patient_records" not in st.session_state:
    st.session_state["patient_records"] = {}  # {username: [records]}

# Utility functions
def save_records_to_file():
    """Save patient records to a JSON file."""
    with open(RECORDS_FILE, "w") as file:
        json.dump(st.session_state["patient_records"], file)


def load_records_from_file():
    """Load patient records from a JSON file."""
    if os.path.exists(RECORDS_FILE):
        with open(RECORDS_FILE, "r") as file:
            st.session_state["patient_records"] = json.load(file)


# Load records at the start
load_records_from_file()


def get_prediction(image_data):
    url = url
    r = requests.post(url, data=image_data)
    response = r.json()['predicted_label']
    score = r.json()['score']
    return response, score


def login_page():
    st.title("CerviHope Login")

    username = st.text_input("👤 Enter Username")
    password = st.text_input("🔒 Enter Password", type="password")

    if st.button("Login"):
        # Authentication logic
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            if username not in st.session_state["patient_records"]:
                st.session_state["patient_records"][username] = []  # Initialize record
            st.success("✅ Login successful!")
        else:
            st.error("❌ Invalid username or password.")


def about_page():
    st.title("About CerviHope")
    st.image(IMAGE_URL, caption="CerviHope - Empowering Pathologists", use_column_width=True)

    st.markdown(
        """
        ### 🩺 CerviHope: Cancer Cell Analysis Made Simple
        CerviHope is an advanced AI-powered web app designed to assist pathologists in diagnosing cancer cells.
        It provides:
        - 📊 Accurate classification of cancer cell images
        - 📋 Streamlined patient record management
        - 🌐 Accessible results and predictions
        
        #### 📍 Prediction Categories:
        1. High squamous intra-epithelial lesion  
        2. Low squamous intra-epithelial lesion  
        3. Negative for Intraepithelial malignancy  
        4. Squamous cell carcinoma  

        ---
        #### Designed for accuracy and accessibility.
        """
    )


def image_analysis_page():
    st.title("🖼️ Image Analysis")

    with st.form("patient_form"):
        patient_name = st.text_input("Enter Patient Name 🧑‍⚕️")
        image = st.file_uploader("Upload a cancer cell image (JPG/PNG)", type=['jpg', 'png', 'jpeg'])
        submit = st.form_submit_button("🔍 Analyze")

    if submit and patient_name and image:
        img = Image.open(image).convert('RGB')
        buf = io.BytesIO()
        img.save(buf, format='JPEG')
        byte_im = buf.getvalue()

        payload = base64.b64encode(byte_im)
        saved_image_path = os.path.join(UPLOAD_DIR, image.name)
        img.save(saved_image_path)

        response, scores = get_prediction(payload)
        response_label = PREDICTED_LABELS[response]
        confidence_score = max(scores)

        st.image(img, caption=f"Uploaded Image: {image.name}", use_column_width=True)
        st.success(f"**Prediction:** {response_label}")
        st.info(f"**Confidence Score:** {confidence_score:.2f}")

        # Add record to session state
        username = st.session_state["username"]

        # Ensure the user's record list is initialized
        if username not in st.session_state["patient_records"]:
            st.session_state["patient_records"][username] = []

        st.session_state["patient_records"][username].append({
            "Patient Name": patient_name,
            "Image Name": image.name,
            "Prediction": response_label,
            "Confidence": confidence_score,
            "Image Path": saved_image_path
        })
        save_records_to_file()  # Save updated records to file


def patient_records_page():
    st.title("📋 Patient Records")
    username = st.session_state["username"]

    if st.session_state["patient_records"].get(username):
        records = st.session_state["patient_records"][username]
        records_df = pd.DataFrame(records)
        st.dataframe(records_df.drop(columns=["Image Path"]))

        for record in records:
            if st.button(f"🖼️ View Image: {record['Image Name']}"):
                st.image(record["Image Path"], caption=f"Image for {record['Patient Name']}")
    else:
        st.info("No records available yet. Upload an image in the **Image Analysis** section.")


def app_page():
    st.sidebar.title("🔍 Navigation")
    page = st.sidebar.radio("", ["🏠 About", "🖼️ Image Analysis", "📋 Patient Records", "🚪 Logout"])

    if page == "🏠 About":
        about_page()
    elif page == "🖼️ Image Analysis":
        image_analysis_page()
    elif page == "📋 Patient Records":
        patient_records_page()
    elif page == "🚪 Logout":
        st.session_state["logged_in"] = False
        st.session_state["username"] = None
        st.success("You have successfully logged out. See you next time!")


# Main logic
if st.session_state["logged_in"]:
    app_page()
else:
    login_page()

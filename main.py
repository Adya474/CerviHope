import streamlit as st
import json
import requests
import base64
from PIL import Image
import io
#CONSTANTS
PREDICTED_LABELS = ['High squamous intra-epithelial lesion','Low squamous intra-epithelial lesion','Negative for Intraepithelial malignancy','Squamous cell carcinoma']
IMAGE_URL = "https://cdn.cancercenter.com/-/media/ctca/images/others/blogs/2016/08-august/09-news-cell-wars-fb.jpg"
PREDICTED_LABELS.sort()

def get_prediction(image_data):
  #replace your image classification ai service endpoint URL
  url = 'https://askai.aiclub.world/c23bffea-9fc9-41f9-b2b-ac7e272f1e9b'  
  r = requests.post(url, data=image_data)
  response = r.json()['predicted_label']
  score = r.json()['score']
  #print("Predicted_label: {} and confidence_score: {}".format(response,score))
  return response, score

# Initialize session state variables
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

def login_page():
    st.title('Login Page')

    username = st.text_input('Enter Username')
    password = st.text_input('Enter Password', type="password")

    if st.button("Login"):
        # Simple authentication logic
        if username == "admin" and password == "password123":  # Replace with your logic
            st.session_state["logged_in"] = True
            st.success("Login successful! Redirecting...")
        else:
            st.error("Invalid username or password.")

def app_page():
    st.title('CerviHope')
    #setting the main picture
    st.image(IMAGE_URL, caption = "Image Classification")

    #about the web app
    st.header("About the Web App")

    #details about the project
    with st.expander("Web App 🌐"):
        st.subheader("Cancer Cell Predictions")
        st.write("""My app is designed to predict and classify cancer cell images into one of the following categories :
        1.High squamous intra-epithelial lesion
        2.Low squamous intra-epithelial lesion
        3.Negative for Intraepithelial malignancy
        4.Squamous cell carcinoma""")
    #setting file uploader
    image =st.file_uploader("Upload a cancer cell image",type = ['jpg','png','jpeg'])
    if image:
        #converting the image to bytes
        img = Image.open(image).convert('RGB') #ensuring to convert into RGB as model expects the image to be in 3 channel
        buf = io.BytesIO()
        img.save(buf,format = 'JPEG')
        byte_im = buf.getvalue()

        #converting bytes to b64encoding
        payload = base64.b64encode(byte_im)
        #file details
        file_details = {
            "file name": image.name,
            "file type": image.type,
            "file size": image.size
        }
        #write file details
        st.write(file_details)
        #setting up the image
        st.image(img)
        #predictions
        response, scores = get_prediction(payload)
        #if you are using the model deployment in navigator
        #you need to define the labels
        response_label = PREDICTED_LABELS[response]
        st.metric("Prediction Label",response_label)
        st.metric("Confidence Score", max(scores))

# Main logic
if st.session_state["logged_in"]:
    app_page()
else:
    login_page()
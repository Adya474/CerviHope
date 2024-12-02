import streamlit as st

def login_page():
    st.title('Login Page')

    username = st.text_input('Enter Username')
    password = st.text_input('Enter Password')

    
    if st.button("Login"):
        st.success("Welcome")
        app_page()

def app_page():
    st.title('CerviHope')

    st.write('''
    Recurring costs include cloud storage, computing resources, model updates, and user support.
     Additional expenses cover training materials, continuous marketing to engage NGOs and government
      health officials, and outreach for broader adoption.

    ''')

login_page()
import streamlit as st

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

    st.write('''
    Recurring costs include cloud storage, computing resources, model updates, and user support.
    Additional expenses cover training materials, continuous marketing to engage NGOs and government
    health officials, and outreach for broader adoption.
    ''')

# Main logic
if st.session_state["logged_in"]:
    app_page()
else:
    login_page()
import streamlit as st
import requests

# Title for the Streamlit app
st.title("Flask and Streamlit Integration")

# Embed the Flask app using an iframe
st.markdown("### Flask App Preview:")
flask_app_url = "http://127.0.0.1:5000"  # Flask app URL

# Check if the Flask app is running
try:
    response = requests.get(flask_app_url)
    if response.status_code == 200:
        st.markdown(
            f'<iframe src="{flask_app_url}" width="100%" height="600px" frameborder="0"></iframe>',
            unsafe_allow_html=True,
        )
    else:
        st.error("Flask app is not responding.")
except requests.exceptions.ConnectionError:
    st.error("Flask app is not running. Please start the Flask app first.")

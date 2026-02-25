import streamlit as st

def main():
    st.set_page_config(page_title="Insurance Spam Detection", layout="wide")

    # Title and description
    st.title("Insurance Spam Detection System")
    st.markdown(
        """
        ### Spam Detection System
        This AI and ML system detects spam and provides intelligent responses for:
        - Emails
        - SMS
        - APK files
        - Phone numbers
        - Images

        It also offers offline capability and assistance.
        """
    )

    # Input options
    st.sidebar.header("Input Options")
    input_type = st.sidebar.selectbox("Select Input Type", ["Text", "Image", "SMS", "Phone Number", "Email", "APK File"])

    if input_type == "Text":
        user_input = st.text_area("Enter the text to analyze for spam:")
        if st.button("Analyze Text"):
            st.write("Analyzing text for spam...")
            # Call the Groq model API here

    elif input_type == "Image":
        uploaded_image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
        if uploaded_image and st.button("Analyze Image"):
            st.write("Analyzing image for spam...")
            # Call the Groq model API here

    elif input_type == "SMS":
        sms_input = st.text_input("Enter the SMS content:")
        if st.button("Analyze SMS"):
            st.write("Analyzing SMS for spam...")
            # Call the Groq model API here

    elif input_type == "Phone Number":
        phone_number = st.text_input("Enter the phone number:")
        if st.button("Analyze Phone Number"):
            st.write("Analyzing phone number for spam...")
            # Call the Groq model API here

    elif input_type == "Email":
        email_input = st.text_input("Enter the email address:")
        if st.button("Analyze Email"):
            st.write("Analyzing email for spam...")
            # Call the Groq model API here

    elif input_type == "APK File":
        uploaded_apk = st.file_uploader("Upload an APK file", type=["apk"])
        if uploaded_apk and st.button("Analyze APK"):
            st.write("Analyzing APK file for spam...")
            # Call the Groq model API here

    # Footer
    st.sidebar.markdown("---")
    st.sidebar.write("Powered by Groq Model Ilama-3.1-8b-instant")

if __name__ == "__main__":
    main()
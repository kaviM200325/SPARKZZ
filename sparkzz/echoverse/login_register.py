import streamlit as st
from backend.database import register_user, login_user

# Custom CSS for login form
st.markdown("""
<style>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');
body {
    background: linear-gradient(to right, #ff7e5f, #feb47b);
}
.login-container {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}
.login-form {
    background: white;
    padding: 3rem;
    border-radius: 15px;
    box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    width: 450px;
    text-align: center;
}
.stTextInput, .stButton>button {
    width: 100%;
    margin-bottom: 1rem;
}
.stTextInput input {
    border-radius: 25px;
    padding: 1rem 3rem;
    border: 1px solid #ddd;
}
.stButton>button {
    border-radius: 25px;
    padding: 1rem;
    background: linear-gradient(to right, #ff7e5f, #feb47b);
    color: white;
    font-weight: bold;
    border: none;
}
.stTextInput i {
    position: absolute;
    left: 20px;
    top: 50%;
    transform: translateY(-50%);
    color: #aaa;
}
</style>
""", unsafe_allow_html=True)

def login_register_app():
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        st.header('Welcome Back!')

        username_or_email = st.text_input('Username or Email', placeholder='Username or Email', label_visibility='collapsed')
        password = st.text_input('Password', type='password', placeholder='Password', label_visibility='collapsed')

        if st.button('Login'):
            user = login_user(username_or_email, password)
            if user:
                st.session_state['user'] = user['username']
                st.session_state['logged_in'] = True
                st.success('Logged in successfully!')
                st.rerun()
            else:
                st.error('Invalid credentials')

    with tab2:
        st.header('Register')
        full_name = st.text_input('Full Name')
        username = st.text_input('Username')
        email = st.text_input('Email')
        age = st.number_input('Age', min_value=0, max_value=150)
        gender = st.selectbox('Gender', ['Male', 'Female', 'Other'])
        password = st.text_input('Password', type='password')
        confirm_password = st.text_input('Confirm Password', type='password')
        if st.button('Register'):
            if password != confirm_password:
                st.error('Passwords do not match')
            elif len(password) < 6:
                st.error('Password must be at least 6 characters')
            else:
                if register_user(username, email, password, full_name, age, gender):
                    st.success('Registered successfully! Please login.')
                else:
                    st.error('Username or email already exists')

login_register_app()

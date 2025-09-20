#!/usr/bin/env python3
"""
Debug script to test login functionality step by step
"""
import streamlit as st
import sys
import os
sys.path.append('.')

from backend.database import login_user

def debug_login():
    st.title("Login Debug Test")

    st.write("This is a simplified login test to debug the issue.")

    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'user' not in st.session_state:
        st.session_state['user'] = None

    st.write(f"Current session state: logged_in={st.session_state['logged_in']}, user={st.session_state['user']}")

    if not st.session_state['logged_in']:
        st.subheader("Login Form")

        username_or_email = st.text_input('Username or Email', key='debug_username')
        password = st.text_input('Password', type='password', key='debug_password')

        if st.button('Login', key='debug_login_btn'):
            st.write(f"Attempting login with: {username_or_email}")

            user = login_user(username_or_email, password)
            if user:
                st.write(f"✅ Login successful! User: {user['username']}")
                st.session_state['user'] = user['username']
                st.session_state['logged_in'] = True
                st.write(f"Updated session state: logged_in={st.session_state['logged_in']}, user={st.session_state['user']}")
                st.success('Logged in successfully!')
                st.write("Click the button below to rerun and see the main app:")
                if st.button('Continue to Main App'):
                    st.rerun()
            else:
                st.write("❌ Login failed")
                st.error('Invalid credentials')
    else:
        st.success(f"Welcome back, {st.session_state['user']}!")
        st.write("You are successfully logged in.")

        if st.button('Logout'):
            st.session_state['user'] = None
            st.session_state['logged_in'] = False
            st.rerun()

if __name__ == "__main__":
    debug_login()

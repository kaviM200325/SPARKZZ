#!/usr/bin/env python3
"""
Test script to verify login functionality in Streamlit context
"""
import sys
import os
sys.path.append('.')

import streamlit as st
from backend.database import login_user

def test_streamlit_login():
    print("Testing login functionality in Streamlit context...")

    # Test with existing users
    test_cases = [
        ('hai', '123456'),
        ('hai@gmail.com', '123456'),
        ('kavi', '123456'),
        ('testuser', 'wrongpassword'),  # Should fail
    ]

    for username_or_email, password in test_cases:
        print(f"\nTesting: {username_or_email} / {password}")
        user = login_user(username_or_email, password)
        if user:
            print(f"✅ SUCCESS: User found - {user['username']}")
            print(f"   Email: {user['email']}")
            print(f"   Full name: {user['full_name']}")
        else:
            print("❌ FAILED: Invalid credentials")

    # Test session state simulation
    print("\n" + "="*50)
    print("Testing session state simulation...")

    # Simulate what happens in streamlit_app.py
    session_state = {}
    session_state['logged_in'] = False
    session_state['user'] = None

    print(f"Initial state: logged_in={session_state['logged_in']}, user={session_state['user']}")

    # Simulate successful login
    test_user = 'hai'
    test_pass = '123456'

    user = login_user(test_user, test_pass)
    if user:
        session_state['user'] = user['username']
        session_state['logged_in'] = True
        print(f"✅ Login successful: logged_in={session_state['logged_in']}, user={session_state['user']}")
    else:
        print("❌ Login failed")

if __name__ == "__main__":
    test_streamlit_login()

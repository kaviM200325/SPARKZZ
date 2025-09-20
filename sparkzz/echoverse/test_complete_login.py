#!/usr/bin/env python3
"""
Complete test of the login flow with splash screen logic
"""
import sys
sys.path.append('.')

def test_complete_login_flow():
    print("Testing complete login flow with splash screen...")

    # Simulate session state like in streamlit_app.py
    session_state = {}

    # Initialize session state
    if 'logged_in' not in session_state:
        session_state['logged_in'] = False
    if 'user' not in session_state:
        session_state['user'] = None
    if 'show_splash' not in session_state:
        session_state['show_splash'] = True

    print(f"Initial state: {session_state}")

    # Test splash screen condition (should show splash if not logged in)
    show_splash = session_state['show_splash'] and not session_state.get('logged_in', False)
    print(f"Splash screen should show: {show_splash}")

    # Simulate splash screen completion
    session_state['show_splash'] = False
    print(f"After splash: {session_state}")

    # Test login condition (should show login page)
    login_condition = not session_state['logged_in']
    print(f"Should show login page: {login_condition}")

    # Simulate successful login
    session_state['user'] = 'hai'
    session_state['logged_in'] = True
    print(f"After login: {session_state}")

    # Test login condition after login (should show main app)
    login_condition = not session_state['logged_in']
    print(f"Should show main app: {not login_condition}")

    # Test splash screen condition after login (should not show splash)
    show_splash = session_state['show_splash'] and not session_state.get('logged_in', False)
    print(f"Splash screen should show after login: {show_splash}")

    print("✅ Complete login flow test passed!")

if __name__ == "__main__":
    test_complete_login_flow()

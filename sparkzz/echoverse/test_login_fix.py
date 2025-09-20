#!/usr/bin/env python3
"""
Test script to verify login functionality
"""
import sys
import os
sys.path.append('.')

from backend.database import login_user

def test_login():
    print("Testing login functionality...")

    # Test with existing user
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
        else:
            print("❌ FAILED: Invalid credentials")

if __name__ == "__main__":
    test_login()

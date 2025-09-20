
import streamlit as st
import os
import time
from PIL import Image
from dotenv import load_dotenv
load_dotenv()
from backend.file_utils import save_uploaded_text, read_text_file, list_sample_files
from backend.ai import rewrite_text_tone, generate_audio_from_text, transcribe_audio
from backend.database import register_user, login_user

# Splash screen - only show if not logged in
if 'show_splash' not in st.session_state:
    st.session_state['show_splash'] = True

if st.session_state['show_splash'] and not st.session_state.get('logged_in', False):
    # Custom CSS for splash screen
    st.markdown("""
    <style>
    .splash-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: black;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        animation: fadeOut 3.5s ease-in-out 3s forwards;
    }
    .logo-container {
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
        animation: scaleIn 1s ease-out;
    }
    .center-circle {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: linear-gradient(to right, #fbbf24, #ea580c);
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 20px rgba(251, 191, 36, 0.5);
    }
    .center-circle span {
        color: black;
        font-size: 1.5rem;
        font-weight: bold;
        letter-spacing: 0.1em;
    }
    .glow-ring {
        position: absolute;
        width: 80px;
        height: 80px;
        border-radius: 50%;
        border: 2px solid #fbbf24;
        animation: expandFade 1.5s infinite;
    }
    .glow-ring:nth-child(2) {
        border-color: #ea580c;
        animation-duration: 1.8s;
        animation-delay: 0.5s;
    }
    .spark {
        position: absolute;
        width: 8px;
        height: 8px;
        background: #fbbf24;
        border-radius: 50%;
        box-shadow: 0 0 5px #fbbf24;
        animation: sparkBurst 1.5s infinite;
    }
    .spark:nth-child(1) { animation-delay: 0s; }
    .spark:nth-child(2) { animation-delay: 0.2s; }
    .spark:nth-child(3) { animation-delay: 0.4s; }
    .spark:nth-child(4) { animation-delay: 0.6s; }
    .spark:nth-child(5) { animation-delay: 0.8s; }
    .spark:nth-child(6) { animation-delay: 1.0s; }
    @keyframes scaleIn {
        from { transform: scale(0); }
        to { transform: scale(1); }
    }
    @keyframes expandFade {
        from { transform: scale(1); opacity: 0.8; }
        to { transform: scale(2.2); opacity: 0; }
    }
    @keyframes sparkBurst {
        0% { transform: scale(0); opacity: 0; }
        50% { transform: scale(1); opacity: 1; }
        100% { transform: scale(0); opacity: 0; }
    }
    @keyframes fadeOut {
        to { opacity: 0; visibility: hidden; }
    }
    </style>
    <div class="splash-container">
        <div class="logo-container">
            <div class="center-circle">
                <span>EV</span>
            </div>
            <div class="glow-ring"></div>
            <div class="glow-ring"></div>
            <div class="spark" style="transform: translate(40px, 0);"></div>
            <div class="spark" style="transform: translate(28px, 28px);"></div>
            <div class="spark" style="transform: translate(0, 40px);"></div>
            <div class="spark" style="transform: translate(-28px, 28px);"></div>
            <div class="spark" style="transform: translate(-40px, 0);"></div>
            <div class="spark" style="transform: translate(-28px, -28px);"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    time.sleep(3.5)
    st.session_state['show_splash'] = False
    st.rerun()

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user' not in st.session_state:
    st.session_state['user'] = None

# Debug: Print session state for troubleshooting
# st.write(f"DEBUG: logged_in = {st.session_state['logged_in']}, user = {st.session_state['user']}")

# Initialize page variable
page = 'Home'  # Default page

if not st.session_state['logged_in']:
    # Show login form directly without radio button navigation
    page = 'Login'

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

    login_container = st.container()
    with login_container:
        st.markdown('<div class="login-container">' , unsafe_allow_html=True)
        st.markdown('<div class="login-form">' , unsafe_allow_html=True)
        st.header('Welcome Back!')

        username_or_email = st.text_input('Username or Email', placeholder='Username or Email', label_visibility='collapsed')
        password = st.text_input('Password', type='password', placeholder='Password', label_visibility='collapsed')

        if st.button('Login'):
            # Debug: Print login attempt
            # st.write(f"DEBUG: Attempting login with {username_or_email}")

            user = login_user(username_or_email, password)
            if user:
                st.session_state['user'] = user['username']
                st.session_state['logged_in'] = True
                # st.write(f"DEBUG: Login successful, user set to {st.session_state['user']}")
                st.success('Logged in successfully!')
                st.rerun()
            else:
                # st.write(f"DEBUG: Login failed for {username_or_email}")
                st.error('Invalid credentials')
        st.markdown('</div>' , unsafe_allow_html=True)
        st.markdown('</div>' , unsafe_allow_html=True)

    # Add a link to register page
    st.markdown("---")
    if st.button('Need an account? Register here'):
        st.session_state['show_register'] = True
        st.rerun()

    if st.session_state.get('show_register', False):
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
                    st.session_state['show_register'] = False
                    st.rerun()
                else:
                    st.error('Username or email already exists')

        if st.button('Back to Login'):
            st.session_state['show_register'] = False
            st.rerun()

else:
    # Custom CSS for navbar styling
    st.markdown("""
    <style>
    .navbar {
        background: linear-gradient(135deg, #1e40af 0%, #3730a3 100%);
        padding: 1rem 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .navbar-left {
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
    }
    .navbar-title {
        color: white;
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
    }
    .navbar-subtitle {
        color: rgba(255,255,255,0.8);
        font-size: 0.9rem;
        margin: 0;
    }
    .navbar-right {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    .nav-links {
        display: flex;
        gap: 2rem;
        align-items: center;
    }
    .nav-link {
        color: rgba(255,255,255,0.9);
        text-decoration: none;
        font-weight: 500;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        transition: all 0.3s ease;
    }
    .nav-link:hover {
        background: rgba(255,255,255,0.1);
        color: white;
    }
    .nav-link.active {
        background: rgba(255,255,255,0.2);
        color: white;
        font-weight: 600;
    }
    .logout-btn {
        background: rgba(255,255,255,0.1);
        color: white;
        border: 1px solid rgba(255,255,255,0.3);
        padding: 0.5rem 1rem;
        border-radius: 6px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .logout-btn:hover {
        background: rgba(255,255,255,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

    # Navigation options
    page_names = ['Home', 'Upload & Convert', 'Transcribe Audio', 'Samples', 'Settings']

    # Create a radio button selection for navigation (hidden, just for state management)
    tab_selection = st.radio('Navigate', page_names, label_visibility='collapsed', horizontal=True)
    page_index = page_names.index(tab_selection)

    # Navbar HTML
    # Handle navigation changes
    if 'nav_trigger' not in st.session_state:
        st.session_state.nav_trigger = 0

    # JavaScript bridge for navigation
    st.markdown("""
    <script>
    // Check for navigation changes
    if (window.navSelection !== undefined && window.navSelection !== window.lastNavSelection) {
        window.lastNavSelection = window.navSelection;
        // Force rerun
        Streamlit.setComponentValue('nav_changed', window.navSelection);
    }

    // Check for logout
    if (window.logout) {
        window.logout = false;
        Streamlit.setComponentValue('user_logout', true);
    }
    </script>
    """, unsafe_allow_html=True)



# Route to selected page
selected_page = page_names[page_index]

if selected_page == 'Home':
    # Simple, clean home page using pure Streamlit components
    st.markdown("""
    <style>
    .hero-gradient {
        background: linear-gradient(135deg, #1e40af 0%, #3730a3 100%);
        padding: 3rem 2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-container {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #3b82f6;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    .feature-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    .feature-description {
        color: #6b7280;
        font-size: 0.9rem;
        line-height: 1.4;
    }
    .stats-container {
        background: #f8fafc;
        padding: 2rem;
        border-radius: 12px;
        margin: 2rem 0;
    }
    .stat-item {
        text-align: center;
        padding: 1rem;
    }
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: #3b82f6;
    }
    .stat-label {
        color: #6b7280;
        font-size: 0.9rem;
    }
    </style>
    """, unsafe_allow_html=True)

    # Hero Section
    st.markdown("""
    <div class="hero-gradient">
        <h1 style="font-size: 3rem; font-weight: 700; margin-bottom: 1rem;">EchoVerse</h1>
        <p style="font-size: 1.2rem; opacity: 0.9; margin-bottom: 0;">Professional AI-powered text-to-speech platform</p>
    </div>
    """, unsafe_allow_html=True)

    # Features Section
    st.subheader("Advanced Capabilities")

    # Feature 1
    st.markdown("""
    <div class="feature-container">
        <div class="feature-icon">📄</div>
        <div class="feature-title">Intelligent Text Processing</div>
        <div class="feature-description">Advanced AI algorithms process and optimize your text content, ensuring natural flow and pronunciation for superior audio output.</div>
    </div>
    """, unsafe_allow_html=True)

    # Feature 2
    st.markdown("""
    <div class="feature-container">
        <div class="feature-icon">🎭</div>
        <div class="feature-title">Dynamic Tone Control</div>
        <div class="feature-description">Choose from professional tone profiles - Corporate, Narrative, or Motivational - each optimized for specific content types and audiences.</div>
    </div>
    """, unsafe_allow_html=True)

    # Feature 3
    st.markdown("""
    <div class="feature-container">
        <div class="feature-icon">🎙️</div>
        <div class="feature-title">Premium Voice Synthesis</div>
        <div class="feature-description">Generate broadcast-quality audio using our advanced neural voice technology. Select from multiple professional voice profiles.</div>
    </div>
    """, unsafe_allow_html=True)

    # Feature 4
    st.markdown("""
    <div class="feature-container">
        <div class="feature-icon">⚡</div>
        <div class="feature-title">Audio Transcription</div>
        <div class="feature-description">Upload existing audio files for transcription. Then enhance and regenerate with improved tone, pacing, and voice selection.</div>
    </div>
    """, unsafe_allow_html=True)

    # Feature 5
    st.markdown("""
    <div class="feature-container">
        <div class="feature-icon">📚</div>
        <div class="feature-title">Content Library</div>
        <div class="feature-description">Access our curated collection of sample texts and audio examples to explore different tones and voices before creating your content.</div>
    </div>
    """, unsafe_allow_html=True)

    # Feature 6
    st.markdown("""
    <div class="feature-container">
        <div class="feature-icon">💾</div>
        <div class="feature-title">Professional Export</div>
        <div class="feature-description">Download your generated audio in multiple formats. Stream directly in your browser or integrate with professional audio workflows.</div>
    </div>
    """, unsafe_allow_html=True)

    # Statistics Section
    st.subheader("Platform Capabilities")
    st.markdown("""
    <div class="stats-container">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem;">
            <div class="stat-item">
                <div class="stat-number">3</div>
                <div class="stat-label">Professional Voices</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">3</div>
                <div class="stat-label">Tone Profiles</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">∞</div>
                <div class="stat-label">Content Length</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">24/7</div>
                <div class="stat-label">Processing</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Quick Action Buttons
    st.subheader("Quick Start")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button('📝 Text to Audio', use_container_width=True, type="primary"):
            tab_selection = 'Upload & Convert'
            st.rerun()

    with col2:
        if st.button('🎙️ Audio Transcription', use_container_width=True, type="primary"):
            tab_selection = 'Transcribe Audio'
            st.rerun()

    with col3:
        if st.button('📚 Sample Library', use_container_width=True, type="primary"):
            tab_selection = 'Samples'
            st.rerun()

if selected_page == 'Upload & Convert':
    st.header('Upload or Paste Text')
    uploaded = st.file_uploader('Upload a .txt file', type=['txt'])
    text_area = st.text_area('Or paste text here', height=240)

    if uploaded:
        path = save_uploaded_text(uploaded)
        text_area = read_text_file(path)
        st.success('File loaded.')

    tone = st.selectbox('Select tone for rewriting', ['Neutral', 'Suspenseful', 'Inspiring'])
    voice = st.selectbox('Select voice (TTS)', ['allison', 'michael', 'lisa'])
    out_name = st.text_input('Output filename (without ext)', 'echoverse_narration')

    if st.button('Rewrite & Generate Audio'):
        if not text_area.strip():
            st.error('Please provide text or upload a file first.')
        else:
            with st.spinner('Rewriting text...'):
                rewritten = rewrite_text_tone(text_area, tone)
            st.subheader('Comparison')
            st.markdown('**Original**')
            st.write(text_area[:3000])
            st.markdown('**Rewritten**')
            st.write(rewritten[:3000])

            with st.spinner('Generating audio...'):
                audio_path = generate_audio_from_text(rewritten, voice, f'{out_name}.mp3')

            st.audio(audio_path)
            with open(audio_path, 'rb') as f:
                st.download_button(label="Download MP3", data=f, file_name=os.path.basename(audio_path))

if selected_page == 'Transcribe Audio':
    st.header('Transcribe Audio')
    audio_file = st.file_uploader('Upload an audio file', type=['mp3'])
    if audio_file is not None:
        temp_audio_path = f'temp_audio_{audio_file.name}'
        try:
            with open(temp_audio_path, 'wb') as f:
                f.write(audio_file.read())
            with st.spinner('Transcribing audio...'):
                try:
                    transcription = transcribe_audio(temp_audio_path)
                    st.subheader('Transcription')
                    st.write(transcription)
                    tone = st.selectbox('Select tone for rewriting', ['Neutral', 'Suspenseful', 'Inspiring'], key='transcribe_tone')
                    voice = st.selectbox('Select voice (TTS)', ['allison', 'michael', 'lisa'], key='transcribe_voice')
                    out_name = st.text_input('Output filename (without ext)', 'echoverse_transcription', key='transcribe_out_name')
                    if st.button('Rewrite & Generate Audio', key='transcribe_generate'):
                        with st.spinner('Rewriting text...'):
                            rewritten = rewrite_text_tone(transcription, tone)
                        st.subheader('Comparison')
                        st.markdown('**Original Transcription**')
                        st.write(transcription[:3000])
                        st.markdown('**Rewritten**')
                        st.write(rewritten[:3000])
                        with st.spinner('Generating audio...'):
                            audio_path = generate_audio_from_text(rewritten, voice, f'{out_name}.mp3')
                        st.audio(audio_path)
                        with open(audio_path, 'rb') as f:
                            st.download_button(label="Download MP3", data=f, file_name=os.path.basename(audio_path))
                except Exception as e:
                    st.error(f"Transcription failed: {e}")
        finally:
            # Clean up temporary audio file
            if os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)

if selected_page == 'Samples':
    st.header('Sample texts')
    files = list_sample_files()
    for f in files:
        st.write(f)
        if st.button(f'Load {f}'):
            content = read_text_file(os.path.join('examples', f))
            st.query_params['sample'] = f
            st.write(content[:2000])

if selected_page == 'Settings':
    st.header('Settings')
    st.write('Text-to-speech uses gTTS (Google Text-to-Speech) to generate MP3 output with light dependencies.')
    st.write('Available voices: allison (US), michael (UK), lisa (AU).') 
import streamlit as st
import os
import json
from datetime import datetime

# Import tool functions directly
# Content Tools
from tools.content_tools import (
    render_text_generator,
    render_text_rewriter,
    render_academic_content,
    render_lesson_plan_generator,
    render_unit_plan_generator
)

# Assessment Tools
from tools.assessment_tools import (
    render_mcq_generator,
    render_hot_questions,
    render_text_dependent_questions,
    render_dok_questions,
    render_youtube_video_questions
)

# Support Tools
from tools.support_tools import (
    render_vocabulary_focus,
    render_text_proofreader,
    render_iep_goal_responder,
    render_standards_unpacker,
    render_image_generator
)

# Communication Tools
from tools.communication_tools import (
    render_prompt_builder,
    render_email_responder,
    render_email_template_maker,
    render_song_generator
)

# Create the tool mapping dictionary
tool_mapping = {
    # Content Tools
    "Text Generator": render_text_generator,
    "Text Rewriter": render_text_rewriter,
    "Academic Content": render_academic_content,
    "Lesson Plan Generator": render_lesson_plan_generator,
    "Unit Plan Generator": render_unit_plan_generator,
    
    # Assessment Tools
    "MCQ Generator": render_mcq_generator,
    "HOT Questions": render_hot_questions,
    "Text Dependent Questions": render_text_dependent_questions,
    "DOK Questions": render_dok_questions,
    "YouTube Video Questions": render_youtube_video_questions,
    
    # Support Tools
    "Vocabulary Focus": render_vocabulary_focus,
    "Text Proofreader": render_text_proofreader,
    "IEP Goal Responder": render_iep_goal_responder,
    "Standards Unpacker": render_standards_unpacker,
    "Image Generator": render_image_generator,
    
    # Communication Tools
    "Prompt Builder": render_prompt_builder,
    "Email Responder": render_email_responder,
    "Email Template Maker": render_email_template_maker,
    "Song Generator": render_song_generator
}

# Page configuration
st.set_page_config(
    page_title="Teacher Magic",
    page_icon="🧑‍🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
def load_css():
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Try to load CSS, with error handling if file doesn't exist
try:
    load_css()
except FileNotFoundError:
    st.warning("styles.css file not found. Some styling may be missing.")

# Initialize session state variables
if 'api_key' not in st.session_state:
    st.session_state['api_key'] = ""
if 'api_key_saved' not in st.session_state:
    st.session_state['api_key_saved'] = False
if 'history' not in st.session_state:
    st.session_state['history'] = []
if 'theme' not in st.session_state:
    st.session_state['theme'] = 'light'
if 'selected_tool' not in st.session_state:
    st.session_state['selected_tool'] = "Prompt Builder"  # Default tool

# Main title and toolbar
title_col, spacer, about_col, help_col, theme_col = st.columns([6, 1, 1, 1, 1])

with title_col:
    st.markdown("<div class='main-header'>Teacher Magic by G Stanyard</div>", unsafe_allow_html=True)

with about_col:
    if st.button("ℹ️ About", help="About the developer"):
        st.session_state['show_about'] = not st.session_state.get('show_about', False)

with help_col:
    if st.button("❓ Help", help="How to use Teacher Magic"):
        st.session_state['show_help'] = not st.session_state.get('show_help', False)

with theme_col:
    if st.button("🌓 Theme", help="Toggle light/dark mode"):
        st.session_state['theme'] = 'dark' if st.session_state['theme'] == 'light' else 'light'
        # Inject theme toggle JavaScript
        st.markdown(f"""
        <script>
            document.body.classList.remove('light-mode', 'dark-mode');
            document.body.classList.add('{st.session_state['theme']}-mode');
        </script>
        """, unsafe_allow_html=True)

# Show About modal
if st.session_state.get('show_about', False):
    with st.expander("About Teacher Magic", expanded=True):
        st.markdown("""
        ### About Teacher Magic
        
        Teacher Magic is made by Gary Stanyard for the benefit of colleagues in Brunei and beyond.
        
        Contact Gary at gstanyard@gmail.com
        
        This tool harnesses the power of AI to help teachers create high-quality educational content efficiently.
        """)
        if st.button("Close", key="close_about"):
            st.session_state['show_about'] = False
            st.rerun()

# Show Help modal
if st.session_state.get('show_help', False):
    with st.expander("How to Use Teacher Magic", expanded=True):
        st.markdown("""
        ### How to Use Teacher Magic
        
        1. **Get a Gemini API Key**:
           - You need a Google account
           - Visit [Google AI Studio](https://aistudio.google.com/apikey/)
           - Sign in and create a free API key
        
        2. **Configure the App**:
           - Enter your API key in the sidebar on the left
           - Click "Save API Key"
        
        3. **Select a Tool**:
           - Choose a tool from the sidebar
           - Fill in the required information
           - Click the generate button
        
        The API key is required before you can use any of the tools. Your API key is stored only in your browser's session and is not saved or transmitted anywhere except to Google's API.
        """)
        if st.button("Close", key="close_help"):
            st.session_state['show_help'] = False
            st.rerun()

# Sidebar with API Key entry and Tool Selection
with st.sidebar:
    st.markdown("### Setup")
    st.markdown("#### API Key")
    
    api_key_input = st.text_input(
        "Enter your Gemini API Key:",
        type="password",
        value=st.session_state['api_key'],
        help="Get a free API key from Google AI Studio: https://aistudio.google.com/apikey/"
    )
    
    if st.button("Save API Key"):
        st.session_state['api_key'] = api_key_input
        st.session_state['api_key_saved'] = True
        st.success("API Key saved for this session!")
    
    if st.session_state['api_key_saved']:
        st.success("API Key is configured!")
    
    st.markdown("---")
    
    # Tool Categories and Selection
    tool_categories = {
        "Core Tools": [
            "Prompt Builder"
        ],
        "Content Creation": [
            "Text Generator",
            "Text Rewriter",
            "Academic Content",
            "Lesson Plan Generator",
            "Unit Plan Generator",
            "Image Generator"
        ],
        "Assessment": [
            "MCQ Generator",
            "HOT Questions",
            "Text Dependent Questions",
            "DOK Questions",
            "YouTube Video Questions"
        ],
        "Student Support": [
            "Vocabulary Focus",
            "Text Proofreader",
            "IEP Goal Responder",
            "Standards Unpacker"
        ],
        "Communication": [
            "Email Responder",
            "Email Template Maker",
            "Song Generator"
        ]
    }
    
    st.markdown("### Tool Categories")
    
    # Convert nested dictionary to flat list for the radio button
    all_tools = []
    for category, tools in tool_categories.items():
        all_tools.extend(tools)
    
    # Use radio buttons for tool selection (cleaner UI)
    selected_tool = st.radio("Select a Tool:", all_tools, index=all_tools.index(st.session_state['selected_tool']))
    
    # Update session state when selection changes
    if selected_tool != st.session_state['selected_tool']:
        st.session_state['selected_tool'] = selected_tool
        st.rerun()

# Add history and export function at the bottom
with st.expander("📜 History & Export", expanded=False):
    if len(st.session_state['history']) > 0:
        st.download_button(
            label="Download History (JSON)",
            data=get_history_json(),
            file_name=f"teacher_magic_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
        
        # Display recent history
        st.markdown("### Recent Activity")
        for i, item in enumerate(st.session_state['history'][:5]):  # Show last 5 items
            st.markdown(f"**{item['timestamp']} - {item['tool']}**")
            # Use HTML details instead of nested expander
            st.markdown("<details><summary>View Details</summary>", unsafe_allow_html=True)
            st.write("Inputs:", item['inputs'])
            st.markdown("Result:")
            st.markdown(item['result'])
            st.markdown("</details>", unsafe_allow_html=True)
        
        if len(st.session_state['history']) > 5:
            st.markdown(f"*...and {len(st.session_state['history']) - 5} more items*")
    else:
        st.info("No history yet. Use the tools above to generate content!")

# Render the selected tool
if selected_tool in tool_mapping:
    tool_mapping[selected_tool]()
else:
    st.error(f"Tool '{selected_tool}' not found. Please select another tool.")

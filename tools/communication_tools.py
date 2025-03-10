# tools/communication_tools.py
import streamlit as st
from utils.api import call_gemini_api
from utils.data import save_to_history

def display_result(title, content):
    """Display the result in a formatted area."""
    st.markdown(f"### {title}")
    st.markdown(f"<div class='result-area'>{content}</div>", unsafe_allow_html=True)

# Tool 1: Prompt Builder
def render_prompt_builder():
    """Render the Prompt Builder tool."""
    st.markdown("<div class='sub-header'>🔧 AI Prompt Builder</div>", unsafe_allow_html=True)
    
    with st.form(key="prompt_builder_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            role = st.text_input("AI Role (e.g., science teacher, language tutor)", 
                                placeholder="Enter the role for the AI")
            outcome = st.text_input("Desired Outcome (e.g., lesson plan, quiz, explanation)", 
                                   placeholder="What do you want the AI to create?")
            
        with col2:
            audience = st.text_input("Target Audience (e.g., 5th grade students, ESL learners)", 
                                    placeholder="Who is this for?")
            avoid = st.text_input("Avoid (optional)", 
                                 placeholder="What should the AI avoid?")
        
        example = st.text_area("Include Examples or Specific Instructions (optional)", 
                               placeholder="Any specific format, examples, or instructions?")
        
        submit_button = st.form_submit_button(label="Build Prompt")
    
    if submit_button:
        if not role or not outcome or not audience:
            st.error("Please fill in all required fields: Role, Outcome, and Audience.")
        else:
            components = [
                f"Act as a {role.strip()}",
                f"to produce {outcome.strip()}",
                f"for {audience.strip()}"
            ]
            
            if avoid and avoid.strip():
                components.append(f"Avoid: {avoid.strip()}")
            if example and example.strip():
                components.append(f"Include: {example.strip()}")
            
            final_prompt = ". ".join(components) + "."
            
            display_result("Your AI Prompt", final_prompt)
            
            # Add copy button
            st.text("")
            if st.button("Copy to Clipboard"):
                st.code(final_prompt)
                st.success("Prompt copied to clipboard! (Use Ctrl+C)")
            
            # Save to history
            save_to_history(st.session_state, "Prompt Builder", 
                           {"role": role, "outcome": outcome, "audience": audience, 
                            "avoid": avoid, "example": example}, 
                           final_prompt)

# Tool 2: Email Responder
def render_email_responder():
    """Render the Email Responder tool."""
    st.markdown("<div class='sub-header'>✉️ Email Responder</div>", unsafe_allow_html=True)
    
    with st.form(key="email_responder_form"):
        email_scenario = st.selectbox("Email Scenario", 
                                   options=["Parent Concern/Complaint", "Parent Question", "Student Question/Request", 
                                            "Administrator Communication", "Colleague Collaboration", 
                                            "Event/Activity Planning", "Other"])
        
        email_content = st.text_area("Original Email/Context", 
                                   placeholder="Paste the email you received or describe the situation...",
                                   height=150)
        
        col1, col2 = st.columns(2)
        
        with col1:
            response_tone = st.selectbox("Response Tone", 
                                       options=["Professional", "Supportive", "Firm but Kind", 
                                                "Enthusiastic", "Formal", "Informative"])
            include_elements = st.multiselect("Include Elements", 
                                           options=["Greeting", "Acknowledgment", "Information/Answer", 
                                                   "Next Steps", "Resources", "Invitation for Follow-up", "Closing"],
                                           default=["Greeting", "Acknowledgment", "Information/Answer", "Closing"])
        
        with col2:
            response_length = st.selectbox("Response Length", 
                                        options=["Brief (1-2 paragraphs)", "Standard (3-4 paragraphs)", "Detailed (5+ paragraphs)"])
            language = st.selectbox("Language", options=["English", "Bahasa Melayu"])
        
        key_points = st.text_area("Key Points to Include", 
                               placeholder="List specific points you want to address in your response...",
                               height=100)
        
        submit_button = st.form_submit_button(label="Generate Email Response")
    
    if submit_button:
        if not email_content:
            st.error("Please provide the original email or context.")
        else:
            with st.spinner("Generating email response..."):
                # Join include elements with commas
                elements_str = ", ".join(include_elements)
                
                prompt = f"""
                Generate a professional email response in {language} for this {email_scenario} scenario:
                
                Original email/context:
                ---
                {email_content}
                ---
                
                Key points to include:
                {key_points if key_points else "Respond appropriately to the email content provided."}
                
                Write a {response_length} response with a {response_tone} tone.
                Include these elements: {elements_str}
                
                Guidelines:
                1. Be professional, clear, and respectful
                2. Address the specific concerns or questions raised
                3. Maintain appropriate teacher-student or teacher-parent boundaries
                4. Provide concrete information or next steps when appropriate
                5. Avoid making promises that cannot be kept
                6. Use language appropriate for the recipient
                
                Format the email with appropriate spacing and structure.
                """
                
                result = call_gemini_api(prompt, st.session_state['api_key'])
                
                if result:
                    display_result("Generated Email Response", result)
                    
                    # Save to history
                    save_to_history(st.session_state, "Email Responder", 
                                   {"email_scenario": email_scenario, 
                                    "email_content": email_content[:100] + "..." if len(email_content) > 100 else email_content, 
                                    "response_tone": response_tone, "response_length": response_length}, 
                                   result)

# Tool 3: Email Template Maker
def render_email_template_maker():
    """Render the Email Template Maker tool."""
    st.markdown("<div class='sub-header'>📧 Email Template Maker</div>", unsafe_allow_html=True)
    
    with st.form(key="email_template_form"):
        email_type = st.selectbox("Email Type", 
                               options=["Parent Newsletter", "Class Announcement", "Event Invitation", 
                                        "Project Information", "Field Trip Details", "Classroom Updates", 
                                        "Beginning of Year/Term", "End of Year/Term"])
        
        col1, col2 = st.columns(2)
        
        with col1:
            grade_level = st.selectbox("Grade/Class Level", 
                                     options=["Primary (1-3)", "Primary (4-6)", "Secondary (7-9)", "Secondary (10-12)"])
            subject_area = st.selectbox("Subject Area (if applicable)", 
                                     options=["General", "Mathematics", "Language Arts", "Science", "Social Studies", 
                                              "Arts", "Physical Education", "Multiple Subjects"])
        
        with col2:
            communication_style = st.selectbox("Communication Style", 
                                            options=["Formal", "Conversational", "Enthusiastic", "Informative"])
            language = st.selectbox("Language", options=["English", "Bahasa Melayu"])
        
        key_information = st.text_area("Key Information to Include", 
                                     placeholder="List the important details, dates, requirements, etc. to include...",
                                     height=150)
        
        submit_button = st.form_submit_button(label="Generate Email Template")
    
    if submit_button:
        if not key_information:
            st.error("Please provide key information to include in the email.")
        else:
            with st.spinner("Generating email template..."):
                prompt = f"""
                Create a {email_type} email in {language} for {grade_level} {subject_area} class using a {communication_style} communication style.
                
                Include the following key information:
                {key_information}
                
                Guidelines:
                1. Create a clear, attention-grabbing subject line
                2. Use an appropriate greeting/introduction
                3. Present information in a well-organized, easy-to-scan format
                4. Include all necessary details (who, what, when, where, why, how)
                5. Specify any actions recipients need to take and deadlines
                6. Include contact information for questions or clarifications
                7. End with an appropriate closing
                
                Format the email with appropriate spacing, bullet points, and structure for easy reading.
                """
                
                result = call_gemini_api(prompt, st.session_state['api_key'])
                
                if result:
                    display_result("Generated Email Template", result)
                    
                    # Save to history
                    save_to_history(st.session_state, "Email Template Maker", 
                                   {"email_type": email_type, "grade_level": grade_level, 
                                    "subject_area": subject_area, "communication_style": communication_style,
                                    "key_information": key_information[:100] + "..." if len(key_information) > 100 else key_information}, 
                                   result)

# Tool 4: Song Generator
def render_song_generator():
    """Render the Song Generator tool."""
    st.markdown("<div class='sub-header'>🎵 Educational Song Generator</div>", unsafe_allow_html=True)
    
    with st.form(key="song_generator_form"):
        topic = st.text_input("Educational Topic", placeholder="e.g., Water Cycle, Multiplication, Parts of Speech")
        
        col1, col2 = st.columns(2)
        
        with col1:
            grade_level = st.selectbox("Grade Level", 
                                     options=["Early Childhood", "Primary (1-3)", "Primary (4-6)", 
                                              "Secondary (7-9)", "Secondary (10-12)"])
            song_style = st.selectbox("Song Style", 
                                    options=["Simple Rhyme", "Nursery Rhyme", "Rap/Hip-Hop", "Pop Song", 
                                             "Folk Song", "Chant/Call and Response", "Parody of Known Song"])
        
        with col2:
            song_length = st.selectbox("Song Length", 
                                     options=["Short (1 verse + chorus)", "Medium (2 verses + chorus)", 
                                              "Full Song (3+ verses + chorus)"])
            language = st.selectbox("Language", options=["English", "Bahasa Melayu"])
        
        key_concepts = st.text_area("Key Concepts to Include", 
                                  placeholder="List the important terms, facts, or concepts that should be in the song...",
                                  height=100)
        
        melody_note = st.text_input("Melody Note (Optional)", 
                                 placeholder="e.g., 'Sung to the tune of Twinkle Twinkle' or 'Original melody'")
        
        submit_button = st.form_submit_button(label="Generate Educational Song")
    
    if submit_button:
        if not topic:
            st.error("Please enter an educational topic.")
        else:
            with st.spinner("Composing educational song..."):
                prompt = f"""
                Create an educational song in {language} about {topic} for {grade_level} students.
                
                Song specifications:
                - Style: {song_style}
                - Length: {song_length}
                - Key concepts to include: {key_concepts if key_concepts else topic}
                {f"- Melody note: {melody_note}" if melody_note else ""}
                
                The song should:
                1. Be age-appropriate for {grade_level} students
                2. Contain accurate educational content about {topic}
                3. Use rhyme, rhythm, and repetition to aid memory
                4. Be engaging and fun to sing/perform
                5. Include movements or actions if appropriate
                
                Format your response with:
                1. A catchy title for the song
                2. Lyrics clearly formatted with verses and chorus labeled
                3. Performance notes (suggested movements, instruments, or teaching tips)
                4. Brief explanation of how the song addresses key learning objectives
                """
                
                result = call_gemini_api(prompt, st.session_state['api_key'])
                
                if result:
                    display_result("Generated Educational Song", result)
                    
                    # Save to history
                    save_to_history(st.session_state, "Song Generator", 
                                   {"topic": topic, "grade_level": grade_level, 
                                    "song_style": song_style, "song_length": song_length,
                                    "key_concepts": key_concepts}, 
                                   result)

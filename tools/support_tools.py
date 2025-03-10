# tools/support_tools.py
import streamlit as st
from utils.api import call_gemini_api
from utils.data import save_to_history

def display_result(title, content):
    """Display the result in a formatted area."""
    st.markdown(f"### {title}")
    st.markdown(f"<div class='result-area'>{content}</div>", unsafe_allow_html=True)

# Tool 1: Vocabulary Focus
def render_vocabulary_focus():
    """Render the Vocabulary Focus tool."""
    st.markdown("<div class='sub-header'>📖 Vocabulary Focus</div>", unsafe_allow_html=True)
    
    with st.form(key="vocab_focus_form"):
        vocabulary = st.text_area("Enter vocabulary words (comma-separated)", 
                                placeholder="e.g., photosynthesis, ecosystem, habitat, predator")
        
        col1, col2 = st.columns(2)
        
        with col1:
            grade_level = st.selectbox("Grade Level", 
                                     options=["Primary (1-3)", "Primary (4-6)", "Secondary (7-9)", "Secondary (10-12)"])
            language = st.selectbox("Language", options=["English", "Bahasa Melayu"])
        
        with col2:
            output_type = st.selectbox("Output Type", 
                                     options=["Vocabulary MCQs", "Word Maps", "Sentence Frames", "Vocabulary Activities"])
        
        submit_button = st.form_submit_button(label="Generate Vocabulary Resources")
    
    if submit_button:
        if not vocabulary:
            st.error("Please enter vocabulary words.")
        else:
            with st.spinner("Generating vocabulary resources..."):
                vocab_list = [word.strip() for word in vocabulary.split(",")]
                
                if output_type == "Vocabulary MCQs":
                    prompt = f"""
                    You are an MCQ generator for {grade_level} students. Create vocabulary MCQs in {language} for these words: {vocabulary}
                    1. Include definition, synonym, and usage questions
                    2. Format response:
                       Q: [Question]
                       A: [Option A] | [Option B] | [Option C] | [Option D]
                       Correct: [Letter]
                       Explanation: [Brief rationale]
                       Concepts: [Comma-separated concepts]

                    Example:
                    Q: What does "photosynthesis" mean?
                    A: Plant growth | Light-to-energy | Water process | Gas exchange
                    Correct: B
                    Explanation: Photosynthesis changes light energy to chemical energy
                    Concepts: biology, energy
                    """
                    
                elif output_type == "Word Maps":
                    prompt = f"""
                    Create detailed word maps for these vocabulary terms: {vocabulary}
                    
                    For each word in {language}, provide:
                    1. Word: [vocabulary word]
                    2. Definition: [simple, grade-appropriate definition for {grade_level}]
                    3. Synonyms: [2-3 synonyms]
                    4. Antonyms: [2-3 antonyms if applicable]
                    5. Examples: [2-3 concrete examples]
                    6. Non-examples: [1-2 non-examples to clarify meaning]
                    7. Visual cue: [brief description of an image that represents the word]
                    8. Use in a sentence: [example sentence appropriate for {grade_level}]
                    9. Word parts: [prefix, root, suffix if applicable]
                    
                    Format each word map clearly with headings and bullet points.
                    """
                    
                elif output_type == "Sentence Frames":
                    prompt = f"""
                    Create sentence frames for {grade_level} students to practice using these vocabulary words: {vocabulary}
                    
                    For each word in {language}, provide:
                    1. Basic sentence frame (simple usage)
                    2. Intermediate sentence frame (more complex usage)
                    3. Advanced sentence frame (critical thinking)
                    4. Question frame (to prompt discussion)
                    5. Comparison frame (to compare concepts)
                    
                    Each frame should have blanks for students to fill in, but should guide them to use the vocabulary word correctly.
                    
                    Example for "ecosystem":
                    Basic: An ecosystem includes living things such as _______ and non-living things such as _______.
                    Intermediate: In the _______ ecosystem, _______ are producers because they _______.
                    Advanced: When _______ happens in an ecosystem, it affects _______ because _______.
                    Question: How might the _______ in this ecosystem be affected if _______?
                    Comparison: The _______ ecosystem is different from the _______ ecosystem because _______.
                    """
                    
                else:  # Vocabulary Activities
                    prompt = f"""
                    Create 5 engaging vocabulary activities for {grade_level} students to learn these words: {vocabulary}
                    
                    Each activity in {language} should:
                    1. Have a clear title and purpose
                    2. Include step-by-step instructions
                    3. Specify materials needed
                    4. Include examples of how to use the vocabulary words
                    5. Be appropriate for {grade_level} students
                    6. Take 10-15 minutes to complete
                    
                    Include a mix of individual, pair, and group activities that address different learning styles (visual, auditory, kinesthetic).
                    Each activity should deeply engage students with the meaning and usage of the vocabulary words.
                    """
                
                result = call_gemini_api(prompt, st.session_state['api_key'])
                
                if result:
                    display_result(f"Generated {output_type}", result)
                    
                    # Save to history
                    save_to_history(st.session_state, "Vocabulary Focus", 
                                   {"vocabulary": vocabulary, "grade_level": grade_level, 
                                    "output_type": output_type, "language": language}, 
                                   result)

# Tool 2: Text Proofreader
def render_text_proofreader():
    """Render the Text Proofreader tool."""
    st.markdown("<div class='sub-header'>✏️ Text Proofreader</div>", unsafe_allow_html=True)
    
    with st.form(key="text_proofreader_form"):
        original_text = st.text_area("Text to Proofread", 
                                   placeholder="Paste student writing or your text here...",
                                   height=200)
        
        col1, col2 = st.columns(2)
        
        with col1:
            grade_level = st.selectbox("Grade/Writing Level", 
                                     options=["Primary (1-3)", "Primary (4-6)", "Secondary (7-9)", "Secondary (10-12)", "College"])
            focus_areas = st.multiselect("Focus Areas", 
                                       options=["Grammar", "Spelling", "Punctuation", "Sentence Structure", 
                                                "Vocabulary", "Clarity", "Organization", "Style"],
                                       default=["Grammar", "Spelling", "Punctuation"])
        
        with col2:
            feedback_tone = st.selectbox("Feedback Tone", 
                                       options=["Supportive", "Direct", "Academic", "Detailed", "Simplified"])
            language = st.selectbox("Language", options=["English", "Bahasa Melayu"])
        
        submit_button = st.form_submit_button(label="Proofread Text")
    
    if submit_button:
        if not original_text:
            st.error("Please enter text to proofread.")
        else:
            with st.spinner("Proofreading text..."):
                # Join focus areas with commas
                focus_str = ", ".join(focus_areas)
                
                prompt = f"""
                Proofread the following text in {language} as if it were written by a {grade_level} student. 
                Use a {feedback_tone} tone in your feedback.
                
                Focus particularly on these areas: {focus_str}
                
                Text to proofread:
                ---
                {original_text}
                ---
                
                Please provide:
                
                1. An overall assessment of the writing (2-3 sentences)
                2. Specific corrections for errors (clearly mark what needs to be changed)
                3. Positive feedback on strengths (at least 2 points)
                4. Suggestions for improvement (2-3 specific, actionable suggestions)
                5. A revised/corrected version of the text
                
                Format your response clearly with sections for each type of feedback.
                """
                
                result = call_gemini_api(prompt, st.session_state['api_key'])
                
                if result:
                    display_result("Proofreading Results", result)
                    
                    # Save to history
                    save_to_history(st.session_state, "Text Proofreader", 
                                   {"original_text": original_text[:100] + "..." if len(original_text) > 100 else original_text, 
                                    "grade_level": grade_level, "focus_areas": focus_str,
                                    "feedback_tone": feedback_tone}, 
                                   result)

# Tool 3: IEP Goal Responder
def render_iep_goal_responder():
    """Render the IEP Goal Responder tool."""
    st.markdown("<div class='sub-header'>🎯 IEP Goal Responder</div>", unsafe_allow_html=True)
    
    with st.form(key="iep_goal_form"):
        student_needs = st.text_area("Student Needs/Challenges", 
                                   placeholder="Describe the student's specific needs, challenges, or areas for development...",
                                   height=100)
        
        col1, col2 = st.columns(2)
        
        with col1:
            grade_level = st.selectbox("Grade Level", 
                                     options=["Primary (1-3)", "Primary (4-6)", "Secondary (7-9)", "Secondary (10-12)"])
            subject_areas = st.multiselect("Subject/Skill Areas", 
                                         options=["Reading", "Writing", "Mathematics", "Science", "Social Skills", 
                                                 "Communication", "Executive Function", "Motor Skills", "Behavior", "Self-Regulation"],
                                         default=["Reading", "Writing"])
        
        with col2:
            time_frame = st.selectbox("Time Frame", 
                                    options=["Quarter", "Semester", "School Year"])
            language = st.selectbox("Language", options=["English", "Bahasa Melayu"])
        
        current_levels = st.text_area("Current Performance Levels (Optional)", 
                                   placeholder="Describe what the student can currently do in these areas...",
                                   height=100)
        
        submit_button = st.form_submit_button(label="Generate IEP Goals")
    
    if submit_button:
        if not student_needs:
            st.error("Please describe the student's needs/challenges.")
        else:
            with st.spinner("Generating IEP goals..."):
                # Join subject areas with commas
                subjects_str = ", ".join(subject_areas)
                
                prompt = f"""
                Create Individualized Education Program (IEP) goals in {language} for a {grade_level} student with the following needs:
                
                Student Needs/Challenges:
                {student_needs}
                
                {f"Current Performance Levels:\n{current_levels}" if current_levels else ""}
                
                Generate 1-2 SMART goals for each of these areas: {subjects_str}
                Each goal should be designed for a {time_frame} time frame.
                
                For each goal, include:
                
                1. The SMART goal statement (Specific, Measurable, Achievable, Relevant, Time-bound)
                2. 2-3 specific benchmarks or short-term objectives that lead to the goal
                3. Suggested accommodations or modifications to support the goal
                4. 2-3 specific strategies that educators and parents can use to support progress
                5. Ideas for measuring and documenting progress
                
                Format each goal clearly with headings and bullet points.
                """
                
                result = call_gemini_api(prompt, st.session_state['api_key'])
                
                if result:
                    display_result("Generated IEP Goals", result)
                    
                    # Save to history
                    save_to_history(st.session_state, "IEP Goal Responder", 
                                   {"student_needs": student_needs[:100] + "..." if len(student_needs) > 100 else student_needs, 
                                    "grade_level": grade_level, "subject_areas": subjects_str,
                                    "time_frame": time_frame}, 
                                   result)

# Tool 4: Standards Unpacker
def render_standards_unpacker():
    """Render the Standards Unpacker tool."""
    st.markdown("<div class='sub-header'>📋 Standards Unpacker</div>", unsafe_allow_html=True)
    
    with st.form(key="standards_unpacker_form"):
        standard_text = st.text_area("Standard Text", 
                                   placeholder="Paste the educational standard or learning objective here...",
                                   height=100)
        
        col1, col2 = st.columns(2)
        
        with col1:
            subject = st.selectbox("Subject Area", 
                                 options=["Mathematics", "English Language Arts", "Science", "Social Studies", 
                                          "Arts", "Physical Education", "Technology", "Other"])
            grade_level = st.selectbox("Grade Level", 
                                     options=["Primary (1-3)", "Primary (4-6)", "Secondary (7-9)", "Secondary (10-12)"])
        
        with col2:
            curriculum_framework = st.selectbox("Curriculum Framework (if applicable)", 
                                             options=["General", "Common Core", "NGSS", "IGCSE", "IB", "National Curriculum", "Other"])
            language = st.selectbox("Language", options=["English", "Bahasa Melayu"])
        
        submit_button = st.form_submit_button(label="Unpack Standard")
    
    if submit_button:
        if not standard_text:
            st.error("Please enter a standard to unpack.")
        else:
            with st.spinner("Unpacking standard..."):
                prompt = f"""
                Unpack the following {subject} educational standard for {grade_level} students from the {curriculum_framework} framework. Provide your analysis in {language}.
                
                Standard:
                {standard_text}
                
                Please provide:
                
                1. A simplified explanation of what this standard means (teacher-friendly language)
                2. A breakdown of the key skills and knowledge students need to demonstrate
                3. The prerequisite knowledge/skills students should have before addressing this standard
                4. 3-4 clear "I can" statements that students could use to understand the standard
                5. 2-3 ways to assess mastery of this standard
                6. At least 3 specific instructional strategies or activities that would help teach this standard
                7. Potential challenges students might face in mastering this standard and how to address them
                8. How this standard connects to previous and future learning in the curriculum
                
                Format your response in clear sections with headings for easy reference.
                """
                
                result = call_gemini_api(prompt, st.session_state['api_key'])
                
                if result:
                    display_result("Unpacked Standard", result)
                    
                    # Save to history
                    save_to_history(st.session_state, "Standards Unpacker", 
                                   {"standard_text": standard_text[:100] + "..." if len(standard_text) > 100 else standard_text, 
                                    "subject": subject, "grade_level": grade_level,
                                    "curriculum_framework": curriculum_framework}, 
                                   result)

# Tool 5: Image Generator
def render_image_generator():
    """Render the Image Generator tool."""
    st.markdown("<div class='sub-header'>🖼️ Image Generator Prompts</div>", unsafe_allow_html=True)
    st.markdown("""
    This tool helps you create prompts for image generation tools like Adobe Firefly, DALL-E, or Midjourney.
    """)
    
    with st.form(key="image_generator_form"):
        subject = st.text_input("Subject/Concept", 
                             placeholder="e.g., photosynthesis, water cycle, division, historical event")
        
        col1, col2 = st.columns(2)
        
        with col1:
            image_type = st.selectbox("Image Type", 
                                    options=["Diagram", "Illustration", "Infographic", "Chart/Graph", 
                                             "Comic/Cartoon", "Timeline", "Map", "Process Flow"])
            style = st.selectbox("Visual Style", 
                               options=["Simple/Clear", "Colorful/Engaging", "Realistic", "Cartoon", 
                                        "Minimalist", "Hand-drawn", "Technical", "3D"])
        
        with col2:
            audience = st.selectbox("Target Audience", 
                                  options=["Early Elementary", "Upper Elementary", "Middle School", 
                                           "High School", "College", "Adult Learners"])
            purpose = st.selectbox("Educational Purpose", 
                                 options=["Explain Concept", "Compare/Contrast", "Show Process", 
                                          "Visualize Data", "Engage Interest", "Assessment", "Review"])
        
        specific_elements = st.text_area("Specific Elements to Include", 
                                       placeholder="e.g., labels, arrows, specific parts or steps")
        
        submit_button = st.form_submit_button(label="Generate Image Prompt")
    
    if submit_button:
        if not subject:
            st.error("Please enter a subject/concept.")
        else:
            with st.spinner("Creating image generation prompt..."):
                prompt = f"""
                Create a detailed prompt that can be used with image generation AI tools like DALL-E, Midjourney, or Adobe Firefly to create an educational image.
                
                The prompt should describe:
                
                1. An educational {image_type} about {subject}
                2. In a {style} visual style
                3. Appropriate for {audience} students
                4. Designed to {purpose}
                5. Including these specific elements: {specific_elements if specific_elements else "clear labels and visual cues"}
                
                Provide:
                1. A concise image generation prompt (1-3 sentences)
                2. A detailed image generation prompt (paragraph with specifics)
                3. A list of 3-5 suggestions for how to use this image in teaching
                """
                
                result = call_gemini_api(prompt, st.session_state['api_key'])
                
                if result:
                    display_result("Image Generation Prompt", result)
                    
                    # Save to history
                    save_to_history(st.session_state, "Image Generator", 
                                   {"subject": subject, "image_type": image_type, 
                                    "style": style, "audience": audience, "purpose": purpose}, 
                                   result)

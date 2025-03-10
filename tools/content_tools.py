# tools/content_tools.py
import streamlit as st
import math
from utils.api import call_gemini_api
from utils.data import load_educational_data, save_to_history

def display_result(title, content):
    """Display the result in a formatted area."""
    st.markdown(f"### {title}")
    st.markdown(f"<div class='result-area'>{content}</div>", unsafe_allow_html=True)

# Tool 1: Text Generator
def render_text_generator():
    """Render the Text Generator tool."""
    st.markdown("<div class='sub-header'>📄 Text Generator</div>", unsafe_allow_html=True)
    
    with st.form(key="text_generator_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            lexile_score = st.slider("Lexile Score", min_value=200, max_value=1600, value=800, step=50,
                                  help="Higher values create more complex text")
            language = st.selectbox("Language", options=["English", "Bahasa Melayu"])
        
        with col2:
            subject = st.selectbox("Subject", 
                                 options=["Science", "History", "Literature", "Social Studies", "General Knowledge"])
            text_type = st.selectbox("Text Type", 
                                   options=["Informational", "Narrative", "Persuasive", "Procedural", "Descriptive"])
        
        vocabulary = st.text_area("Target Vocabulary (comma-separated)", 
                                placeholder="e.g., analyze, compare, evaluate, synthesize")
        topic = st.text_input("Topic", placeholder="e.g., Water Cycle, American Revolution")
        
        submit_button = st.form_submit_button(label="Generate Text")
    
    if submit_button:
        if not topic:
            st.error("Please enter a topic.")
        else:
            with st.spinner("Generating text..."):
                # Calculate reading level parameters based on lexile
                readingEase = max(0, min(100, -0.0721 * lexile_score + 120))
                avgSyllables = 1 + 0.2 * math.log(lexile_score / 100)
                complexWordPct = min(0.4, 0.05 * math.log(lexile_score))
                avgSentenceLength = (206.835 - readingEase - 84.6 * avgSyllables) / 1.015
                
                # Format vocabulary
                vocab_list = [word.strip() for word in vocabulary.split(",")] if vocabulary else []
                
                prompt = f"""
                Generate a 250-300 word {text_type.lower()} text about "{topic}" in {language} that:
                
                1. Is appropriate for a Lexile level of {lexile_score} 
                2. Is related to {subject}
                3. Follows these reading metrics:
                   - Reading Ease: {readingEase:.1f}
                   - Average syllables per word: {avgSyllables:.2f}
                   - Complex words percentage: {complexWordPct*100:.1f}%
                   - Average sentence length: {avgSentenceLength:.1f} words
                
                {f"4. Incorporates these vocabulary words: {', '.join(vocab_list)}" if vocab_list else ""}
                
                The text should be engaging, accurate, and educational. Include a title for the text.
                Ensure the content is age-appropriate and maintains a natural flow while adhering to the metrics.
                """
                
                result = call_gemini_api(prompt, st.session_state['api_key'])
                
                if result:
                    display_result("Generated Text", result)
                    
                    # Calculate approximate word count
                    word_count = len(result.split())
                    st.info(f"Approximate word count: {word_count}")
                    
                    # Save to history
                    save_to_history(st.session_state, "Text Generator", 
                                   {"lexile_score": lexile_score, "topic": topic, 
                                    "subject": subject, "text_type": text_type, "vocabulary": vocabulary}, 
                                   result)

# Tool 2: Text Rewriter
def render_text_rewriter():
    """Render the Text Rewriter tool."""
    st.markdown("<div class='sub-header'>📝 Text Rewriter</div>", unsafe_allow_html=True)
    
    with st.form(key="text_rewriter_form"):
        original_text = st.text_area("Original Text", 
                                   placeholder="Paste the text you want to rewrite here...",
                                   height=200)
        
        col1, col2 = st.columns(2)
        
        with col1:
            reading_level = st.selectbox("Target Reading Level", 
                                      options=["Elementary (Grades 1-5)", "Middle School (Grades 6-8)", 
                                               "High School (Grades 9-12)", "College", "Advanced"])
            language = st.selectbox("Language", options=["English", "Bahasa Melayu"])
        
        with col2:
            style = st.selectbox("Writing Style", 
                               options=["Simplified", "Academic", "Conversational", "Engaging", "Technical", "Creative"])
            purpose = st.selectbox("Purpose", 
                                 options=["Instruction", "Explanation", "Retention", "Engagement", "Assessment"])
        
        submit_button = st.form_submit_button(label="Rewrite Text")
    
    if submit_button:
        if not original_text:
            st.error("Please enter text to rewrite.")
        else:
            with st.spinner("Rewriting text..."):
                prompt = f"""
                Rewrite the following text for {reading_level} students in a {style} style for {purpose} purposes in {language}:

                ---
                {original_text}
                ---

                Guidelines:
                1. Maintain the core meaning and key information
                2. Adjust vocabulary and sentence complexity to match {reading_level} level
                3. Use {style} tone and structure
                4. Format the text to support {purpose}
                5. Ensure the rewritten text is clear, coherent, and effective for the target audience
                """
                
                result = call_gemini_api(prompt, st.session_state['api_key'])
                
                if result:
                    display_result("Rewritten Text", result)
                    
                    # Calculate change in complexity
                    original_words = len(original_text.split())
                    new_words = len(result.split())
                    word_diff = ((new_words - original_words) / original_words) * 100 if original_words > 0 else 0
                    
                    st.info(f"Original: ~{original_words} words | New: ~{new_words} words | Change: {word_diff:.1f}%")
                    
                    # Save to history
                    save_to_history(st.session_state, "Text Rewriter", 
                                   {"original_text": original_text[:100] + "..." if len(original_text) > 100 else original_text, 
                                    "reading_level": reading_level, 
                                    "style": style, "purpose": purpose}, 
                                   result)

# Tool 3: Academic Content Generator
def render_academic_content():
    """Render the Academic Content Generator tool."""
    st.markdown("<div class='sub-header'>📚 Academic Content Generator</div>", unsafe_allow_html=True)
    
    with st.form(key="academic_content_form"):
        topic = st.text_input("Topic", placeholder="e.g., Photosynthesis, Civil Rights Movement")
        
        col1, col2 = st.columns(2)
        
        with col1:
            content_type = st.selectbox("Content Type", 
                                      options=["Passage/Article", "Overview", "Definition", "Process Explanation", 
                                               "Timeline", "Comparison", "Analysis", "Problem-Solution"])
            grade_level = st.selectbox("Grade Level", 
                                     options=["Primary (1-3)", "Primary (4-6)", "Secondary (7-9)", "Secondary (10-12)", "College"])
        
        with col2:
            subject = st.selectbox("Subject", 
                                 options=["Science", "Mathematics", "History", "Geography", "Literature", "Arts", 
                                          "Social Studies", "Economics", "Technology", "Languages"])
            language = st.selectbox("Language", options=["English", "Bahasa Melayu"])
        
        key_concepts = st.text_area("Key Concepts to Include (comma-separated)", 
                                  placeholder="e.g., light energy, chloroplasts, glucose, oxygen")
        
        submit_button = st.form_submit_button(label="Generate Academic Content")
    
    if submit_button:
        if not topic:
            st.error("Please enter a topic.")
        else:
            with st.spinner("Generating academic content..."):
                # Format key concepts
                concept_list = [concept.strip() for concept in key_concepts.split(",")] if key_concepts else []
                
                prompt = f"""
                Create an educational {content_type} about "{topic}" for {grade_level} students in the subject of {subject} in {language}.
                
                {f"Include these key concepts: {', '.join(concept_list)}" if concept_list else ""}
                
                Guidelines:
                1. Ensure accuracy and educational value
                2. Use age-appropriate language for {grade_level} students
                3. Structure the content clearly with appropriate subheadings
                4. Include at least 3 key takeaways or main points
                5. If relevant, include real-world applications or examples
                6. Length should be appropriate for a classroom resource (300-500 words)
                
                Format your response with a clear title, introduction, body with appropriate sections, and conclusion.
                """
                
                result = call_gemini_api(prompt, st.session_state['api_key'])
                
                if result:
                    display_result("Generated Academic Content", result)
                    
                    # Save to history
                    save_to_history(st.session_state, "Academic Content", 
                                   {"topic": topic, "content_type": content_type, 
                                    "grade_level": grade_level, "subject": subject,
                                    "key_concepts": key_concepts}, 
                                   result)

# Tool 4: Lesson Plan Generator
def render_lesson_plan_generator():
    """Render the Lesson Plan Generator tool."""
    st.markdown("<div class='sub-header'>📚 Lesson Plan Generator</div>", unsafe_allow_html=True)
    
    # Load educational data
    strategies_df, _ = load_educational_data()
    
    with st.form(key="lesson_plan_form"):
        lesson_objective = st.text_input("Lesson Objective", 
                                       placeholder="e.g., Students will understand the water cycle")
        student_action = st.text_input("Student Action", 
                                     placeholder="e.g., create a diagram explaining each step of the water cycle")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            duration = st.number_input("Duration (minutes)", min_value=30, max_value=180, value=60, step=5)
            grade_level = st.selectbox("Grade Level", 
                                     options=["Primary 1-3", "Primary 4-6", "Secondary 1-3", "Secondary 4-5"])
        
        with col2:
            subject = st.selectbox("Subject Area", 
                                 options=["Mathematics", "Science", "English/Language", "Geography", "History", "Art", "Music", "Physical Education", "Other"])
            language = st.selectbox("Language", options=["English", "Bahasa Melayu"])
        
        with col3:
            resources = st.multiselect("Available Resources", 
                                     options=["Whiteboard", "Projector", "Computers", "Tablets", "Textbooks", "Worksheets", "Manipulatives", "Limited Resources"])
            activity_focus = st.multiselect("Activity Focus", 
                                          options=["Collaborative", "Individual", "Discussion", "Hands-on", "Digital", "Reading", "Writing"])
        
        # Include strategies for different parts of the lesson
        st.markdown("**Include specific strategies for:**")
        strategy_cols = st.columns(5)
        include_strategies = {}
        
        strategy_types = ["Starter", "Instruction", "Assessment", "Dialogic", "Consolidation"]
        for i, col in enumerate(strategy_cols):
            with col:
                strategy_type = strategy_types[i]
                include_strategies[strategy_type] = st.checkbox(strategy_type, value=True)
        
        submit_button = st.form_submit_button(label="Generate Lesson Plan")
    
    if submit_button:
        if not lesson_objective or not student_action:
            st.error("Please enter both the lesson objective and student action.")
        else:
            with st.spinner("Generating lesson plan..."):
                # Select strategies to include in the prompt
                strategy_prompts = []
                for strategy_type, include in include_strategies.items():
                    if include:
                        # Get a random strategy from that category
                        strategy = strategies_df[strategy_type].sample().iloc[0]
                        strategy_prompts.append(f"{strategy_type}: {strategy}")
                
                strategies_text = "\n".join(strategy_prompts)
                
                prompt = f"""
                You are an experienced {subject} teacher. Create a detailed {duration}-minute lesson plan for {grade_level} students with this objective:

                OBJECTIVE: {lesson_objective}
                STUDENT ACTION: {student_action}

                Resources available: {", ".join(resources)}
                Activity focus: {", ".join(activity_focus)}

                Please incorporate and adapt these teaching strategies into your plan:
                {strategies_text}

                Format your lesson plan with these clear sections:
                1. 📌 **Starter**: An engaging activity to begin the lesson (5-10 minutes)
                2. 🧠 **Instruction**: How you'll present the main content (15-20 minutes)
                3. 📝 **Assessment**: How you'll check understanding during the lesson
                4. 🗣️ **Dialogic**: How students will discuss and engage with the content
                5. ✅ **Consolidation**: How you'll summarize and conclude the lesson
                6. 🚀 **S2S**: Suggestions for supporting struggling students and extending learning for advanced students

                For each section, provide specific timings, detailed instructions, and necessary resources. The plan should be practical, easy to follow, and written in {language}.
                """
                
                result = call_gemini_api(prompt, st.session_state['api_key'])
                
                if result:
                    display_result("Generated Lesson Plan", result)
                    
                    # Save to history
                    save_to_history(st.session_state, "Lesson Plan Generator", 
                                   {"lesson_objective": lesson_objective, "student_action": student_action, 
                                    "duration": duration, "grade_level": grade_level, "subject": subject}, 
                                   result)

# Tool 5: Unit Plan Generator
def render_unit_plan_generator():
    """Render the Unit Plan Generator tool."""
    st.markdown("<div class='sub-header'>📘 Unit Plan Generator</div>", unsafe_allow_html=True)
    
    with st.form(key="unit_plan_form"):
        unit_title = st.text_input("Unit Title", placeholder="e.g., Understanding Ecosystems")
        
        col1, col2 = st.columns(2)
        
        with col1:
            subject = st.selectbox("Subject", 
                                 options=["Science", "Mathematics", "English/Language Arts", "Social Studies", 
                                          "History", "Geography", "Art", "Music", "Physical Education", "Other"])
            grade_level = st.selectbox("Grade Level", 
                                     options=["Primary (1-3)", "Primary (4-6)", "Secondary (7-9)", "Secondary (10-12)"])
        
        with col2:
            duration = st.selectbox("Unit Duration", 
                                  options=["1 week", "2 weeks", "3 weeks", "4 weeks", "6 weeks"])
            language = st.selectbox("Language", options=["English", "Bahasa Melayu"])
        
        learning_objectives = st.text_area("Learning Objectives/Standards", 
                                        placeholder="List 3-5 key learning objectives or standards for this unit")
        
        key_resources = st.text_input("Key Resources Available", 
                                    placeholder="e.g., textbooks, lab equipment, computers, field trip opportunities")
        
        submit_button = st.form_submit_button(label="Generate Unit Plan")
    
    if submit_button:
        if not unit_title or not learning_objectives:
            st.error("Please enter a unit title and learning objectives.")
        else:
            with st.spinner("Generating unit plan..."):
                prompt = f"""
                Create a comprehensive unit plan for "{unit_title}" in {subject} for {grade_level} students that spans {duration}. The unit plan should be in {language}.
                
                Learning Objectives:
                {learning_objectives}
                
                Resources Available:
                {key_resources if key_resources else "Standard classroom resources"}
                
                Include in the unit plan:
                
                1. Unit Overview (big ideas and essential questions)
                2. Sequence of 4-8 lesson topics with brief descriptions
                3. Assessment Plan (formative and summative assessments)
                4. Differentiation Strategies for diverse learners
                5. Key vocabulary
                6. Cross-curricular connections
                7. Materials and resources needed
                
                Format the unit plan clearly with headings and bullet points for easy reference.
                """
                
                result = call_gemini_api(prompt, st.session_state['api_key'])
                
                if result:
                    display_result("Generated Unit Plan", result)
                    
                    # Save to history
                    save_to_history(st.session_state, "Unit Plan Generator", 
                                   {"unit_title": unit_title, "subject": subject, 
                                    "grade_level": grade_level, "duration": duration,
                                    "learning_objectives": learning_objectives}, 
                                   result)

# tools/assessment_tools.py
import streamlit as st
import re
from utils.api import call_gemini_api
from utils.data import load_educational_data, save_to_history
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

def display_result(title, content):
    """Display the result in a formatted area."""
    st.markdown(f"### {title}")
    st.markdown(f"<div class='result-area'>{content}</div>", unsafe_allow_html=True)

# Tool 1: MCQ Generator
def render_mcq_generator():
    """Render the MCQ Generator tool."""
    st.markdown("<div class='sub-header'>📝 Multiple Choice Question Generator</div>", unsafe_allow_html=True)
    
    with st.form(key="mcq_generator_form"):
        topic = st.text_input("Main Topic", placeholder="e.g., Photosynthesis, World War II")
        keywords = st.text_input("Key Words (comma-separated)", 
                               placeholder="e.g., chlorophyll, sunlight, glucose")
        
        num_questions = st.slider("Number of Questions", min_value=3, max_value=10, value=5)
        reading_age = st.slider("Reading Age", min_value=6, max_value=18, value=10)
        
        submit_button = st.form_submit_button(label="Generate MCQs")
    
    if submit_button:
        if not topic:
            st.error("Please enter a topic.")
        else:
            with st.spinner("Generating questions..."):
                prompt = f"""
                You are an MCQ generator. Create {num_questions} multiple-choice questions (MCQs) about "{topic}" for children with a reading age of {reading_age}. 
                {f"Use these keywords: {keywords}." if keywords else ""}
                Keep language simple and easy to understand, but still address the key concepts.

                For each question, produce exactly the following lines:
                Q: [Write a clear, simple question]
                A: [Option A] | [Option B] | [Option C] | [Option D]
                Correct: [One letter: A, B, C, or D]
                Explanation: [Brief reason why the correct answer is correct]
                Concepts: [Comma-separated main ideas or key words]

                Important:
                - Do NOT label your options inside the 'A:' line with A:, B:, C:, D:. Just separate them with " | ".
                - Make sure every question has exactly 4 options.
                - Ensure questions test understanding, not just recall.
                - Use age-appropriate language for reading age {reading_age}.
                """
                
                result = call_gemini_api(prompt, st.session_state['api_key'])
                
                if result:
                    display_result("Generated Questions", result)
                    
                    # Save to history
                    save_to_history(st.session_state, "MCQ Generator", 
                                   {"topic": topic, "keywords": keywords, 
                                    "num_questions": num_questions, "reading_age": reading_age}, 
                                   result)

# Tool 2: HOT Questions
def render_hot_questions():
    """Render the Higher-Order Thinking Questions tool."""
    st.markdown("<div class='sub-header'>🧠 Higher-Order Thinking Questions</div>", unsafe_allow_html=True)
    
    # Load Bloom's taxonomy data
    _, blooms_df = load_educational_data()
    
    with st.form(key="hot_questions_form"):
        lesson_objective = st.text_input("Lesson Objective", 
                                       placeholder="e.g., Understand the causes of climate change")
        
        col1, col2 = st.columns(2)
        
        with col1:
            bloom_level = st.selectbox("Bloom's Taxonomy Level", 
                                     options=blooms_df['Level'].tolist())
            subject = st.selectbox("Subject", 
                                 options=["english", "math", "science", "other"])
        
        with col2:
            complexity = st.selectbox("Complexity Level", 
                                    options=["primary", "lower_secondary", "upper_secondary", "igcse"])
            language = st.selectbox("Language", options=["English", "Bahasa Melayu"])
        
        # Display corresponding question stems and response frames
        bloom_data = blooms_df[blooms_df['Level'] == bloom_level].iloc[0]
        st.markdown(f"**Question Stems**: {bloom_data['Question_Stems']}")
        st.markdown(f"**Response Frames**: {bloom_data['Response_Frames']}")
        
        submit_button = st.form_submit_button(label="Generate HOT Questions")
    
    if submit_button:
        if not lesson_objective:
            st.error("Please enter a lesson objective.")
        else:
            with st.spinner("Generating HOT questions..."):
                # Get question stems and response frames
                bloom_info = blooms_df[blooms_df['Level'] == bloom_level].iloc[0]
                question_stems = bloom_info['Question_Stems']
                response_frames = bloom_info['Response_Frames']
                
                # Build the prompt with guidance for answering HOT questions
                prompt = f"""
                You are an AI assistant helping teachers create HOT questions. 
                Generate a **higher-order thinking (HOT) question** based on the following details:
                
                - **Language**: {language}
                - **Lesson Objective**: {lesson_objective}
                - **Bloom's Taxonomy Level**: {bloom_level}
                - **Complexity Level**: {complexity}
                
                Use these question stems:
                **{question_stems}**

                Use these sentence frames:
                **{response_frames}**

                Include guidance for students using these strategies:
                - Understand the question: Identify what the question is asking them to do (analyze, evaluate, compare, etc.)
                - Break down the question: Separate complex questions into smaller parts
                - Think critically: Analyze information closely and evaluate different perspectives
                - Provide evidence: Support answers with specific examples or logical arguments
                - Consider counterarguments: Acknowledge opposing viewpoints

                ### Generate the final HOT Question and at least **3 sentence stems** that would help students structure their answers. The question should match the complexity level.
                **Respond in {language} only.**

                Format your response as:
                Q: <Your HOT Question>
                Stems:
                1) <Sentence Stem 1>
                2) <Sentence Stem 2>
                3) <Sentence Stem 3>
                """
                
                result = call_gemini_api(prompt, st.session_state['api_key'])
                
                if result:
                    display_result("Generated HOT Question", result)
                    
                    # Save to history
                    save_to_history(st.session_state, "HOT Questions", 
                                   {"lesson_objective": lesson_objective, "bloom_level": bloom_level, 
                                    "subject": subject, "complexity": complexity, "language": language}, 
                                   result)

# Tool 3: Text Dependent Questions
def render_text_dependent_questions():
    """Render the Text Dependent Questions tool."""
    st.markdown("<div class='sub-header'>📖 Text Dependent Questions</div>", unsafe_allow_html=True)
    
    with st.form(key="text_dependent_questions_form"):
        passage = st.text_area("Passage/Text", 
                            placeholder="Paste the reading passage or text here...",
                            height=200)
        
        col1, col2 = st.columns(2)
        
        with col1:
            grade_level = st.selectbox("Grade Level", 
                                     options=["Primary (1-3)", "Primary (4-6)", "Secondary (7-9)", "Secondary (10-12)"])
            num_questions = st.slider("Number of Questions", min_value=3, max_value=10, value=5)
        
        with col2:
            question_types = st.multiselect("Question Types", 
                                          options=["Key Details", "Vocabulary in Context", "Text Structure", 
                                                  "Author's Purpose", "Inference", "Main Idea", "Evidence-Based"],
                                          default=["Key Details", "Vocabulary in Context", "Inference"])
            language = st.selectbox("Language", options=["English", "Bahasa Melayu"])
        
        submit_button = st.form_submit_button(label="Generate Text-Dependent Questions")
    
    if submit_button:
        if not passage:
            st.error("Please enter a passage/text.")
        else:
            with st.spinner("Generating text-dependent questions..."):
                # Join question types with commas
                question_types_str = ", ".join(question_types)
                
                prompt = f"""
                Create {num_questions} text-dependent questions in {language} for the following passage, appropriate for {grade_level} students. 
                Focus on these question types: {question_types_str}.
                
                Passage:
                ---
                {passage}
                ---
                
                For each question:
                1. Clearly indicate the question type (e.g., Key Details, Inference, etc.)
                2. Write a clear, focused question that requires students to refer back to the text
                3. Provide the correct answer and cite specific text evidence that supports it
                4. Include a brief explanation of why this is the correct answer
                
                Format each question as follows:
                [Question Type] Question: [The question]
                Answer: [Correct answer]
                Text Evidence: [Relevant quote or reference from the text]
                Explanation: [Brief explanation]
                """
                
                result = call_gemini_api(prompt, st.session_state['api_key'])
                
                if result:
                    display_result("Generated Text-Dependent Questions", result)
                    
                    # Save to history
                    save_to_history(st.session_state, "Text Dependent Questions", 
                                   {"passage": passage[:100] + "..." if len(passage) > 100 else passage, 
                                    "grade_level": grade_level, "question_types": question_types_str,
                                    "num_questions": num_questions}, 
                                   result)

# Tool 4: DOK Questions
def render_dok_questions():
    """Render the Depth of Knowledge Questions tool."""
    st.markdown("<div class='sub-header'>🔍 Depth of Knowledge (DOK) Questions</div>", unsafe_allow_html=True)
    
    with st.form(key="dok_questions_form"):
        topic = st.text_input("Topic/Content", placeholder="e.g., Fractions, Romeo and Juliet, Ecosystems")
        
        col1, col2 = st.columns(2)
        
        with col1:
            subject = st.selectbox("Subject", 
                                 options=["Mathematics", "English Language Arts", "Science", "Social Studies", 
                                          "History", "Other"])
            grade_level = st.selectbox("Grade Level", 
                                     options=["Primary (1-3)", "Primary (4-6)", "Secondary (7-9)", "Secondary (10-12)"])
        
        with col2:
            dok_levels = st.multiselect("DOK Levels", 
                                      options=["Level 1: Recall", "Level 2: Skills/Concepts", 
                                               "Level 3: Strategic Thinking", "Level 4: Extended Thinking"],
                                      default=["Level 1: Recall", "Level 2: Skills/Concepts", "Level 3: Strategic Thinking"])
            language = st.selectbox("Language", options=["English", "Bahasa Melayu"])
        
        standards = st.text_area("Standards/Learning Objectives (Optional)", 
                              placeholder="List any specific standards or learning objectives to target")
        
        submit_button = st.form_submit_button(label="Generate DOK Questions")
    
    if submit_button:
        if not topic:
            st.error("Please enter a topic/content.")
        else:
            with st.spinner("Generating DOK questions..."):
                # Join DOK levels with commas
                dok_levels_str = ", ".join(dok_levels)
                
                prompt = f"""
                Create Depth of Knowledge (DOK) questions in {language} about {topic} for {grade_level} students in {subject}.
                
                {f"Target these standards/objectives: {standards}" if standards else ""}
                
                Generate 2 questions for each of these DOK levels: {dok_levels_str}
                
                For each question:
                1. Clearly indicate the DOK level
                2. Write a clear, focused question appropriate for that DOK level
                3. Provide sample answer(s) or success criteria
                4. Include a brief explanation of why this question reflects its DOK level
                
                DOK Level Descriptions:
                - Level 1 (Recall): Recall of information, basic facts, definitions, simple procedures
                - Level 2 (Skills/Concepts): Use information, conceptual knowledge, follow procedures, two or more steps
                - Level 3 (Strategic Thinking): Reasoning, planning, using evidence, complex thinking, justification
                - Level 4 (Extended Thinking): Complex reasoning, planning, developing, thinking, connecting ideas across content
                
                Format each question clearly with headings for the DOK level, question, sample answer, and explanation.
                """
                
                result = call_gemini_api(prompt, st.session_state['api_key'])
                
                if result:
                    display_result("Generated DOK Questions", result)
                    
                    # Save to history
                    save_to_history(st.session_state, "DOK Questions", 
                                   {"topic": topic, "subject": subject, 
                                    "grade_level": grade_level, "dok_levels": dok_levels_str}, 
                                   result)

# Helper function to get video ID from URL
def get_video_id(url):
    """Extracts YouTube video ID from various URL formats."""
    if not url:
        return None
    # Regex patterns to cover standard, short, and embed URLs
    patterns = [
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([a-zA-Z0-9_-]{11})',  # Standard URL
        r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/([a-zA-Z0-9_-]{11})',           # Short URL
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([a-zA-Z0-9_-]{11})',   # Embed URL
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/v\/([a-zA-Z0-9_-]{11})',       # v/ URL
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/shorts\/([a-zA-Z0-9_-]{11})'  # Shorts URL
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None # Return None if no valid ID found

# Helper function to get transcript
def get_transcript(video_id, desired_language_code='en'):
    """Fetches YouTube transcript for a given video ID."""
    if not video_id:
        return None, "Invalid video URL provided."
    try:
        # Get available transcripts
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Try to find the desired language, fallback to generated, then any available
        try:
            transcript = transcript_list.find_manually_created_transcript([desired_language_code])
        except NoTranscriptFound:
            try:
                transcript = transcript_list.find_generated_transcript([desired_language_code])
            except NoTranscriptFound:
                # Fallback: Get the first available transcript regardless of language
                transcript = transcript_list.find_generated_transcript(transcript_list.available_languages)


        transcript_text = " ".join([entry['text'] for entry in transcript.fetch()])
        return transcript_text, None # Return transcript and no error
        
    except TranscriptsDisabled:
        return None, "Transcripts are disabled for this video."
    except NoTranscriptFound:
         return None, f"No transcript found for this video in any language or for code '{desired_language_code}'. Transcripts might not be available."
    except Exception as e:
        # Catch other potential errors (network issues, etc.)
        return None, f"An error occurred while fetching the transcript: {e}"


# Tool 5: YouTube Video Questions
def render_youtube_video_questions():
    """Render the YouTube Video Questions tool."""
    st.markdown("<div class='sub-header'>🎥 YouTube Video Questions</div>", unsafe_allow_html=True)
    st.markdown("Generates questions **based on the actual transcript** of a YouTube video.")

    with st.form(key="youtube_questions_form"):
        video_url = st.text_input("YouTube Video URL", placeholder="e.g., https://www.youtube.com/watch?v=...")
        # Video topic is less critical now, but can provide context if transcript fails
        # video_topic = st.text_input("Video Topic/Title (Optional Fallback)", placeholder="e.g., Photosynthesis Explained")

        col1, col2 = st.columns(2)

        with col1:
            grade_level = st.selectbox("Grade Level",
                                     options=["Primary (1-3)", "Primary (4-6)", "Secondary (7-9)", "Secondary (10-12)"])
            question_focus = st.multiselect("Question Focus",
                                          options=["Comprehension", "Analysis", "Application", "Prediction",
                                                  "Evaluation", "Connection to Curriculum", "Summarization", "Fact-Checking"],
                                          default=["Comprehension", "Analysis", "Summarization"])

        with col2:
            num_questions = st.slider("Number of Questions", min_value=3, max_value=15, value=5) # Increased max slightly
            language = st.selectbox("Language of Questions", options=["English", "Bahasa Melayu"])
            transcript_lang_code = 'en' if language == "English" else 'ms' # Map UI language to transcript code

        learning_objectives = st.text_area("Learning Objectives (Optional)",
                                        placeholder="What should students learn from this video?")

        submit_button = st.form_submit_button(label="Generate Video Questions from Transcript")

    if submit_button:
        if not video_url:
            st.error("Please enter a YouTube Video URL.")
            return # Stop processing

        video_id = get_video_id(video_url)
        if not video_id:
            st.error("Could not extract a valid Video ID from the URL. Please check the link.")
            return # Stop processing

        with st.spinner(f"Fetching transcript for video ID: {video_id}..."):
            transcript_text, error_msg = get_transcript(video_id, transcript_lang_code)

        if error_msg:
            st.error(f"Failed to get transcript: {error_msg}")
            st.warning("Cannot generate questions based on video content without a transcript.")
            # Optionally, you could fall back to the old topic-based generation here,
            # but it's better to be clear that it failed.
            return # Stop processing

        if not transcript_text:
             st.error("Fetched transcript appears to be empty.")
             return # Stop processing

        # --- Transcript Fetched Successfully ---
        with st.spinner("Transcript found! Generating questions based on video content..."):
            focus_str = ", ".join(question_focus)

            # Limit transcript length to avoid exceeding API context limits (adjust as needed)
            # A simple truncation strategy. More complex chunking/summarization might be needed for very long videos.
            MAX_TRANSCRIPT_CHARS = 15000 # Example limit, adjust based on your model's context window
            if len(transcript_text) > MAX_TRANSCRIPT_CHARS:
                st.warning(f"Transcript is very long ({len(transcript_text)} chars). Truncating to {MAX_TRANSCRIPT_CHARS} characters for analysis.")
                transcript_text = transcript_text[:MAX_TRANSCRIPT_CHARS]

            prompt = f"""
            You are an expert educational content creator. Based **strictly** on the following YouTube video transcript, create {num_questions} questions in **{language}** suitable for **{grade_level}** students.

            **Video Transcript:**
            ```
            {transcript_text}
            ```

            **Instructions:**
            1.  Focus on these question types: **{focus_str}**. Ensure a mix if multiple types are selected.
            2.  Generate questions **directly related to the content, examples, and information presented in the transcript**. Do NOT use external knowledge.
            3.  {f"Align questions with these Learning Objectives if provided: {learning_objectives}" if learning_objectives else "Focus on understanding the key points of the transcript."}
            4.  For each question:
                *   Clearly indicate the intended **Question Type** (e.g., Comprehension, Analysis).
                *   Write a clear, concise question in **{language}**.
                *   Provide a **Sample Answer** or **Key Points** expected in a good response, based *only* on the transcript.
            5.  Consider including a mix of questions suitable for different points (e.g., recalling facts, analyzing arguments, summarizing sections). Suggest if a question is best for 'During Viewing' or 'After Viewing' based on its nature.

            **Output Format:**
            Present each question clearly numbered, with its type, the question itself, and the sample answer/key points.
            Example:
            1.  **Type:** Comprehension (After Viewing)
                **Question:** According to the video transcript, what are the three main stages discussed?
                **Answer Key Points:** The transcript mentions Stage A, Stage B, and Stage C as the main stages.
            """

            # Ensure you have the call_gemini_api function available
            # Make sure it handles potential API errors
            try:
                 result = call_gemini_api(prompt, st.session_state.get('api_key')) # Use .get for safety

                 if result:
                     display_result("Generated Video Questions (from Transcript)", result) # Assuming display_result exists

                     # Save to history (include info that transcript was used)
                     save_to_history(st.session_state, "YouTube Video Questions",
                                    {"video_url": video_url,
                                     "grade_level": grade_level, "question_focus": focus_str,
                                     "num_questions": num_questions, "transcript_used": True,
                                     "transcript_length": len(transcript_text)},
                                    result) # Assuming save_to_history exists
                 else:
                      st.error("The AI model did not return a result.")

            except Exception as e:
                 st.error(f"An error occurred while calling the AI model: {e}")
                 # Log the error for debugging if needed

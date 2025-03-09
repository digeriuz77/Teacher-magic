import streamlit as st
import google.generativeai as genai
import pandas as pd
import json
import os
import math
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI Teaching Assistant by Gary Stanyard",
    page_icon="🧑‍🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #4b2e83;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #4b2e83;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .tool-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .api-section {
        background-color: #f9f9f9;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
    }
    .result-area {
        background-color: #f0f4f8;
        border-radius: 10px;
        padding: 15px;
        border-left: 5px solid #4b2e83;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'api_key' not in st.session_state:
    st.session_state['api_key'] = ""
if 'api_key_saved' not in st.session_state:
    st.session_state['api_key_saved'] = False
if 'history' not in st.session_state:
    st.session_state['history'] = []

# Sidebar with API Key entry
with st.sidebar:
    st.markdown("### Setup")
    st.markdown("#### API Key")
    
    api_key_input = st.text_input(
        "Enter your Gemini API Key:",
        type="password",
        value=st.session_state['api_key'],
        help="Get a free API key from Google AI Studio: https://aistudio.google.com//"
    )
    
    if st.button("Save API Key"):
        st.session_state['api_key'] = api_key_input
        st.session_state['api_key_saved'] = True
        st.success("API Key saved for this session!")
    
    if st.session_state['api_key_saved']:
        st.success("API Key is configured!")
    
    st.markdown("---")
    st.markdown("### Tool Navigation")
    tool_options = [
        "Prompt Builder",
        "MCQ Generator",
        "HOT Questions",
        "Lesson Plan Generator",
        "Vocabulary Focus",
        "Text Generator"
    ]
    selected_tool = st.radio("Select Tool:", tool_options)

# Load educational data
@st.cache_data
def load_educational_data():
    # Strategies from paste.txt
    strategies_df = pd.DataFrame({
        'Starter': [
            "Show an image related to the topic and ask students to describe what they see.",
            "Use a mnemonic to help students remember key vocabulary words.",
            "Have students act out a key concept using gestures (Total Physical Response).",
            "Use real objects or pictures to introduce the vocabulary in context.",
            "Ask a thought-provoking question to activate prior knowledge."
        ],
        'Instruction': [
            "Use word mapping: Define, give examples, and create connections.",
            "Use sentence frames: Students complete structured sentences using new words.",
            "Create a comic strip incorporating key vocabulary in context.",
            "Collaborative storytelling: Each student adds a sentence using a target word.",
            "Read a short, engaging passage and ask students to identify key vocabulary words."
        ],
        'Assessment': [
            "Quickfire Q&A: Students explain a word in pairs in 30 seconds.",
            "Exit Ticket: Students write a sentence using a key word.",
            "Create a mind map linking words to related concepts.",
            "Match words with definitions in a timed challenge.",
            "Fill-in-the-blank using words from the lesson."
        ],
        'Dialogic': [
            "Turn & Talk: In pairs, students explain a word in their own words.",
            "Think-Pair-Share: Discuss how they'd use the word in real life.",
            "Role-play: Students use key words in a real-world scenario.",
            "Socratic questioning and Socratic circles: Encourage discussion and critical thinking.",
            "Pose-pause-bounce-pounce: Build on peer ideas collaboratively."
        ],
        'Consolidation': [
            "Summarize the lesson in three key words and explain why.",
            "Draw a picture representing the meaning of a key word.",
            "Word Ladder: Change one letter at a time to form new words.",
            "Vocabulary Bingo: Call definitions, students mark words.",
            "Create a KWL Chart (What I Know, What I Want to Know, What I Learned)."
        ]
    })
    
    # Bloom's Taxonomy from paste-2.txt
    blooms_df = pd.DataFrame({
        'Level': ['REMEMBER', 'UNDERSTAND', 'APPLY', 'ANALYZE', 'CREATE', 'EVALUATE'],
        'Description': [
            'Recall facts and basic concepts',
            'Explain ideas or concepts',
            'Use information in new situations',
            'Draw connections among ideas',
            'Produce new or original work',
            'Justify a stand or decision'
        ],
        'Question_Stems': [
            'What is...? Where is...? When did...? What would you find...?',
            'How would you explain...? What does this mean...? Can you give an example of...?',
            'How would you use...? How would you solve...? What would happen if...?',
            'Why did this happen...? What evidence shows...? How are these different...?',
            'How could you make...? What would you design...? How could you adapt...?',
            'Do you think this is good...? What would you choose...? Why is this method best...?'
        ],
        'Response_Frames': [
            'It is... You would find this in/at...',
            'I can explain this by... This means that...',
            'I would use this by... To solve this I would...',
            'This happened because... The evidence is... ___ is different from ___ because...',
            'I could make this by... I would design ___ with...',
            'I think this is good/bad because... I would choose ___ because...'
        ]
    })
    
    return strategies_df, blooms_df

strategies_df, blooms_df = load_educational_data()

# Configure Gemini API
def configure_genai():
    if st.session_state['api_key']:
        genai.configure(api_key=st.session_state['api_key'])
        return True
    return False

# Function to call Gemini API
def call_gemini_api(prompt):
    if not configure_genai():
        st.error("Please save your API key first!")
        return None
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error calling Gemini API: {e}")
        return None

# Save history
def save_to_history(tool_name, inputs, result):
    history_item = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tool": tool_name,
        "inputs": inputs,
        "result": result
    }
    st.session_state['history'].insert(0, history_item)  # Add to the beginning

# Download history as JSON
def get_history_json():
    return json.dumps(st.session_state['history'], indent=2)

# Main title
st.markdown("<div class='main-header'>🧑‍🏫 AI Teaching Assistant</div>", unsafe_allow_html=True)

# Add history and export function at the bottom
with st.expander("📜 History & Export", expanded=False):
    if len(st.session_state['history']) > 0:
        st.download_button(
            label="Download History (JSON)",
            data=get_history_json(),
            file_name=f"ai_teaching_assistant_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
        
        # Display recent history
        st.markdown("### Recent Activity")
        for i, item in enumerate(st.session_state['history'][:5]):  # Show last 5 items
            st.markdown(f"**{item['timestamp']} - {item['tool']}**")
            with st.expander(f"View Details"):
                st.write("Inputs:", item['inputs'])
                st.markdown("Result:")
                st.markdown(item['result'])
        
        if len(st.session_state['history']) > 5:
            st.markdown(f"*...and {len(st.session_state['history']) - 5} more items*")
    else:
        st.info("No history yet. Use the tools above to generate content!")

# Tool: Prompt Builder
if selected_tool == "Prompt Builder":
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
            
            st.markdown("### Your AI Prompt:")
            st.markdown(f"<div class='result-area'>{final_prompt}</div>", unsafe_allow_html=True)
            
            # Add copy button
            st.text("")
            if st.button("Copy to Clipboard"):
                st.code(final_prompt)
                st.success("Prompt copied to clipboard! (Use Ctrl+C)")
            
            # Save to history
            save_to_history("Prompt Builder", 
                           {"role": role, "outcome": outcome, "audience": audience, 
                            "avoid": avoid, "example": example}, 
                           final_prompt)

# Tool: MCQ Generator
elif selected_tool == "MCQ Generator":
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
                
                result = call_gemini_api(prompt)
                
                if result:
                    st.markdown("### Generated Questions:")
                    st.markdown(f"<div class='result-area'>{result}</div>", unsafe_allow_html=True)
                    
                    # Format for printing/export
                    formatted_result = result.replace("Q:", "**Q:**").replace("A:", "**A:**").replace("Correct:", "**Correct:**").replace("Explanation:", "**Explanation:**").replace("Concepts:", "**Concepts:**")
                    
                    # Save to history
                    save_to_history("MCQ Generator", 
                                   {"topic": topic, "keywords": keywords, 
                                    "num_questions": num_questions, "reading_age": reading_age}, 
                                   result)

# Tool: HOT Questions
elif selected_tool == "HOT Questions":
    st.markdown("<div class='sub-header'>🧠 Higher-Order Thinking Questions</div>", unsafe_allow_html=True)
    
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
                
                result = call_gemini_api(prompt)
                
                if result:
                    st.markdown("### Generated HOT Question:")
                    st.markdown(f"<div class='result-area'>{result}</div>", unsafe_allow_html=True)
                    
                    # Save to history
                    save_to_history("HOT Questions", 
                                   {"lesson_objective": lesson_objective, "bloom_level": bloom_level, 
                                    "subject": subject, "complexity": complexity, "language": language}, 
                                   result)

# Tool: Lesson Plan Generator
elif selected_tool == "Lesson Plan Generator":
    st.markdown("<div class='sub-header'>📚 Lesson Plan Generator</div>", unsafe_allow_html=True)
    
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
                
                result = call_gemini_api(prompt)
                
                if result:
                    st.markdown("### Generated Lesson Plan:")
                    st.markdown(f"<div class='result-area'>{result}</div>", unsafe_allow_html=True)
                    
                    # Save to history
                    save_to_history("Lesson Plan Generator", 
                                   {"lesson_objective": lesson_objective, "student_action": student_action, 
                                    "duration": duration, "grade_level": grade_level, "subject": subject}, 
                                   result)

# Tool: Vocabulary Focus
elif selected_tool == "Vocabulary Focus":
    st.markdown("<div class='sub-header'>📖 Vocabulary Focus</div>", unsafe_allow_html=True)
    
    with st.form(key="vocab_focus_form"):
        vocabulary = st.text_area("Enter vocabulary words (comma-separated)", 
                                placeholder="e.g., photosynthesis, ecosystem, habitat, predator")
        
        col1, col2 = st.columns(2)
        
        with col1:
            grade_level = st.selectbox("Grade Level", 
                                     options=["Primary 1-3", "Primary 4-6", "Secondary 1-3", "Secondary 4-5"])
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
                
                result = call_gemini_api(prompt)
                
                if result:
                    st.markdown(f"### Generated {output_type}:")
                    st.markdown(f"<div class='result-area'>{result}</div>", unsafe_allow_html=True)
                    
                    # Save to history
                    save_to_history("Vocabulary Focus", 
                                   {"vocabulary": vocabulary, "grade_level": grade_level, 
                                    "output_type": output_type, "language": language}, 
                                   result)

# Tool: Text Generator
elif selected_tool == "Text Generator":
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
                
                result = call_gemini_api(prompt)
                
                if result:
                    st.markdown("### Generated Text:")
                    st.markdown(f"<div class='result-area'>{result}</div>", unsafe_allow_html=True)
                    
                    # Calculate approximate word count
                    word_count = len(result.split())
                    st.info(f"Approximate word count: {word_count}")
                    
                    # Save to history
                    save_to_history("Text Generator", 
                                   {"lexile_score": lexile_score, "topic": topic, 
                                    "subject": subject, "text_type": text_type, "vocabulary": vocabulary}, 
                                   result)

# Tool: Text Rewriter
elif selected_tool == "Text Rewriter":
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
                
                result = call_gemini_api(prompt)
                
                if result:
                    st.markdown("### Rewritten Text:")
                    st.markdown(f"<div class='result-area'>{result}</div>", unsafe_allow_html=True)
                    
                    # Calculate change in complexity
                    original_words = len(original_text.split())
                    new_words = len(result.split())
                    word_diff = ((new_words - original_words) / original_words) * 100 if original_words > 0 else 0
                    
                    st.info(f"Original: ~{original_words} words | New: ~{new_words} words | Change: {word_diff:.1f}%")
                    
                    # Save to history
                    save_to_history("Text Rewriter", 
                                   {"original_text": original_text[:100] + "..." if len(original_text) > 100 else original_text, 
                                    "reading_level": reading_level, 
                                    "style": style, "purpose": purpose}, 
                                   result)

# Tool: Academic Content
elif selected_tool == "Academic Content":
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
                
                result = call_gemini_api(prompt)
                
                if result:
                    st.markdown("### Generated Academic Content:")
                    st.markdown(f"<div class='result-area'>{result}</div>", unsafe_allow_html=True)
                    
                    # Save to history
                    save_to_history("Academic Content", 
                                   {"topic": topic, "content_type": content_type, 
                                    "grade_level": grade_level, "subject": subject,
                                    "key_concepts": key_concepts}, 
                                   result)

# Tool: Unit Plan Generator
elif selected_tool == "Unit Plan Generator":
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
                
                result = call_gemini_api(prompt)
                
                if result:
                    st.markdown("### Generated Unit Plan:")
                    st.markdown(f"<div class='result-area'>{result}</div>", unsafe_allow_html=True)
                    
                    # Save to history
                    save_to_history("Unit Plan Generator", 
                                   {"unit_title": unit_title, "subject": subject, 
                                    "grade_level": grade_level, "duration": duration,
                                    "learning_objectives": learning_objectives}, 
                                   result)

# Tool: Image Generator
elif selected_tool == "Image Generator":
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
                
                result = call_gemini_api(prompt)
                
                if result:
                    st.markdown("### Image Generation Prompt:")
                    st.markdown(f"<div class='result-area'>{result}</div>", unsafe_allow_html=True)
                    
                    # Save to history
                    save_to_history("Image Generator", 
                                   {"subject": subject, "image_type": image_type, 
                                    "style": style, "audience": audience, "purpose": purpose}, 
                                   result)

# Tool: Text Dependent Questions
elif selected_tool == "Text Dependent Questions":
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
                
                result = call_gemini_api(prompt)
                
                if result:
                    st.markdown("### Generated Text-Dependent Questions:")
                    st.markdown(f"<div class='result-area'>{result}</div>", unsafe_allow_html=True)
                    
                    # Save to history
                    save_to_history("Text Dependent Questions", 
                                   {"passage": passage[:100] + "..." if len(passage) > 100 else passage, 
                                    "grade_level": grade_level, "question_types": question_types_str,
                                    "num_questions": num_questions}, 
                                   result)

# Tool: DOK Questions
elif selected_tool == "DOK Questions":
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
                
                result = call_gemini_api(prompt)
                
                if result:
                    st.markdown("### Generated DOK Questions:")
                    st.markdown(f"<div class='result-area'>{result}</div>", unsafe_allow_html=True)
                    
                    # Save to history
                    save_to_history("DOK Questions", 
                                   {"topic": topic, "subject": subject, 
                                    "grade_level": grade_level, "dok_levels": dok_levels_str}, 
                                   result)

# Tool: YouTube Video Questions
elif selected_tool == "YouTube Video Questions":
    st.markdown("<div class='sub-header'>🎥 YouTube Video Questions</div>", unsafe_allow_html=True)
    
    with st.form(key="youtube_questions_form"):
        video_url = st.text_input("YouTube Video URL", placeholder="e.g., https://www.youtube.com/watch?v=...")
        video_topic = st.text_input("Video Topic/Title", placeholder="e.g., Photosynthesis Explained")
        
        col1, col2 = st.columns(2)
        
        with col1:
            grade_level = st.selectbox("Grade Level", 
                                     options=["Primary (1-3)", "Primary (4-6)", "Secondary (7-9)", "Secondary (10-12)"])
            question_focus = st.multiselect("Question Focus", 
                                          options=["Comprehension", "Analysis", "Application", "Prediction", 
                                                  "Evaluation", "Connection to Curriculum"],
                                          default=["Comprehension", "Analysis"])
        
        with col2:
            num_questions = st.slider("Number of Questions", min_value=3, max_value=10, value=5)
            language = st.selectbox("Language", options=["English", "Bahasa Melayu"])
        
        learning_objectives = st.text_area("Learning Objectives (Optional)", 
                                        placeholder="What should students learn from this video?")
        
        submit_button = st.form_submit_button(label="Generate Video Questions")
    
    if submit_button:
        if not video_topic:
            st.error("Please enter a video topic/title.")
        else:
            with st.spinner("Generating video questions..."):
                # Join question focus areas with commas
                focus_str = ", ".join(question_focus)
                
                # Video URL note
                video_note = f"based on the YouTube video at {video_url}" if video_url else f"about {video_topic}"
                
                prompt = f"""
                Create {num_questions} questions in {language} {video_note} suitable for {grade_level} students.
                
                {f"Learning Objectives: {learning_objectives}" if learning_objectives else ""}
                
                Focus on these question types: {focus_str}
                
                For each question:
                1. Clearly indicate the question type (e.g., Comprehension, Analysis, etc.)
                2. Write a clear, focused question that encourages students to engage with the video content
                3. Provide sample answer(s) or criteria for successful responses
                
                Include a mix of:
                - Before viewing questions (to activate prior knowledge)
                - During viewing questions (to maintain engagement)
                - After viewing questions (to assess understanding and extend thinking)
                
                Format each question with a clear indication of when it should be asked (before/during/after) and the question type.
                """
                
                result = call_gemini_api(prompt)
                
                if result:
                    st.markdown("### Generated Video Questions:")
                    st.markdown(f"<div class='result-area'>{result}</div>", unsafe_allow_html=True)

# tools/__init__.py
# Import tool modules to make them available when importing from the package

# Import necessary render functions
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

# For easier access, create a dictionary mapping tool names to their render functions
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

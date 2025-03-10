# Teacher Magic

A streamlined AI-powered teaching assistant application that helps educators create high-quality educational content.

## Overview

Teacher Magic is a Streamlit application that provides 19 specialized tools for teachers to generate educational content using Google's Gemini 2.0 Flash AI model. The tools range from lesson planning to assessment generation, student support resources, and communication templates.

## Features

### Core Tools
- **Prompt Builder**: Create structured prompts for AI content generation

### Content Creation
- **Text Generator**: Create texts with controlled reading levels
- **Text Rewriter**: Adapt existing text for different reading levels and purposes
- **Academic Content**: Generate educational content on various topics
- **Lesson Plan Generator**: Create comprehensive lesson plans
- **Unit Plan Generator**: Build multi-week unit plans
- **Image Generator**: Create prompts for educational images

### Assessment
- **MCQ Generator**: Create multiple-choice questions
- **HOT Questions**: Generate higher-order thinking questions
- **Text Dependent Questions**: Create questions based on provided text
- **DOK Questions**: Generate Depth of Knowledge questions
- **YouTube Video Questions**: Create questions for video content

### Student Support
- **Vocabulary Focus**: Generate vocabulary resources
- **Text Proofreader**: Check and improve student writing
- **IEP Goal Responder**: Create individualized education program goals
- **Standards Unpacker**: Break down educational standards

### Communication
- **Email Responder**: Draft responses to emails
- **Email Template Maker**: Create email templates for different scenarios
- **Song Generator**: Create educational songs about curriculum topics

### Additional Features
- **Light/Dark Mode**: Toggle between light and dark themes for comfortable viewing
- **About Information**: Quick access to information about the developer
- **Help Guide**: Instructions for getting started with the app
- **History**: Track and export your generated content

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/teacher-magic.git
   cd teacher-magic
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   streamlit run app.py
   ```

## Usage

1. **Get a Gemini API Key**:
   - Visit [Google AI Studio](https://aistudio.google.com/apikey/)
   - Create a free API key (requires a Google account)

2. **Configure the App**:
   - Enter your API key in the sidebar
   - Click "Save API Key"

3. **Select a Tool**:
   - Choose a tool from the sidebar
   - Fill in the required information
   - Click the generate button

4. **Use Generated Content**:
   - Copy and use the generated content
   - All generations are saved to your session history

## Project Structure

```
teacher-magic/
│
├── app.py                  # Main application file
├── styles.css              # CSS styling
├── requirements.txt        # Package dependencies
│
├── tools/                  # Tool implementations
│   ├── __init__.py
│   ├── content_tools.py    # Content creation tools
│   ├── assessment_tools.py # Assessment tools
│   ├── support_tools.py    # Student support tools
│   └── communication_tools.py # Communication tools
│
└── utils/                  # Utility functions
    ├── __init__.py
    ├── api.py              # API integration with Gemini
    └── data.py             # Educational data and helper functions
```

## Requirements

- Python 3.8+
- Streamlit
- Google generative AI SDK
- Pandas
- Internet connection for API calls

## About the Developer

Teacher Magic is made by Gary Stanyard for the benefit of colleagues in Brunei and beyond. Contact Gary at gstanyard@gmail.com.

## License

[MIT License](LICENSE)

## Acknowledgments

- Educational strategies and Bloom's Taxonomy data from established research
- Developed by G Stanyard
 file
├── styles.css              # CSS styling
├── requirements.txt        # Package dependencies
│
├── tools/                  # Tool implementations
│   ├── __init__.py
│   ├── content_tools.py    # Content creation tools
│   ├── assessment_tools.py # Assessment tools
│   ├── support_tools.py    # Student support tools
│   └── communication_tools.py # Communication tools
│
└── utils/                  # Utility functions
    ├── __init__.py
    ├── api.py              # API integration with Gemini
    └── data.py             # Educational data and helper functions
```

## Requirements

- Python 3.8+
- Streamlit
- Google generative AI SDK
- Pandas
- Internet connection for API calls

## License

[MIT License](LICENSE)

## Acknowledgments

- Educational strategies and Bloom's Taxonomy data from established research
- Developed by G Stanyard

# AI Teaching Assistant Streamlit App

A Streamlit application that helps teachers generate educational content using the Google Gemini API. This app integrates research-based teaching strategies and Bloom's Taxonomy to create high-quality educational resources.

## Features

- **Prompt Builder**: Create structured prompts for AI content generation
- **MCQ Generator**: Generate multiple-choice questions for any topic
- **HOT Questions**: Create higher-order thinking questions based on Bloom's Taxonomy
- **Lesson Plan Generator**: Build complete lesson plans with differentiated teaching strategies
- **Vocabulary Focus**: Generate resources for teaching vocabulary
- **Text Generator**: Create texts with controlled reading levels

## Getting Started

### Prerequisites

- Python 3.8 or higher
- A Google Gemini API key (get one free at [Google AI Studio](https://makersuite.google.com/))

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ai-teaching-assistant.git
   cd ai-teaching-assistant
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

4. Enter your Gemini API key in the sidebar when prompted.

## Usage Guide

1. **Select a tool** from the sidebar navigation
2. **Fill in the required information** for your chosen tool
3. **Click the generate button** to create your content
4. **Copy, review, and use** the generated content in your teaching

## Educational Frameworks

This app integrates:

- **Bloom's Taxonomy** levels (Remember, Understand, Apply, Analyze, Create, Evaluate)
- **Research-based instructional strategies** for different phases of a lesson
- **Reading level control** through Lexile scores and readability metrics
- **Higher-order thinking support** with structured question stems and response frames

## Deployment

This app can be deployed free on Streamlit Cloud:
1. Push your code to GitHub
2. Visit [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Deploy with a single click

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Educational strategies based on research in effective teaching practices
- Question frameworks adapted from Bloom's Taxonomy research
- Lexile score calculation based on established readability measures

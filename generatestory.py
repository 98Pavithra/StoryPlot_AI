import streamlit as st
import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to generate story plot
def generate_story_prompt(genre, theme, characters, setting, plot_elements):
    prompt = f"In the {genre.lower()} genre, there is a story about {characters} set in {setting}. "
    prompt += f"The theme of the story is {theme}. "
    prompt += f"The plot includes the following elements: {plot_elements}."
    return prompt

# Function to generate story plot using OpenAI
def generate_story(genre, theme, characters, setting, plot_elements):
    prompt = generate_story_prompt(genre, theme, characters, setting, plot_elements)
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=600
    )
    generated_text = response.choices[0].text.strip()

    # Define scene explanations
    scene_explanations = [
        "The story begins with the introduction of the main characters.",
        "The protagonist faces the initial challenge or conflict.",
        "A major turning point or revelation occurs.",
        "The climax of the story unfolds, reaching the peak of tension.",
        "Resolution and conclusion of the story."
    ]

    # Split the generated text into scenes
    scenes = generated_text.split("\n\n")

    # Add scene explanations
    story_with_explanation = ""
    for i, scene in enumerate(scenes):
        if i < len(scene_explanations):
            story_with_explanation += f"\n\n[Scene Explanation: {scene_explanations[i]}]\n\n"
        story_with_explanation += f"{scene}\n\n"

    return story_with_explanation
    
# Streamlit UI
st.markdown(
    """
     <style>
    @import url('https://fonts.googleapis.com/css2?family=Brush+Script+MT&display=swap');
    .title-text {
        font-family: 'Brush Script MT', cursive;
        font-size: 85px;
        text-align: center;
        font-weight: bold;
        background: linear-gradient(90deg, rgba(2,0,36,1) 0%, rgba(9,9,121,1) 16%, rgba(143,80,8,1) 30%, rgba(61,112,78,1) 45%, rgba(137,45,137,1) 59%, rgba(192,113,74,1) 78%, rgba(0,212,255,1) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title with custom styling and decorative font
st.markdown('<p class="title-text">AI Story Plot Generator</p>', unsafe_allow_html=True)

# Sidebar inputs
genre = st.sidebar.selectbox(
    "Genre", ["Sci-Fi", "Fantasy", "Mystery", "Romance", "Thriller"],
    help=" * Choose the genre for your story."
)
theme = st.sidebar.text_input(
    "Theme", "", help=" * Briefly describe the central idea or conflict of your story (e.g., love conquers all, redemption, survival)."
)
characters = st.sidebar.text_input(
    "Characters", "", help=" * Introduce your main characters (e.g., a brave knight, a cunning detective, a rebellious teenager)."
)
setting = st.sidebar.text_input(
    "Setting", "", help=" * Describe the world or environment where your story takes place (e.g., a futuristic city, a magical kingdom, a haunted mansion)."
)
plot_elements = st.sidebar.text_area(
    "Desired Plot Elements", "", help=" * List events or challenges your characters will encounter (e.g., a betrayal, a chase scene, a discovery)."
)

if st.sidebar.button("Generate Story Plot"):
    story = generate_story(genre, theme, characters, setting, plot_elements)
    st.write("Generated Story Plot:")
    st.write(story)

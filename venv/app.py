import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure Google Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set up the model
model = genai.GenerativeModel('gemini-pro')

def generate_jokes(topic, decade, num_jokes, dark_humor_scale):
    prompt = f"""Generate {num_jokes} Bollywood jokes about {topic} from the {decade}s decade.
    The jokes should have a humor level of {dark_humor_scale} out of 5, where 1 is very mild and 5 is edgy but not offensive.
    Format the jokes as a numbered list."""

    try:
        response = model.generate_content(prompt)
        
        if response.parts:
            return response.text
        else:
            # Check safety ratings
            if response.prompt_feedback:
                safety_ratings = response.prompt_feedback.safety_ratings
                blocked_categories = [rating.category for rating in safety_ratings if rating.probability == "HIGH"]
                return f"Response was blocked due to safety concerns in the following categories: {', '.join(blocked_categories)}. Please try adjusting your parameters."
            else:
                return "The response was empty. Please try adjusting your parameters."
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Streamlit app
st.title("Bollywood Jokes Generator")

# Input fields
topic = st.text_input("Enter a topic:")
decade = st.selectbox("Select Bollywood Decade:", ["1950s", "1960s", "1970s", "1980s", "1990s", "2000s", "2010s", "2020s"])
num_jokes = st.slider("Number of jokes:", min_value=1, max_value=10, value=5)
dark_humor_scale = st.slider("Humor Scale:", min_value=1, max_value=5, value=3, help="1 is very mild, 5 is edgy but not offensive")

# Generate button
if st.button("Generate Jokes"):
    if topic:
        with st.spinner("Generating jokes..."):
            jokes = generate_jokes(topic, decade, num_jokes, dark_humor_scale)
        st.write(jokes)
    else:
        st.warning("Please enter a topic.")

# Instructions for running the app
if __name__ == "__main__":
    st.sidebar.header("How to run the app:")
    st.sidebar.markdown("""
    1. Install required packages: `pip install streamlit google-generativeai python-dotenv`
    2. Set up your Google API key in a `.env` file: `GOOGLE_API_KEY=your_api_key_here`
    3. Run the app: `streamlit run app.py`
    """)
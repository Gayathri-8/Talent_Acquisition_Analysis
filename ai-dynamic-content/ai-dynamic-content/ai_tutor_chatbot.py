import streamlit as st
from transformers import pipeline, set_seed
import os

# Set up text-generation model from Hugging Face
@st.cache_resource
def get_model():
    return pipeline("text-generation", model="gpt2")

generator = get_model()
set_seed(42)

# Sidebar: Onboarding
with st.sidebar:
    st.title("🧠 Tutor Setup")
    name = st.text_input("Your name", "Student")
    learning_style = st.selectbox("Learning style", ["Visual", "Auditory", "Reading/Writing", "Kinesthetic"])
    is_visually_impaired = st.checkbox("Visually Impaired Mode")
    subject = st.selectbox("Preferred subject", ["Math", "Science", "History", "English", "Geography"])

    if st.button("Start Tutoring"):
        st.session_state.onboarding_done = True
        st.session_state.name = name
        st.session_state.learning_style = learning_style
        st.session_state.is_visually_impaired = is_visually_impaired
        st.session_state.subject = subject
        st.session_state.messages = [
            f"You are a helpful AI tutor named Gyaan. The student is {name}, who learns best through {learning_style.lower()} style and prefers {subject}. " +
            ("They are visually impaired, so avoid visuals and use vivid, descriptive language. " if is_visually_impaired else "") +
            "Explain things simply and interactively like a teacher."
        ]
        st.success("✅ Onboarding completed!")

# Main UI
st.title("📚 AI Tutor: Ask me anything!")
st.caption("Example: Teach me fractions, or explain photosynthesis...")

if st.session_state.get("onboarding_done"):
    user_input = st.chat_input("Type your question here...")

    if user_input:
        st.session_state.messages.append(f"Student: {user_input}")

        with st.spinner("Gyaan is thinking..."):
            # Use the last system prompt + user question as context
            context = " ".join(st.session_state.messages[-2:])
            output = generator(context, max_length=200, num_return_sequences=1, pad_token_id=50256)
            reply = output[0]['generated_text'].split("Student:")[-1].split("Gyaan:")[-1].strip()

        st.session_state.messages.append(f"Gyaan: {reply}")

    # Display chat history
    for msg in st.session_state.messages[1:]:
        role = "assistant" if msg.startswith("Gyaan:") else "user"
        with st.chat_message(role):
            st.markdown(msg.replace("Gyaan: ", "").replace("Student: ", ""))
else:
    st.info("👈 Fill out the onboarding form to start your tutoring session.")
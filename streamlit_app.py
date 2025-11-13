
import streamlit as st
from groq import Groq  # import the SDK client

# Set up title and description
st.title("💬 Chatbot using Groq SDK")
st.write(
    "This is a simple chatbot that uses Groq's Python SDK to generate responses. "
    "You need to provide your Groq API key."
)

# Ask user for their API key
openai_api_key = st.text_input("Groq API Key", type="password")
if not openai_api_key:
    st.info("Please enter your Groq API key to continue.", icon="🗝️")
else:
    # Initialize the Groq client
    client = Groq(api_key=openai_api_key)

    # Initialize session state for messages
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("What’s on your mind?"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Request chat completion from Groq
        response_obj = client.chat.completions.create(
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            model="openai/gpt-oss-20b",  # change to the model you use
            stream=False  # or True if streaming is supported/desired
        )

        # Retrieve the assistant response
        assistant_content = response_obj.choices[0].message.content

        # Add assistant message to history
        st.session_state.messages.append({"role": "assistant", "content": assistant_content})
        with st.chat_message("assistant"):
            st.markdown(assistant_content)

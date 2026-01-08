import streamlit as st
import os
import requests

BACKEND_URL = os.getenv("BACKEND_URL")


st.set_page_config(page_title="AWS S3 RAG Frontend", layout="centered")

st.title("AWS S3 RAG Query Interface")

st.write(
    "This frontend allows you to ask questions to the AWS S3 RAG backend and get responses from your vector store."
)

question = st.text_input("Enter your question:")

if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question first.")
    else:
        with st.spinner("Fetching answer from backend..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/chat",
                    json={"question": question},
                    timeout=10
                )

                if response.status_code == 200:
                    st.success("Answer received!")
                    # Display the JSON nicely
                    answer = response.json()
                    st.json(answer)
                else:
                    st.error(f"Backend returned {response.status_code}: {response.text}")

            except requests.exceptions.RequestException as e:
                st.error(f"Request failed: {e}")

import os
import tempfile
import streamlit as st

from agent import Agent

st.set_page_config(page_title="AskPDF")


def read_and_save_file():
    st.session_state["agent"].forget()  # to reset the knowledge base
    
    for file in st.session_state["file_uploader"]:

        with tempfile.NamedTemporaryFile(delete=False) as tf:
            tf.write(file.getbuffer())
            file_path = tf.name
        
        st.session_state["agent"].ingest(file_path)
        os.remove(file_path)


def is_openai_api_key_set() -> bool:
    return len(st.session_state["OPENAI_API_KEY"]) > 0

def main():
    if len(st.session_state) == 0:
        st.session_state["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY", "")
        if is_openai_api_key_set():
            print('Creating agent')
            st.session_state["agent"] = Agent(st.session_state["OPENAI_API_KEY"])
        else:
            st.session_state["agent"] = None

    st.header("AskPDF")

    if st.text_input("OpenAI API Key", value=st.session_state["OPENAI_API_KEY"], key="input_OPENAI_API_KEY"):
        if len(st.session_state["input_OPENAI_API_KEY"]) > 0 and st.session_state["input_OPENAI_API_KEY"] != st.session_state["OPENAI_API_KEY"]:
            st.session_state["OPENAI_API_KEY"] = st.session_state["input_OPENAI_API_KEY"]
            print('Creating agent')
            st.session_state["agent"] = Agent(st.session_state["OPENAI_API_KEY"])

    st.subheader("Upload a document")
    st.file_uploader(
        "Upload document",
        type=["pdf"],
        key="file_uploader",
        on_change=read_and_save_file,
        label_visibility="collapsed",
        accept_multiple_files=True,
        disabled=not is_openai_api_key_set()
    )

    st.subheader("Ask anything about the PDF")
    user_text = st.text_input("empty", label_visibility="collapsed", key="user_input", disabled=not is_openai_api_key_set())

    if user_text and len(user_text.strip()) > 0:
        user_text = user_text.strip()
        agent_text = st.session_state["agent"].ask(user_text)
        st.subheader("Response")
        st.markdown(agent_text)

    st.divider()
    st.markdown("Source code: [Github](https://github.com/viniciusarruda/askpdf)")


if __name__ == "__main__":
    main()

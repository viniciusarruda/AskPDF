import os
import streamlit as st

from agent import Agent

st.set_page_config(page_title="AskPDF")


def read_and_save_file():
    files = st.session_state["file_uploader"]
    assert type(files) is list
    st.session_state["agent"].forget()  # to reset the knowledge base
    for file in files:
        file_path = os.path.join("data", "pdf", file.name)

        if not os.path.exists(os.path.join("data", "pdf")):
            os.makedirs(os.path.join("data", "pdf"))

        if not os.path.exists(file_path):
            with open(file_path, "wb") as f:
                f.write(file.getbuffer())
            st.session_state["agent"].ingest(file_path)


@st.cache_resource
def get_agent() -> Agent:
    print("Building agent")
    return Agent()


def main():
    if len(st.session_state) == 0:
        st.session_state["agent"] = get_agent()

    st.header("AskPDF")

    st.subheader("Upload a document")
    st.file_uploader(
        "Upload document",
        type=["pdf"],
        key="file_uploader",
        on_change=read_and_save_file,
        label_visibility="collapsed",
        accept_multiple_files=True,
    )

    st.subheader("Ask anything about the PDF")
    user_text = st.text_input("empty", label_visibility="collapsed", key="user_input")

    if user_text and len(user_text.strip()) > 0:
        user_text = user_text.strip()
        agent_text = st.session_state["agent"].ask(user_text)
        st.subheader("Response")
        st.markdown(agent_text)

    st.divider()
    st.markdown("Source code: [Github](https://github.com/viniciusarruda/askpdf)")


if __name__ == "__main__":
    main()

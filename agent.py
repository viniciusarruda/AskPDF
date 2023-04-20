import os
from knowledge_base import KnowledgeBase
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI


class Agent:
    def __init__(self, openai_api_key: str | None = None) -> None:
        # if openai_api_key is None, then it will look the enviroment variable OPENAI_API_KEY
        self.embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        self.kb = KnowledgeBase(embeddings=self.embeddings)
        self.llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
        self.chain = load_qa_chain(self.llm, chain_type="stuff")

    def ask(self, question: str) -> str:
        docs = self.kb.query(question)
        answer = self.chain.run(input_documents=docs, question=question)
        return answer

    def ingest(self, file_path: os.PathLike) -> None:
        self.kb.add_document(file_path)

    def forget(self) -> None:
        self.kb.remove_documents()


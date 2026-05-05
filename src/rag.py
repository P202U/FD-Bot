import ollama
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from utils import Config
from typing import Any


class FinancialAssistant:
    def __init__(self):
        print("....Loading local knowledge base...")
        embeddings = HuggingFaceEmbeddings(model_name=Config.EMBEDDING_MODEL)
        self.vector_db = FAISS.load_local(
            Config.FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True
        )

    def search_context(self, query, k=4):
        docs = self.vector_db.max_marginal_relevance_search(query, k=k, fetch_k=10)

        context_with_metadata = []
        for doc in docs:
            h1 = doc.metadata.get("Header 1", "")
            h2 = doc.metadata.get("Header 2", "")

            breadcrumb = " > ".join(filter(None, [h1, h2])) or "General Info"

            context_with_metadata.append(f"SOURCE [{breadcrumb}]:\n{doc.page_content}")

        return "\n\n---\n\n".join(context_with_metadata)

    def ask(self, user_query: str, stream: bool = True) -> Any:
        context = self.search_context(user_query)

        system_prompt = f"""
        You are a grounded Financial Assistant.
        
        TASK:
        Answer the user's question using the provided CONTEXT. 
        
        RULES:
        1. LANGUAGE: Match the user's language exactly.
        2. CITATIONS: Always cite the SOURCE header provided in the context (e.g., [Section 1.4]).
        3. MATH: If the user asks for a calculation not in the text, you ARE allowed to calculate it 
           using your internal logic, but state: "Calculation based on standard math."
        4. MISSING INFO: If the context is completely irrelevant to the question, 
           say "The report does not cover this specific detail."

        CONTEXT:
        {context}
        """

        return ollama.generate(
            model=Config.LLM_MODEL,
            system=system_prompt,
            prompt=f"<|think|>\n{user_query}",
            options={
                "num_ctx": 4096,
                "temperature": 0.1,
                "top_p": 0.9,
            },
            stream=stream,
        )


if __name__ == "__main__":
    pass

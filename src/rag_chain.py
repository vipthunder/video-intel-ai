# from langchain.chains import create_retrieval_chain
# from langchain.chains.combine_documents import create_stuff_documents_chain

# from langchain_core.prompts import ChatPromptTemplate

# from src.llm import llm


# def create_rag_chain(retriever):

#     prompt = ChatPromptTemplate.from_template(
#         """
#         You are an AI assistant.

#         Answer the question using only the provided context.

#         Context:
#         {context}

#         Question:
#         {input}
#         """
#     )

#     document_chain = create_stuff_documents_chain(
#         llm,
#         prompt
#     )

#     retrieval_chain = create_retrieval_chain(
#         retriever,
#         document_chain
#     )

#     return retrieval_chain

# instead of this o am using langchain chain format like

from operator import itemgetter

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from src.llm import llm


def format_docs(docs):
    return "\n\n".join(
        doc.page_content
        for doc in docs
    )


def create_rag_chain(retriever):

    prompt = ChatPromptTemplate.from_template(
        """
        You are an AI assistant.

        Answer the question using only the provided context.

        Context:
        {context}

        Question:
        {question}
        """
    )

    rag_chain = (
        {
            "context":
                itemgetter("question")
                | retriever
                | format_docs,

            "question":
                itemgetter("question")
        }
        | prompt| llm | StrOutputParser()
    )

    return rag_chain
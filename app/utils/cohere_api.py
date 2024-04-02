from langchain_cohere import ChatCohere
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import WikipediaLoader
from langchain_cohere import CohereEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
import os
from langchain.chains import create_retrieval_chain
from environs import Env

env = Env()
env.read_env()

def sum_gen(topic):
    llm = ChatCohere(model="command", max_tokens=1000, temperature=0.75, cohere_api_key=env('COHERE_KEY'))
    docs = WikipediaLoader(query=f'{topic}', load_max_docs=1).load()
    embeddings = CohereEmbeddings(cohere_api_key="h0YaTsUOZ6FS40EN8r7EFxYIyQNKzJ00tPciMjam")
    text_splitter = RecursiveCharacterTextSplitter()
    documents = text_splitter.split_documents(docs)
    vector = FAISS.from_documents(documents, embeddings)
    prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

    <context>
    {context}
    </context>

    Question: {input}""")
    document_chain = create_stuff_documents_chain(llm, prompt)
    retriever = vector.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    # response = retrieval_chain.invoke({"input": f"Please summarise this information to highlight the fundamental principles, with some additional detail included."})
    response = retrieval_chain.invoke({"input": """## Instructions \nUsing the included article, perform the following steps:
        \n1. Read through the provided article
        \n2. Extract the 3 most important paragraphs from the article
        \n3. From the paragraphs extracted in step 2, extract the most important sentences from each paragraph
        \n4. Create a summary from the sentences extracted in step 3 in a flowing high natural language quality text. Between 200 and 350 words long.
        \n5. Output only the summary from step 4"""})
    return response["answer"]
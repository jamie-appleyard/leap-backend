from langchain_cohere import ChatCohere
from langchain_community.document_loaders import WebBaseLoader
from langchain_cohere import CohereEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
import os
from langchain.chains import create_retrieval_chain
from .bing_api import bing_search

from environs import Env
env = Env()
env.read_env()

def sum_gen(topic):
    llm = ChatCohere(cohere_api_key=env('COHERE_KEY'))
    urls = bing_search(topic, 5)
    docs = []
    for url in urls:
        loader = WebBaseLoader(url)
        try:
            content = loader.load()
        except:
            continue
        docs = docs + content
    embeddings = CohereEmbeddings(cohere_api_key=env('COHERE_KEY'))
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    documents = text_splitter.split_documents(docs)
    vector = FAISS.from_documents(documents, embeddings)
    prompt = ChatPromptTemplate.from_template("""You are a highly skilled educator who can bring anyone up to a fundamental level of understanding in any topic by giving information on the history, current situation and future of that topic, answer the following question based only on the provided context without using a conversational tone:

    <context>
    {context}
    </context>

    Question: {input}""")
    document_chain = create_stuff_documents_chain(llm, prompt)
    retriever = vector.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    response = retrieval_chain.invoke({"input": f"""## Instructions \nUsing the included text gathered from the top 10 web searches on a set topic, perform the following steps:
            \n1. Read through the provided article for relevant information
            \n2. Extract the 3 most important paragraphs from the provided text
            \n3. From the paragraphs extracted in step 2, extract the most important sentences from each paragraph
            \n4. Create a summary from the sentences extracted in step 3 in a flowing high natural language quality text. Between 300 and 500 words long.
            \n5. Output only the summary from step 4"""})
    return response["answer"]
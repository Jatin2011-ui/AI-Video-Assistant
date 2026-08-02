from dotenv import load_dotenv
load_dotenv()

import os 
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

def get_llm():
    return ChatGroq(model="llama-3.1-8b-instant",groq_api_key=os.getenv("GROQ_API_KEY"),temperature=0.3)

def split_transcript(transcript: str) -> list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 3000,
        chunk_overlap = 200
    ) 
    return splitter.split_text(transcript)

def summarize(transcript: str) -> str:
    llm = get_llm()
    map_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", " summarize this portion of a meeting concisely."),
            ("human", "{text}"),
        ]
    )

    map_chain = map_prompt | llm | StrOutputParser()

    chunks =split_transcript(transcript)

    chunks_summaries = [map_chain.invoke({"text" : chunk}) for chunk in chunks]

    combined = "\n\n".join(chunks_summaries)

    combined_prompt = ChatPromptTemplate.from_messages(
        [
            (
            "system", 
            "You are an expert meeting summarizer. combine these partial summaries "
            "into one final professional meeting summary in bullet points."
            ),
            ("human", "{text}"),
        ]
    )
    
    combined_chain = (
    RunnablePassthrough() | RunnableLambda(lambda x: {"text": x}) | combined_prompt | llm | StrOutputParser()
    )
    return combined_chain.invoke(combined)

def generate_title(transcript: str) -> str:
    llm = get_llm()

    title_chain = (
        RunnablePassthrough() | RunnableLambda(lambda x: {"text": x}) | ChatPromptTemplate.from_messages(
            [
                (
                    "system", 
                    "Based on the meeting transcript, generate a short professional meeting title"
                    "(max 8 words). only return the title, nothing else.",
                ),
                ("human", "{text}"),
            ]
        ) 
        | llm | StrOutputParser()
    )

    return title_chain.invoke(transcript[:2000])
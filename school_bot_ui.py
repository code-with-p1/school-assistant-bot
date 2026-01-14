# school_bot_ui_langchain.py
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import chromadb
import os

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="School Assistant Bot - LangChain + Gemini",
    page_icon="🏫",
    layout="wide"
)

# Suppress some noisy warnings
os.environ['GRPC_VERBOSITY'] = 'ERROR'
os.environ['GLOG_minloglevel'] = '2'

# ─── Initialize Chroma (vector store) ────────────────────────────────────────
@st.cache_resource
def get_chroma_collection():
    client = chromadb.Client()
    
    # Try to get existing collection, create if not exists
    try:
        collection = client.get_collection("school_knowledge")
    except:
        collection = client.create_collection("school_knowledge")
        
        school_facts = [
            "The school library is open from 8 AM to 4 PM on weekdays. Students can borrow up to 3 books at a time.",
            "The principal of the school is Dr. Sarah Smith. Dr. Smith has been the principal for 5 years and holds a PhD in Education.",
            "The school canteen serves pizza every Friday. The menu also includes sandwiches, salads, and drinks.",
            "The computer science lab has 30 computers running the latest software. The lab is available for students during lunch breaks and after school.",
            "All students must wear their ID cards at all times within the school premises. Lost ID cards can be replaced at the administration office for a small fee.",
            "School assembly is held every Monday at 8:30 AM in the main auditorium. Attendance is mandatory for all students.",
            "The basketball team practice is from 3 PM to 5 PM on Tuesdays and Thursdays. Coach Johnson supervises the practice sessions. Students need to try out for the team in the first week of semester.",
            "Basketball is available to all students who make the team through tryouts. Tryouts are held in the first week of each semester.",
            "The school gym is open for general use from 4 PM to 6 PM on weekdays for students who want to practice sports.",
            "To join any school sports team, students must maintain a minimum GPA of 2.5 and have parental permission.",
        ]
        
        collection.add(
            documents=school_facts,
            ids=[f"fact_{i}" for i in range(len(school_facts))]
        )
    
    return collection


# ─── LLM Setup ───────────────────────────────────────────────────────────────
@st.cache_resource
def get_llm():
    return ChatGoogleGenerativeAI(
        model=st.secrets["GEMINI_MODEL"],
        google_api_key=st.secrets["GEMINI_API_KEY"],
        temperature=0.7,
        max_output_tokens=800,
    )


# ─── RAG Chain ───────────────────────────────────────────────────────────────
def create_rag_chain():
    collection = get_chroma_collection()
    llm = get_llm()

    # Simple retriever using Chroma directly
    def retrieve_docs(question: str) -> str:
        results = collection.query(
            query_texts=[question],
            n_results=3
        )
        docs = results['documents'][0]
        return "\n\n".join(docs) if docs else "No relevant information found in school knowledge base."

    retriever = RunnablePassthrough() | retrieve_docs

    # Prompt template
    template = """You are a very friendly and helpful school assistant.  
    Talk to students like a kind older brother/sister would.

    Use the following school information to answer.
    If the information is not enough or you don't know — just say so honestly.

    School information:
    {context}

    Question: {question}

    Answer in natural, conversational language.  
    Do NOT use numbered lists unless the student specifically asks for steps or ranking.  
    Just write a helpful, friendly reply like you would say it in person.

    Important: Only use numbers 1. 2. etc. when the question is clearly asking for steps or multiple separate points.  
    For normal questions, write like a normal conversation.

    Answer:"""

    prompt = ChatPromptTemplate.from_template(template)

    # Chain
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain


# ─── Streamlit UI ────────────────────────────────────────────────────────────
def main():
    st.title("🏫 School Assistant Bot")
    st.caption("LangChain + ChromaDB + Google Gemini")

    # Load chain once
    if "rag_chain" not in st.session_state:
        with st.spinner("Initializing knowledge base & model..."):
            st.session_state.rag_chain = create_rag_chain()

    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Show history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    if prompt := st.chat_input("Ask anything about school..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate answer
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.rag_chain.invoke(prompt)
                    st.markdown(response)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response}
                    )
                except Exception as e:
                    error_msg = f"Error occurred: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": error_msg}
                    )

    # Sidebar controls
    with st.sidebar:
        st.markdown("### Controls")
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

        st.markdown("---")
        st.caption("Tech stack:")
        st.caption("• LangChain")
        st.caption("• ChromaDB (in-memory)")
        st.caption("• Google Gemini")


if __name__ == "__main__":
    main()
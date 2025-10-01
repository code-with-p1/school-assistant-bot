# school_bot_ui.py
import streamlit as st
import google.generativeai as genai
import chromadb
import os

# Set page configuration
st.set_page_config(
    page_title="School Assistant Bot - AI-Powered Q&A System",
    page_icon="🏫",
    layout="wide"
)

# Suppress warnings
os.environ['GRPC_VERBOSITY'] = 'ERROR'
os.environ['GLOG_minloglevel'] = '2'

# Initialize ChromaDB
@st.cache_resource
def init_knowledge_base():
    chroma_client = chromadb.Client()
    collection = chroma_client.create_collection(name="my_school_knowledge")
    
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
        ids=[f"id_{i}" for i in range(len(school_facts))]
    )
    return collection

# Initialize Gemini
def init_gemini():
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Main app
def main():
    # Sidebar for configuration
    # with st.sidebar:
    #     st.title("⚙️ Settings")
    #     api_key = st.text_input("Enter your Gemini API Key:", type="password")
    #     if api_key:
    #         genai.configure(api_key=api_key)
    #         st.success("API Key configured!")
        
    #     st.markdown("---")
    #     st.markdown("### About")
    #     st.markdown("This is your AI School Assistant. Ask questions about school rules, schedules, and facilities!")
    
    init_gemini()

    # Main content area
    st.title("🏫 School Assistant Bot - AI-Powered Q&A System")
    st.markdown("Welcome! I'm here to help you with school-related questions.")
    
    # Initialize components
    collection = init_knowledge_base()
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about school..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate bot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Retrieve relevant facts
                    results = collection.query(
                        query_texts=[prompt],
                        n_results=2
                    )
                    
                    relevant_facts = results['documents'][0] if results['documents'][0] else ["No specific information found."]
                    
                    # Create prompt
                    facts_text = "\n".join([f"- {fact}" for fact in relevant_facts])
                    
                    full_prompt = f"""
                    CONTEXT: You are a helpful school assistant answering a student's question.

                    SCHOOL INFORMATION:
                    {facts_text}

                    STUDENT'S QUESTION: {prompt}

                    INSTRUCTIONS:
                    1. Give a direct answer first (Yes/No/Maybe)
                    2. Then explain using the school information
                    3. Be friendly and helpful
                    4. If you don't know, say so

                    Answer:
                    """
                    
                    # Generate response
                    model = genai.GenerativeModel(st.secrets["GEMINI_MODEL"])
                    response = model.generate_content(full_prompt)
                    
                    bot_response = response.text.strip()
                    st.markdown(bot_response)
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": bot_response})
                    
                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
    
    # Clear chat button
    if st.sidebar.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

if __name__ == "__main__":
    main()
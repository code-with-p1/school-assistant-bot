# 🏫 School Assistant Bot - AI-Powered Q&A System

An intelligent School Assistant Bot built with Generative AI and RAG (Retrieval-Augmented Generation) technology. This project demonstrates how AI can provide accurate, context-aware answers about school information by combining semantic search with large language models.

[![AI-School Assistant](https://img.shields.io/badge/AI-School%2520Assistant-blue)] [![Python-3.8+](https://img.shields.io/badge/Python-3.8%252B-green)] [![UI-Streamlit](https://img.shields.io/badge/UI-Streamlit-red)] [![Architecture-RAG](https://img.shields.io/badge/Architecture-RAG-orange)]

## 🎯 Project Overview

This project implements a smart Q&A system that answers questions about school rules, schedules, and facilities. Unlike standard chatbots, it uses RAG architecture to provide factual, reliable answers based on custom school knowledge rather than generic information.

## ✨ Key Features

- 🤖 **Intelligent Q&A**: Get accurate answers about school information
- 🔍 **Semantic Search**: Finds most relevant information using ChromaDB
- 💬 **Beautiful Web Interface**: Streamlit-based chat interface
- 🎯 **Context-Aware**: Understands questions and provides reasoned answers
- 🚀 **Fast & Responsive**: Real-time AI responses
- 🔒 **Privacy-Focused**: Your data stays with you

## 🛠️ Technology Stack

| Component       | Technology          | Purpose                          |
|-----------------|---------------------|----------------------------------|
| AI Model        | Google Gemini API   | Generative AI responses          |
| Vector Database | ChromaDB            | Semantic search & knowledge retrieval |
| Web Framework   | Streamlit           | User interface                   |
| Language        | Python 3.8+         | Backend logic                    |
| Architecture    | RAG (Retrieval-Augmented Generation) | Accurate AI responses |

## 📋 Prerequisites

Before running this project, ensure you have:

- Python 3.8 or higher
- Google Gemini API key [](https://makersuite.google.com/app/apikey)
- Basic understanding of Python and AI concepts

## 🚀 Quick Setup

### Step 1: Clone the Repository

```
git clone https://github.com/yourusername/school-assistant-bot.git
cd school-assistant-bot
```

### Step 2: Create Virtual Environment (Recommended)
```
python -m venv venv

# on Ubuntu:
source venv/bin/activate  

# On Windows: 
venv\Scripts\activate
```

### Step 3: Install Dependencies
```
pip install -r requirements.txt
```

### Step 4: Set Up API Key
Create a .streamlit/secrets.toml file:
```
GEMINI_API_KEY = "your_gemini_api_key_here"
GEMINI_MODEL = "your_gemini_model_name_here"
```

and create a .env file as well:
```
GEMINI_API_KEY = "your_gemini_api_key_here"
GEMINI_MODEL = "your_gemini_model_name_here"
```

Or set it directly in the code (for testing):
```
# In school_bot_ui.py, replace:
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
# With:
genai.configure(api_key="your_actual_api_key_here")
```

### Step 5: Run the Application
```
streamlit run app.py
```

### Step 6: Access the Bot
Open your browser and go to: http://localhost:8501

## 💡 How It Works
### Architecture Flow
```
User Question → Semantic Search → Relevant Facts → AI Generation → Final Answer
      ↓              ↓               ↓              ↓              ↓
   Input →     ChromaDB Vector   → School Facts → Gemini AI → Response
              Database Search
```

1. **Knowledge Base Setup**
   - School information is stored as vector embeddings in ChromaDB
   - Includes rules, schedules, facilities, and policies

2. **Question Processing**
   - User asks a question through the web interface
   - System performs semantic search to find relevant facts

3. **Intelligent Response Generation**
   - Combines retrieved facts with the original question
   - Uses Gemini AI to generate contextual, accurate answers
   - Provides reasoning and direct responses

## 🎨 Usage Examples

Try asking these questions:

- "When is the library open?"
- "Can anyone join the basketball team?"
- "What do I need to join sports teams?"
- "Who is the principal?"
- "Is computer lab available after school?"

## 📁 Project Structure
```
school-assistant-bot/                     # AI-powered School Assistant using LangChain + Gemini + ChromaDB
├── app.py                          # Main Streamlit application (entry point)
├── requirements.txt                # Project dependencies
├── README.md                       # This file
├── .streamlit/
│   └── secrets.toml                # API keys & configuration (git ignored)
│
├── config/                         # Application-wide constants & settings
│   └── settings.py
│
├── core/                           # LLM and prompt related logic
│   ├── __init__.py
│   ├── llm.py                      # Google Gemini model initialization
│   └── prompt_templates.py         # System & chat prompt definitions
│
├── rag/                            # Retrieval-Augmented Generation components
│   ├── __init__.py
│   ├── vectorstore.py              # Chroma vector database management
│   ├── retriever.py                # Document retrieval logic
│   └── chain.py                    # Full RAG chain (retriever + prompt + LLM)
│
├── data/                           # Static knowledge base
│   └── school_knowledge.py         # School facts/documents used for RAG
│
├── utils/                          # General utilities & helpers
│   ├── __init__.py
│   └── helpers.py                  # Session state, formatting helpers, etc.
│
└── chroma_db/                      # Persistent ChromaDB storage (git ignored)
    └── ... (generated files)
```

## 🔧 Customization

### Adding Your Own School Information

Edit the `SCHOOL_DOCUMENTS` list in `data\school_knowledge.py`:

```python
SCHOOL_DOCUMENTS = [
    "Your custom school information here...",
    "Add as many facts as you need...",
    "The system will automatically learn from these!",
]
```

### Modifying the AI Behavior
Adjust the prompt template in the full_prompt variable:
```
full_prompt = f"""
You are a very friendly, kind and helpful school assistant.
Talk naturally like a supportive older sibling.

Use only the provided school information below to answer.
If you don't have enough information or the topic is not covered — say it honestly.

School information:
{context}

Question: {question}

Answer in natural, conversational style.
Do NOT use numbered lists unless the question is clearly asking for steps or ranking.
Be warm, clear and supportive.Just write a helpful, friendly reply like you would say it in person.

Important: Only use numbers 1. 2. etc. when the question is clearly asking for steps or multiple separate points.  
For normal questions, write like a normal conversation.

Answer:"""
```

# 🌟 Learning Outcomes
This project demonstrates:

- RAG Architecture: Combining retrieval and generation for accurate AI
- Vector Databases: Using ChromaDB for semantic search
- API Integration: Working with Google Gemini AI
- Web Development: Building interactive UIs with Streamlit
- AI Prompt Engineering: Crafting effective prompts for better responses

# 🤝 Contributing
Contributions are welcome! Feel free to:

- Fork the project
- Create a feature branch
- Submit a pull request

# 📝 License
This project is open source and available under the MIT License.

# 🔗 Connect With Me
<img src="https://img.shields.io/badge/LinkedIn-Connect-blue?style=for-the-badge&#x26;logo=linkedin" alt="LinkedIn-Connect"> <img src="https://img.shields.io/badge/GitHub-Follow-black?style=for-the-badge&#x26;logo=github" alt="GitHub-Follow">

# 🚀 Future Enhancements
- Voice input/output capabilities
- Multi-language support
- Integration with school databases
- Mobile app version
- Admin panel for knowledge base management

### ⭐ If you find this project helpful, please give it a star on GitHub!
Built with ❤️ using Python, Streamlit, and Google Gemini AI
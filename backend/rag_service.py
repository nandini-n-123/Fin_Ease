import os
import requests
from bs4 import BeautifulSoup

# LangChain libraries for building the RAG pipeline
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

# --- CONFIGURATION ---
# IMPORTANT: Make sure your Google API Key is set here.
os.environ["GOOGLE_API_KEY"] = "AIzaSyBxZoCwwrwwLAsIoLjT9nfmrlGIzEPnITg"


class RAGService:
    """
    This class encapsulates the entire RAG pipeline, from document processing
    to generating answers. It now supports multilingual queries.
    """
    def __init__(self):
        """
        Initializes the service by loading the necessary AI models.
        """
        # --- Using the smaller, reliable multilingual model ---
        # This new code uses the Google API instead
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables.")

        self.embedding_model = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=google_api_key
        )

        # Initialize the LLM (Gemini)
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest",
                                          temperature=0.3,
                                          convert_system_message_to_human=True)
        
        # Updated prompt template for language instruction
        self.prompt_template = """
        SYSTEM: You are a helpful financial analyst assistant. Answer the user's question based ONLY on the context provided.
        Your answer should be in simple, easy-to-understand language.
        If the context does not contain the answer, state that you cannot find the information in the provided text.
        
        **IMPORTANT**: You MUST answer in the following language: {language}

        CONTEXT:
        {context}

        QUESTION:
        {question}

        ANSWER (in {language}):
        """
        self.prompt = PromptTemplate(template=self.prompt_template, input_variables=["context", "question", "language"])

    def create_vector_store_from_url(self, url: str) -> FAISS:
        """
        This function scrapes a URL and creates a searchable vector store from its content.
        """
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=30) # Increased timeout
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            text = ' '.join(soup.body.stripped_strings)

            if not text:
                print(f"Warning: No text found at URL: {url}")
                return None
            
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            chunks = text_splitter.split_text(text)
            vector_store = FAISS.from_texts(texts=chunks, embedding=self.embedding_model)
            print(f"Vector store created successfully for URL: {url}")
            return vector_store
        except Exception as e:
            print(f"Error processing URL {url}: {e}")
            return None

    def create_rag_chain(self, vector_store: FAISS):
        """
        Creates the full RAG chain that accepts question and language.
        """
        retriever = vector_store.as_retriever(search_kwargs={'k': 5})
        
        rag_chain = (
            {
                "context": lambda x: retriever.invoke(x["question"]),
                "question": lambda x: x["question"],
                "language": lambda x: x["language"]
            }
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
        return rag_chain


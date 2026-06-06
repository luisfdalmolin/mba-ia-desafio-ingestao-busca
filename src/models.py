import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

load_dotenv()

def get_embedding_model():
    if 'OPENAI_API_KEY' in os.environ: # Prefer OpenAI over Google if both keys are present
        return OpenAIEmbeddings(model=os.getenv('OPENAI_EMBEDDING_MODEL', 'text-embedding-3-small'))
    elif 'GOOGLE_API_KEY' in os.environ:
        return GoogleGenerativeAIEmbeddings(model=os.getenv('GOOGLE_EMBEDDING_MODEL', 'gemini-embedding-2'))
    else:
        raise EnvironmentError('No valid API key found. OPENAI_API_KEY or GOOGLE_API_KEY must be set in the environment variables')

def get_llm_model(temperature=0.5):
    if 'OPENAI_API_KEY' in os.environ:
        return ChatOpenAI(model=os.getenv('OPENAI_LLM_MODEL', 'gpt-5.4-nano'), temperature=temperature)
    elif 'GOOGLE_API_KEY' in os.environ:
        return ChatGoogleGenerativeAI(model=os.getenv('GOOGLE_LLM_MODEL', 'gemini-2.5-flash'), temperature=temperature)
    else:
        raise EnvironmentError('No valid API key found. OPENAI_API_KEY or GOOGLE_API_KEY must be set in the environment variables')

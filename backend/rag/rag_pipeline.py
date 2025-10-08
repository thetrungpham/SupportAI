from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint
from langchain.memory import ConversationSummaryMemory
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from dotenv import load_dotenv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
BACKEND_DIR = os.path.dirname(BASE_DIR)                
load_dotenv(os.path.join(BACKEND_DIR, ".env"))

def load_vector_store():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return FAISS.load_local(
        "D:\\Python\\chatbotAI\\backend\\rag\\embeddings",
        embeddings,
        allow_dangerous_deserialization=True
    )


def create_qa_chain():
    vector_store = load_vector_store()
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",  # có thể đổi sang gemini-1.5-pro nếu muốn
        api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.2
    )
    prompt = ChatPromptTemplate.from_messages([
    ("system", "Bạn là một trợ lý AI hữu ích. Dựa vào tài liệu sau để trả lời câu hỏi. "
               "Nếu không tìm thấy thông tin trong tài liệu thì nói 'Không có trong dữ liệu'. "
               "Tài liệu:\n{context}"),
    ("user", "{input}")
    ])
    history_aware_retriever = create_history_aware_retriever(llm, retriever, prompt)
    document_chain = create_stuff_documents_chain(llm, prompt)

    # Bước 3: ghép lại thành retrieval chain
    qa_chain = create_retrieval_chain(history_aware_retriever, document_chain)

    return qa_chain

def answer_query(query):
    qa_chain = create_qa_chain()
    result = qa_chain.invoke({"input":query, "chat_history":[]})
    return result["answer"]

# Load data
#loader = DirectoryLoader('documents/data', glob='**/*.txt')
#documents = loader.load()
# Build vector store
#vector_store = build_vector_store(documents)
# Create QA chain
#qa_chain = create_qa_chain(vector_store)

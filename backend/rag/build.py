from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


def build_vector_store():
    intro_loader = DirectoryLoader(
        'D:\\Python\\chatbotAI\\backend\\rag\\documents\\Introduction',
        glob="**/*.md",
        loader_cls=lambda path: TextLoader(path, encoding="utf-8")
    )
    train_loader = DirectoryLoader(
        "D:\\Python\\chatbotAI\\backend\\rag\\documents\\Training",
        glob="**/*.md",
        loader_cls=lambda path: TextLoader(path, encoding="utf-8")
    )

    intro_docs = intro_loader.load()
    train_docs = train_loader.load()
    documents = intro_docs + train_docs

    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = FAISS.from_documents(texts, embeddings)
    vector_store.save_local("D:\\Python\\chatbotAI\\backend\\rag\\embeddings")

    return vector_store

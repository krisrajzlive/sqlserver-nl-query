"""LangChain implementation: text-to-SQL, FAISS vector RAG, and a router over both."""
from pathlib import Path

from langchain_community.utilities import SQLDatabase
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings

from . import config
from .result import Answer
from .sqlguard import assert_read_only, clean_sql

INDEX_DIR = Path("index_store/langchain")
TEXT_COLUMNS = "HotelId, HotelName, City, Country, Category, Rating, PricePerNight, Tags, Description"


def _llm() -> AzureChatOpenAI:
    a = config.azure()
    # GPT-5 family are reasoning models: leave temperature unset.
    return AzureChatOpenAI(
        azure_endpoint=a["endpoint"], api_key=a["api_key"],
        api_version=a["api_version"], azure_deployment=a["chat"],
    )


def _embeddings() -> AzureOpenAIEmbeddings:
    a = config.azure()
    return AzureOpenAIEmbeddings(
        azure_endpoint=a["endpoint"], api_key=a["api_key"],
        api_version=a["api_version"], azure_deployment=a["embedding"],
    )


def _db() -> SQLDatabase:
    return SQLDatabase.from_uri(config.sql_url(), include_tables=["Hotels"])


def build_index() -> int:
    rows = _db()._execute(f"SELECT {TEXT_COLUMNS} FROM dbo.Hotels")
    docs = [
        Document(
            page_content=f"{r['HotelName']} ({r['City']}, {r['Country']}). {r['Category']}. "
                         f"Tags: {r['Tags']}. {r['Description']}",
            metadata={"hotel_id": r["HotelId"], "name": r["HotelName"], "city": r["City"],
                      "rating": float(r["Rating"]), "price": float(r["PricePerNight"])},
        )
        for r in rows
    ]
    INDEX_DIR.parent.mkdir(exist_ok=True)
    FAISS.from_documents(docs, _embeddings()).save_local(str(INDEX_DIR))
    return len(docs)


def ask_sql(question: str) -> Answer:
    db, llm = _db(), _llm()
    gen = ChatPromptTemplate.from_messages([
        ("system", "You write a single read-only T-SQL SELECT for SQL Server (use TOP, not LIMIT). "
                   "Return only the SQL, no commentary.\nSchema:\n{schema}"),
        ("human", "{question}"),
    ]) | llm | StrOutputParser()
    sql = assert_read_only(clean_sql(gen.invoke({"schema": db.get_table_info(), "question": question})))
    result = db.run(sql)
    ans = ChatPromptTemplate.from_template(
        "Question: {q}\nSQL: {sql}\nResult: {res}\nAnswer concisely in plain language."
    ) | llm | StrOutputParser()
    return Answer(ans.invoke({'q': question, 'sql': sql, 'res': result}), sql=sql, route="sql")


def ask_vector(question: str, k: int = 4) -> Answer:
    store = FAISS.load_local(str(INDEX_DIR), _embeddings(), allow_dangerous_deserialization=True)
    context = "\n\n".join(d.page_content for d in store.similarity_search(question, k=k))
    text = (ChatPromptTemplate.from_template(
        "Answer using only these hotel descriptions. Name the best matches.\n\n{ctx}\n\nQuestion: {q}"
    ) | _llm() | StrOutputParser()).invoke({"ctx": context, "q": question})
    return Answer(text)


def ask(question: str) -> Answer:
    route = (ChatPromptTemplate.from_template(
        "Reply with exactly 'sql' if the question needs filtering, counting, sorting or numbers over "
        "columns (rating, price, city, parking), or 'vector' if it asks about vibe, atmosphere or "
        "free-text description.\nQuestion: {q}"
    ) | _llm() | StrOutputParser()).invoke({"q": question}).strip().lower()
    return ask_vector(question) if route.startswith("vector") else ask_sql(question)

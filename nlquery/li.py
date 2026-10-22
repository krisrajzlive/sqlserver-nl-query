"""LlamaIndex implementation: NL-to-SQL engine, vector index, and a router over both."""
from pathlib import Path

from llama_index.core import Document, Settings, SQLDatabase, StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.core.query_engine import NLSQLTableQueryEngine, RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector
from llama_index.core.tools import QueryEngineTool
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.llms.azure_openai import AzureOpenAI
from sqlalchemy import create_engine, text

from . import config
from .result import Answer

INDEX_DIR = Path("index_store/llamaindex")


def _configure() -> None:
    a = config.azure()
    Settings.llm = AzureOpenAI(
        engine=a["chat"], model=a["chat"], azure_endpoint=a["endpoint"],
        api_key=a["api_key"], api_version=a["api_version"],
    )
    Settings.embed_model = AzureOpenAIEmbedding(
        engine=a["embedding"], model=a["embedding"], azure_endpoint=a["endpoint"],
        api_key=a["api_key"], api_version=a["api_version"],
    )


def build_index() -> int:
    _configure()
    with create_engine(config.sql_url()).connect() as c:
        rows = c.execute(text("SELECT HotelId, HotelName, City, Country, Category, Rating, "
                              "PricePerNight, Tags, Description FROM dbo.Hotels")).mappings().all()
    docs = [
        Document(
            text=f"{r['HotelName']} ({r['City']}, {r['Country']}). {r['Category']}. "
                 f"Tags: {r['Tags']}. {r['Description']}",
            metadata={"hotel_id": r["HotelId"], "name": r["HotelName"], "city": r["City"],
                      "rating": float(r["Rating"]), "price": float(r["PricePerNight"])},
        )
        for r in rows
    ]
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    VectorStoreIndex.from_documents(docs).storage_context.persist(str(INDEX_DIR))
    return len(docs)


def _engines():
    _configure()
    sql_engine = NLSQLTableQueryEngine(
        sql_database=SQLDatabase(create_engine(config.sql_url()), include_tables=["Hotels"]),
        tables=["Hotels"],
    )
    index = load_index_from_storage(StorageContext.from_defaults(persist_dir=str(INDEX_DIR)))
    return sql_engine, index.as_query_engine(similarity_top_k=4)


def ask(question: str) -> Answer:
    sql_engine, vector_engine = _engines()
    router = RouterQueryEngine(
        selector=LLMSingleSelector.from_defaults(),
        query_engine_tools=[
            QueryEngineTool.from_defaults(
                sql_engine, name="sql",
                description="Counts, filters, sorting and numeric questions over hotel columns "
                            "(rating, price, city, country, category, parking)."),
            QueryEngineTool.from_defaults(
                vector_engine, name="vector",
                description="Semantic questions about atmosphere, vibe or description text."),
        ],
    )
    resp = router.query(question)
    sql = (resp.metadata or {}).get("sql_query")
    return Answer(str(resp), sql=sql, route="sql" if sql else "vector")

import os
from urllib.parse import quote_plus

from dotenv import load_dotenv

load_dotenv()


def sql_url() -> str:
    odbc = (
        f"DRIVER={{{os.getenv('SQL_DRIVER', 'ODBC Driver 18 for SQL Server')}}};"
        f"SERVER={os.getenv('SQL_SERVER', 'localhost')};"
        f"DATABASE={os.getenv('SQL_DATABASE', 'HotelsDb')};"
        "Trusted_Connection=yes;TrustServerCertificate=yes;"
    )
    return f"mssql+pyodbc:///?odbc_connect={quote_plus(odbc)}"


def azure() -> dict:
    return {
        "endpoint": os.environ["AZURE_OPENAI_ENDPOINT"],
        "api_key": os.environ["AZURE_OPENAI_API_KEY"],
        "api_version": os.getenv("AZURE_OPENAI_API_VERSION", "2025-04-01-preview"),
        "chat": os.getenv("CHAT_DEPLOYMENT", "gpt-5-nano"),
        "embedding": os.getenv("EMBEDDING_DEPLOYMENT", "text-embedding-3-small"),
    }

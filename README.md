# sqlserver-nl-query

Natural-language querying of a local SQL Server database, implemented twice: with LangChain and with LlamaIndex.

Two retrieval paths, plus a router that picks between them:

- **Text-to-SQL** for filters, counts and numeric questions ("hotels under $150 with parking").
- **Vector search (RAG)** over embedded free-text columns ("quiet, cozy place near water").

## Setup

```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
sqlcmd -S localhost -E -C -i sql/hotels.sql      # creates HotelsDb + dbo.Hotels
cp .env.example .env                              # then fill in endpoint, key, deployment names
```

Requires two Azure AI Foundry deployments: a chat model (e.g. `gpt-5-nano` or `gpt-5-mini`) and `text-embedding-3-small`.

## Usage

```bash
python -m nlquery index --engine langchain
python -m nlquery index --engine llamaindex

python -m nlquery ask "Which hotels under 150 dollars include parking?"
python -m nlquery ask "Somewhere quiet and romantic with good food" --engine llamaindex
python -m nlquery ask "Average price by country" --mode sql
```

## Web UI

```bash
streamlit run app.py
```

Pick the framework and retrieval path in the sidebar, click an example or type a question; the generated SQL is shown in an expander.

## Notes

- LangChain path validates generated SQL (SELECT/WITH only, single statement) before running it. For real use, also connect with a read-only SQL login.
- GPT-5 models are reasoning models, so `temperature` is intentionally left unset.
- Indexes are stored under `index_store/` (git-ignored); re-run `index` after the table changes.

import argparse

from . import lc, li


def main() -> None:
    p = argparse.ArgumentParser(prog="nlquery", description="Natural-language queries over SQL Server")
    p.add_argument("command", choices=["index", "ask"])
    p.add_argument("question", nargs="?")
    p.add_argument("--engine", choices=["langchain", "llamaindex"], default="langchain")
    p.add_argument("--mode", choices=["auto", "sql", "vector"], default="auto",
                   help="LangChain only: force a retrieval path instead of routing")
    args = p.parse_args()
    impl = lc if args.engine == "langchain" else li

    if args.command == "index":
        print(f"Indexed {impl.build_index()} rows with {args.engine}")
        return
    if not args.question:
        p.error("ask requires a question")
    if args.engine == "langchain" and args.mode != "auto":
        print((lc.ask_sql if args.mode == "sql" else lc.ask_vector)(args.question))
    else:
        print(impl.ask(args.question))


if __name__ == "__main__":
    main()

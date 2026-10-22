import re

_FORBIDDEN = re.compile(
    r"\b(insert|update|delete|drop|alter|create|truncate|merge|exec|execute|grant|revoke|xp_\w+)\b",
    re.IGNORECASE,
)


def clean_sql(text: str) -> str:
    """Strip code fences the model may add and return a single statement."""
    text = re.sub(r"^```(?:sql)?|```$", "", text.strip(), flags=re.MULTILINE).strip()
    return text.rstrip(";").strip()


def assert_read_only(sql: str) -> str:
    if not re.match(r"^\s*(select|with)\b", sql, re.IGNORECASE) or _FORBIDDEN.search(sql) or ";" in sql:
        raise ValueError(f"Refusing to run non read-only SQL: {sql!r}")
    return sql

from dataclasses import dataclass


@dataclass
class Answer:
    text: str
    sql: str | None = None
    route: str = "vector"

    def __str__(self) -> str:
        return (f"[SQL] {self.sql}\n" if self.sql else "") + self.text

from pydantic import BaseModel


class SqliteDB(BaseModel):
    path: str = "aiochatgpt.db"
    timezone: str = "Europe/Moscow"
    dialect: str = "aiosqlite"

    class Config:
        allow_mutation = False

    def __str__(self):
        return f"{self.path}"

    @property
    def url(self):
        return (f"sqlite+{self.dialect}://"
                f"{self.path}")

    @property
    def sync_url(self):
        return (f"sqlite://"
                f"{self.path}")

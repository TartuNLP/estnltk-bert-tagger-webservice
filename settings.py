from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    max_content_length: int = 200000
    bert_model: str = "tartuNLP/EstBERT"

settings = Settings()
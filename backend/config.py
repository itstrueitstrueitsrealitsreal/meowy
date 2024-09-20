import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration class."""
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    CAT_API_KEY: str = os.getenv("CAT_API_KEY")

    @classmethod
    def validate(cls):
        """Validate that all required configuration values are set."""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set.")
        if not cls.CAT_API_KEY:
            raise ValueError("CAT_API_KEY is not set.")


Config.validate()

from pydantic_settings import BaseSettings


class SharedSettings(BaseSettings):
    """Base settings shared by all services."""
    database_url: str = ""
    supabase_url: str = "https://exjynimkhdamhaqpbcvy.supabase.co"
    environment: str = "production"

    model_config = {"env_file": ".env"}

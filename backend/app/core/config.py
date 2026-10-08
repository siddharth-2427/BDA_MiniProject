import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    HADOOP_NAMENODE_HOST: str = os.getenv("HADOOP_NAMENODE", "namenode")
    HADOOP_NAMENODE_PORT: int = int(os.getenv("HADOOP_NAMENODE_PORT", "9000"))
    HADOOP_NAMENODE_UI_PORT: int = int(os.getenv("HADOOP_NAMENODE_UI_PORT", "9870"))
    
    YARN_RESOURCEMANAGER_HOST: str = os.getenv("YARN_RESOURCEMANAGER", "resourcemanager")
    YARN_RESOURCEMANAGER_PORT: int = int(os.getenv("YARN_RESOURCEMANAGER_PORT", "8088"))
    
    HIVE_SERVER2_HOST: str = os.getenv("HIVE_SERVER2", "hive")
    HIVE_SERVER2_PORT: int = int(os.getenv("HIVE_SERVER2_PORT", "10000"))
    
    PROJECT_ROOT: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    DATA_DIR: str = os.path.join(PROJECT_ROOT, "data")
    MODELS_DIR: str = os.path.join(PROJECT_ROOT, "models")
    STATE_DIR: str = os.path.join(PROJECT_ROOT, "state")
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()

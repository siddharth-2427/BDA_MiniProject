from pathlib import Path
from typing import Dict, Any
from app.core.config import settings
from ml.registry import ModelRegistry

def check_ml_health() -> Dict[str, Any]:
    models_dir = Path(settings.MODELS_DIR)
    registry = ModelRegistry(models_dir)
    plants = registry.get_available_plants()
    return {
        "status": "HEALTHY" if len(plants) > 0 else "NO_MODELS_TRAINED",
        "available_plant_models": plants
    }

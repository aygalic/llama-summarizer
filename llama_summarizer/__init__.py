from pathlib import Path
current_file_path = Path(__file__).resolve()
ROOT_DIR = current_file_path.parent.parent
MODELS_DIR = ROOT_DIR / "models"

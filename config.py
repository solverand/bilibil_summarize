import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

# Load .env early
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
WORKSPACE_DIR = BASE_DIR
STATIC_DIR = WORKSPACE_DIR / "static"
CACHE_DIR = WORKSPACE_DIR / "cache"
COOKIE_PATH = WORKSPACE_DIR / "cookie" / "cookie.json"


@dataclass(frozen=True)
class Settings:
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_base_url: str | None = os.getenv("OPENAI_BASE_URL")
    whisper_model: str = os.getenv("WHISPER_MODEL", "whisper-1")

    # Paths
    workspace_dir: Path = WORKSPACE_DIR
    static_dir: Path = STATIC_DIR
    video_dir: Path = STATIC_DIR / "video"
    speech_dir: Path = STATIC_DIR / "speech"
    text_dir: Path = STATIC_DIR / "text"
    summary_dir: Path = STATIC_DIR / "summary"  # unify name to 'summary'
    analyze_dir: Path = STATIC_DIR / "analyze"
    post_dir: Path = STATIC_DIR / "post"

    cache_bvids_path: Path = CACHE_DIR / "cache_bvids.txt"
    cookie_path: Path = COOKIE_PATH


settings = Settings()


def ensure_directories() -> None:
    """Create required directories if they do not exist."""
    for path in [
        settings.static_dir,
        settings.video_dir,
        settings.speech_dir,
        settings.text_dir,
        settings.summary_dir,
        settings.analyze_dir,
        settings.post_dir,
        settings.cache_bvids_path.parent,
        settings.cookie_path.parent,
    ]:
        path.mkdir(parents=True, exist_ok=True)
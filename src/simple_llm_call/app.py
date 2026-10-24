from pathlib import Path

from dotenv import load_dotenv

from .llm_client import ask_question
from .temperature_demo import run_temperature_demo


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]
    load_dotenv(project_root / ".env")
    print(ask_question("How many moons does Jupiter have?"))
    print("===============================================")

    print(
        ask_question(
            "How many moons does Jupiter have?",
            system_prompt="You are a helpful assistant that answers in short one line",
        )
    )

    print("===============================================")
    run_temperature_demo()
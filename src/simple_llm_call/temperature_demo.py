from .llm_client import ask_question


def run_temperature_demo() -> None:
    prompt = (
        "Write a single tagline for a quirky coffee shop. "
        "Only output the tagline, nothing else."
    )
    for temperature in (0, 1):
        print(f"Temperature {temperature}:")
        print(
            ask_question(
                prompt,
                temperature=temperature,
            )
        )

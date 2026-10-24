import os

from langchain_google_genai import ChatGoogleGenerativeAI


def ask_question(
    question: str,
    *,
    system_prompt: str | None = None,
    model: str | None = None,
    temperature: float | None = None,
) -> str:
    api_url = os.environ["GEMINI_API_URL"].rstrip("/")
    endpoint_suffix = "/v1beta/models"
    if not api_url.endswith(endpoint_suffix):
        raise ValueError(f"GEMINI_API_URL must end with {endpoint_suffix}")

    llm_options: dict[str, str | float] = {
        "model": model or os.getenv("GEMINI_MODEL", "gemini-3.7-flash"),
        "base_url": api_url.removesuffix(endpoint_suffix),
        "api_key": "local",
    }
    if temperature is not None:
        llm_options["temperature"] = temperature
    llm = ChatGoogleGenerativeAI(**llm_options)
    if system_prompt is None:
        response = llm.invoke(question)
    else:
        response = llm.invoke(
            [
                ("system", system_prompt),
                ("human", question),
            ]
        )
    return response.text

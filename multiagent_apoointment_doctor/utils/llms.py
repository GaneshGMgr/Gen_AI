import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from openai import APIConnectionError
from typing import Optional, Tuple, Union
import requests

load_dotenv()

class LLMModel:
    def __init__(self, model_name: str = "llama3", provider: str = "ollama", temperature: float = 0.7):
        if not model_name:
            raise ValueError("Model name must be specified.")

        self.model_name = model_name.lower()
        self.provider = provider.lower()
        self.temperature = temperature

        try:
            if self.provider == "ollama":
                self.model = ChatOllama(
                    model=self.model_name,
                    temperature=self.temperature,
                    base_url='http://localhost:11434',
                    timeout=60,
                    num_ctx=2048,
                    num_gpu=0
                )

            elif self.provider == "openai":
                if not os.getenv("OPENAI_API_KEY"):
                    raise ValueError("OpenAI API key not found in environment")
                self.model = ChatOpenAI(model=self.model_name, temperature=self.temperature)
            else:
                raise ValueError(f"Unsupported provider: {self.provider}")
        except Exception as e:
            raise RuntimeError(f"Model initialization failed: {str(e)}")

    def get_model(self):
        """Returns the underlying LLM model."""
        return self.model

def get_model_with_fallback() -> Tuple[Optional[Union[ChatOpenAI, ChatOllama]], Optional[str]]:
    """Get working LLM with Ollama first, then OpenAI fallback."""
    providers = [
        ("ollama", "llama3"),   # Try Ollama first
        ("openai", "gpt-4o"),   # Fallback to OpenAI
    ]
    
    for provider, model in providers:
        try:
            llm = LLMModel(model_name=model, provider=provider).get_model()
            llm.invoke("Hi, how are you?")  # Test the model
            return llm, provider
        except Exception as e:
            print(f"{provider} ({model}) failed: {str(e)}")
            continue
            
    return None, None  # All providers failed

if __name__ == "__main__":
    model, provider = get_model_with_fallback()
    
    if model:
        print(f"Successfully initialized {provider} model")
        try:
            response = model.invoke("Explain quantum computing simply")
            print(response.content)
        except Exception as e:
            print(f"Generation failed: {str(e)}")
    else:
        print("All model providers failed")
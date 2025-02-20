from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("VENICE_API_KEY"), base_url="https://api.venice.ai/api/v1")

def fetch_and_save_models(output_file="models.json"):
    models = client.models.list()
    model_data = []
    for model in models.data:
        model_dict = {
            "id": model.id,
            "created": model.created,
            "owned_by": model.owned_by,
            "context_tokens": getattr(model, "model_spec", {}).get("availableContextTokens", 65536)
        }
        model_data.append(model_dict)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump({"models": model_data}, f, indent=2)
    print(f"Saved model info to {output_file}")

if __name__ == "__main__":
    fetch_and_save_models()
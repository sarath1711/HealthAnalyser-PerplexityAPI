import json
import requests

def setup_api_key():
    # Your API key here (keep this secure in real apps)
    return "YOUR API KEY"

def build_prompt(text):
    return f"""
You are a highly specialized medical information extraction assistant.
Your task is to analyze the provided patient narrative and extract key information into a structured JSON format.

Instructions:
1. Carefully read the text below.
2. Extract the information and map it to the corresponding fields in the JSON schema.
3. If a piece of information is not mentioned in the text, use "Not mentioned".
4. The output must be a valid JSON object only, without any additional text or markdown formatting.

Patient Narrative:
---
{text}
---

JSON Output Schema:
{{
  "patient_demographics": {{
    "name": "string",
    "age": "integer",
    "occupation": "string"
  }},
  "medical_history": {{
    "primary_diagnosis": "string",
    "diagnosis_duration": "string",
    "contributing_factors": ["string"],
    "family_history": "string"
  }},
  "symptoms": ["string"],
  "diagnostics": {{
    "procedure": "string",
    "findings": "string"
  }},
  "treatment_plan": {{
    "medications": "string",
    "diet": "string",
    "rehabilitation": "string"
  }},
  "current_status": {{
    "outlook": "string",
    "lifestyle_changes": "string"
  }}
}}
"""

def extract_health_info():
    api_key = setup_api_key()
    if not api_key:
        print("API key not configured.")
        return

    # Get user input paragraph
    patient_text = input("Enter the patient health narrative paragraph:\n").strip()
    if not patient_text:
        print("No input provided.")
        return

    prompt = build_prompt(patient_text)

    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "sonar-pro",  # Make sure this model is correct for your API key
        "messages": [
            {"role": "system", "content": "You are a highly specialized medical information extraction assistant."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1000,
        "temperature": 0.2
    }

    print("🤖 Sending request to Perplexity API...")
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"Status Code: {response.status_code}")

        if response.status_code != 200:
            print("❌ Error from API:")
            print(response.text)
            return

        result = response.json()
        assistant_reply = result["choices"][0]["message"]["content"].strip()

        try:
            data = json.loads(assistant_reply)
        except json.JSONDecodeError:
            print("🚨 Error: Could not decode the response into JSON.")
            print("Raw response:", assistant_reply)
            return

        print("\n--- 🩺 Extracted Health Information ---")
        print(json.dumps(data, indent=2))
        print("--------------------------------------\n")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    extract_health_info()

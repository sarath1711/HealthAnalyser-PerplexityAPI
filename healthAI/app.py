from flask import Flask, request, render_template, redirect, url_for
import json

app = Flask(__name__)

# Mock function simulating API response
def get_mock_api_response():
    return {
        "current_status": {
            "lifestyle_changes": "Attends monthly diabetic counseling sessions",
            "outlook": "Motivated to adhere to treatment plan"
        },
        "diagnostics": {
            "findings": "Elevated blood glucose levels and mild kidney impairment",
            "procedure": "Lab tests"
        },
        "medical_history": {
            "contributing_factors": [
                "Hypertension",
                "Obesity"
            ],
            "diagnosis_duration": "8 years",
            "family_history": "Mother diagnosed with diabetes in her 50s",
            "primary_diagnosis": "Type 2 diabetes mellitus"
        },
        "patient_demographics": {
            "age": 60,
            "name": "John Smith",
            "occupation": "Retired engineer"
        },
        "symptoms": [
            "Fatigue",
            "Frequent urination",
            "Occasional blurred vision"
        ],
        "treatment_plan": {
            "diet": "Low-sugar diet",
            "medications": "Daily metformin",
            "rehabilitation": "Regular walking"
        }
    }

def format_health_info(data):
    def format_list(lst):
        if not lst or lst == ["Not mentioned"]:
            return "Not mentioned"
        return ", ".join(lst)

    pd = data.get("patient_demographics", {})
    mh = data.get("medical_history", {})
    symptoms = data.get("symptoms", [])
    diagnostics = data.get("diagnostics", {})
    treatment = data.get("treatment_plan", {})
    status = data.get("current_status", {})

    lines = []

    lines.append("## Structured Health Information\n")

    # Patient Demographics
    lines.append("### Patient Demographics\n")
    lines.append(f"| Name        | Age | Occupation        |")
    lines.append(f"|-------------|-----|-------------------|")
    lines.append(
        f"| {pd.get('name', 'Not mentioned')}  | {pd.get('age', 'Not mentioned')}  | {pd.get('occupation', 'Not mentioned')} |")
    lines.append("")

    # Medical History (With Family History below)
    lines.append("### Medical History\n")
    cfactors = format_list(mh.get("contributing_factors"))
    lines.append(f"| Primary Diagnosis         | Diagnosis Duration | Contributing Factors     |")
    lines.append(f"|---------------------------|--------------------|--------------------------|")
    lines.append(
        f"| {mh.get('primary_diagnosis', 'Not mentioned'):<25} | {mh.get('diagnosis_duration', 'Not mentioned'):<18} | {cfactors:<24} |")
    lines.append(f"\n**Family History:** {mh.get('family_history', 'Not mentioned')}\n")

    # Symptoms
    lines.append("### Symptoms\n")
    if symptoms and symptoms != ["Not mentioned"]:
        for s in symptoms:
            lines.append(f"- {s}")
    else:
        lines.append("Not mentioned")
    lines.append("")

    # Diagnostics
    lines.append("### Diagnostics\n")
    lines.append(f"| Procedure     | Findings                                    |")
    lines.append(f"|---------------|---------------------------------------------|")
    lines.append(
        f"| {diagnostics.get('procedure', 'Not mentioned')}     | {diagnostics.get('findings', 'Not mentioned')} |")
    lines.append("")

    # Treatment Plan
    lines.append("### Treatment Plan\n")
    lines.append(f"| Medications    | Diet           | Rehabilitation     |")
    lines.append(f"|----------------|----------------|--------------------|")
    lines.append(
        f"| {treatment.get('medications', 'Not mentioned'):<15} | {treatment.get('diet', 'Not mentioned'):<14} | {treatment.get('rehabilitation', 'Not mentioned'):<18} |")
    lines.append("")

    # Current Status
    lines.append("### Current Status\n")
    lines.append(f"- **Lifestyle Changes:** {status.get('lifestyle_changes', 'Not mentioned')}")
    lines.append(f"- **Outlook:** {status.get('outlook', 'Not mentioned')}")

    return "\n".join(lines)

@app.route("/", methods=["GET", "POST"])
def index():
    formatted_result = None
    error = None

    if request.method == "POST":
        user_input = request.form.get("patient_text", "").strip()
        if not user_input:
            error = "Please enter valid patient narrative text."
        else:
            api_response = get_mock_api_response()
            formatted_result = format_health_info(api_response)

    return render_template("index.html", result=formatted_result, error=error)

if __name__ == "__main__":
    app.run(debug=True)

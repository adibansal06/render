import json
import os

OUTPUT_DIR = "data/output"

def get_latest_output_file():
    files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith(".json")]
    files.sort(reverse=True)   # timestamped names
    return os.path.join(OUTPUT_DIR, files[0])

def handler(event, context):
    latest_file = get_latest_output_file()

    with open(latest_file, "r") as f:
        leads = json.load(f)

    total_leads = len(leads)

    scores = [
        lead.get("score", 0)
        for lead in leads
        if isinstance(lead, dict)
    ]

    avg_score = round(sum(scores) / len(scores), 2) if scores else 0

    response = {
        "source_file": os.path.basename(latest_file),
        "total_leads": total_leads,
        "average_score": avg_score,
        "leads": leads
    }

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(response)
    }

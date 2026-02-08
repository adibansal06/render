import json

def score_lead(lead):
    score = 0
    score += lead["website_visits"] * 0.3
    score += lead["email_opens"] * 2
    if lead["industry"] == "Energy":
        score += 20
    return round(score, 2)

def handler(event, context):
    with open("data/leads.json") as f:
        leads = json.load(f)

    for lead in leads:
        lead["score"] = score_lead(lead)

    leads.sort(key=lambda x: x["score"], reverse=True)

    avg_score = round(
        sum(l["score"] for l in leads) / len(leads), 2
    )

    response = {
        "total_leads": len(leads),
        "average_score": avg_score,
        "top_lead": leads[0],
        "leads": leads
    }

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(response)
    }

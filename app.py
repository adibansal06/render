from flask import Flask, jsonify, render_template
import os, json

app = Flask(__name__)

OUTPUT_DIR = "data/output"

def get_latest_output_file():
    files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith(".json")]
    files.sort(reverse=True)
    return os.path.join(OUTPUT_DIR, files[0])

def load_leads():
    latest = get_latest_output_file()
    with open(latest, "r") as f:
        leads = json.load(f)
    return leads, os.path.basename(latest)

@app.route("/api/leads")
def api_leads():
    leads, source = load_leads()
    scores = [l.get("score", 0) for l in leads if isinstance(l, dict)]
    avg_score = round(sum(scores) / len(scores), 2) if scores else 0

    return jsonify({
        "source_file": source,
        "total_leads": len(leads),
        "average_score": avg_score,
        "leads": leads
    })

@app.route("/")
def dashboard():
    leads, source = load_leads()
    scores = [l.get("score", 0) for l in leads if isinstance(l, dict)]
    avg_score = round(sum(scores) / len(scores), 2) if scores else 0

    return render_template(
        "dashboard.html",
        leads=leads,
        source_file=source,
        total_leads=len(leads),
        average_score=avg_score
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

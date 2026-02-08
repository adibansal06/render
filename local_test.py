from functions.get_leads import handler
import json

res = handler({}, {})

with open("dashboard/local_output.json", "w") as f:
    f.write(res["body"])

print("Dashboard data generated")


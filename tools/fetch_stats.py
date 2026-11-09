"""Fetch profile numbers and the contribution calendar via the GitHub GraphQL API.
Needs GITHUB_TOKEN in the environment. Writes cache/stats.json and cache/calendar.json."""
import json, os, sys
from pathlib import Path
import requests
ROOT = Path(__file__).resolve().parent.parent
USER = os.environ.get("PROFILE_USER", "PauGon75")
Q = """query($login:String!){user(login:$login){
  followers{totalCount} following{totalCount}
  repositories(ownerAffiliations:OWNER,privacy:PUBLIC){totalCount}
  contributionsCollection{contributionCalendar{totalContributions
    weeks{contributionDays{date contributionCount contributionLevel}}}}}}"""
LV = {"NONE":0,"FIRST_QUARTILE":1,"SECOND_QUARTILE":2,"THIRD_QUARTILE":3,"FOURTH_QUARTILE":4}
r = requests.post("https://api.github.com/graphql", json={"query":Q,"variables":{"login":USER}},
                  headers={"Authorization": f"bearer {os.environ['GITHUB_TOKEN']}"}, timeout=60)
r.raise_for_status()
u = r.json()["data"]["user"]
cal = u["contributionsCollection"]["contributionCalendar"]
days = [[d["date"], LV[d["contributionLevel"]], d["contributionCount"]]
        for w in cal["weeks"] for d in w["contributionDays"]]
(ROOT/"cache").mkdir(exist_ok=True)
(ROOT/"cache/calendar.json").write_text(json.dumps({"days":days,"total":cal["totalContributions"]}, separators=(",",":")))
(ROOT/"cache/stats.json").write_text(json.dumps({"repos":u["repositories"]["totalCount"],
  "followers":u["followers"]["totalCount"],"following":u["following"]["totalCount"],
  "contributions":cal["totalContributions"]}))
print("stats ok")

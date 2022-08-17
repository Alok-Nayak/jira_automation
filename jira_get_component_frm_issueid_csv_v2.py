
import requests
from requests.auth import HTTPBasicAuth
import csv

jira_url = "https://jira.aloksoftware.com"
auth = HTTPBasicAuth("alok", "password_123")

issue_lst = []
component_lst = []
issue_component = {}

with open('issueid.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        issueId = row['issueId']
        url = jira_url + "/rest/api/2/issue/" + issueId
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        response = requests.get(url, headers=headers, auth=auth)
        a = response .json()
        x = [comp["name"] for comp in a["fields"]["components"]]
        components = ("+".join(x))
        try:
            component = components
        except IndexError:
            continue
        issue_component[issueId] = component
        print(f"For Issue Id: {issueId} , Assigned component: {component}")
with open('x_ray_validation_1.csv', 'w') as f:
    for key in issue_component.keys():
        f.write("%s, %s\n" % (key, issue_component[key]))
print("completed!!!")


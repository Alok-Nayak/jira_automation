import requests
from requests.auth import HTTPBasicAuth
import json
import csv

auth = HTTPBasicAuth("alok", "password_123")
project_id = "RZQA"
jira_url = "https://jira.aloksoftware.com"
# from csv file
file_csv = "my_comp.csv"
issuId_column_name = "issueId"
component_column_name = "name"
component_description = "my description"

url = jira_url + "/rest/api/2/project/" + project_id + "/components"
headers = {"Accept": "application/json", "Content-Type": "application/json"}
response = requests.get(url, headers=headers, auth=auth)
a = response.json()

project_comp_lst = []

for i in a:
    val = i['name']
    project_comp_lst.append(val)

# read csv file for component list and issue id

csv_issue_comp_map = {}
csv_issue_lst = []
csv_comp_list = []
with open(file_csv, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        issueId_csv = row[issuId_column_name]
        component_csv = row[component_column_name]
        csv_comp_list.extend(component_csv.split("+"))
        csv_issue_comp_map[issueId_csv] = component_csv
        csv_issue_lst.append(issueId_csv)
# comparing project component with csv list component

component_add_lst = list(set(csv_comp_list).difference(project_comp_lst))
# Add list components in project, if components not in project
url = jira_url + "/rest/api/2/component"
headers = {"Accept": "application/json", "Content-Type": "application/json"}
for i in component_add_lst:
    if i not in project_comp_lst:
        component_add = i
        payload = json.dumps({
            "isAssigneeTypeValid": False,
            "name": component_add,
            "description": component_description,
            "project": project_id
        })
        response = requests.post(url, headers=headers, data=payload, auth=auth)
for issue_id in csv_issue_lst:
    issue_id = issue_id
    # get component from each issue
    url = jira_url + "/rest/api/2/issue/" + issue_id
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    response = requests.get(url, headers=headers, auth=auth)
    ic = response.json()
    data = ic['fields']['components']
    for comp in data:
        issue_component = (comp['name'])
        issue_id = issue_id
        issue_component = issue_component
        # Removing existing components from issue
        print(f"Removing component: {comp}, from issue: {issue_id}")
        url = jira_url + "/rest/api/2/issue/" + issue_id
        payload = json.dumps({
            "update": {
                "components": [
                    {
                        "remove": {
                            "name": issue_component
                        }
                    }
                ]
            }
        })

        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        response = requests.put(url, headers=headers, data=payload, auth=auth)


    comp_add = csv_issue_comp_map[issue_id]
    for component in comp_add.split("+"):
        print(f"Adding component: {comp}, from issue: {issue_id}")
        url = jira_url + "/rest/api/2/issue/" + issue_id
        payload = json.dumps({
            "update": {
                "components": [
                    {
                        "add": {
                            "name": str(component)
                        }
                    }
                ]
            }
        })

        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        response = requests.put(url, headers=headers, data=payload, auth=auth)

    # print(response)


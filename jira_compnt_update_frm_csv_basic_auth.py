# With Basic Authentication

import requests
from requests.auth import HTTPBasicAuth
import json
import csv

auth = HTTPBasicAuth("username", "mypassword")
jira_url = "https://jira-stage.aloksoftware.com"
project_id = "AN"
# from csv file
file_csv = "myfile.csv"
issuId_column_name = "issueId"
component_column_name = "name"
component_description = "compnent of AN project "

url = jira_url + "/rest/api/2/project/" + project_id + "/components"
headers = {"Accept": "application/json", "Content-Type": "application/json"}
response = requests.get(url, headers=headers, auth=auth)
a = response.json()
project_comp_lst = []
for i in a:
    val = i['name']
    project_comp_lst.append(val)
# read csv file for component list and issue id
csv_comp_lst = []
csv_issue_lst = []
with open(file_csv, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        issueId_csv = row[issuId_column_name]
        component_csv = row[component_column_name]
        csv_comp_lst.append(component_csv)
        csv_issue_lst.append(issueId_csv)
# comparing project component with csv list component
component_add_lst = list(set(csv_comp_lst).difference(project_comp_lst))
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
    # list issue in prroject
url = jira_url + "/rest/api/2/search?jql=project=" + project_id + "&maxResults=10000"
headers = {"Accept": "application/json", "Content-Type": "application/json"}
response = requests.get(url, headers=headers, auth=auth)
b = response.json()
for i in b['issues']:
    issue_id = (i['key'])
    # get component from each issu
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
# update latest compoent from csv
count = 0
for issue in csv_issue_lst:
    component_name = csv_comp_lst[count]
    #     print(component_name)
    url = jira_url + "/rest/api/2/issue/" + issue
    payload = json.dumps({
        "update": {
            "components": [
                {
                    "add": {
                        "name": str(component_name)
                    }
                }
            ]
        }
    })

    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    response = requests.put(url, headers=headers, data=payload, auth=auth)
    count += 1
    print(response)
#     a=response.json()
#     print(a)


# add components from csv to project
# get issue components
# remove existing issue components
# add compnents from csv to issue 

import requests
import json
import csv

#Enter details bellow
jira_url = "http://jira.alok.com:8080"
project_id = "AN"
bearer_token = "addyOUrTokEnHerePersonalAcessToken"
# from csv
file_csv = "tr_local.csv"                   #csv file name
issuId_column_name = "issueId"  
component_column_name = "name"              
component_description = "XRAY to ZEPHYR"


url = jira_url + "/rest/api/2/project/" + project_id + "/components"
headers = {"Accept": "application/json", "Content-Type": "application/json",
           'Authorization': 'Bearer'+' '+bearer_token  }
response = requests.get(url, headers=headers)
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
    print(csv_issue_lst)
    print(csv_comp_lst)
# comparing project component with csv list component
component_add_lst = list(set(csv_comp_lst).difference(project_comp_lst))
print(component_add_lst)
# Add list components in project, if components not in project
url = jira_url + "/rest/api/2/component"
headers = {"Accept": "application/json", "Content-Type": "application/json",
           'Authorization': 'Bearer'+' '+bearer_token }
for i in component_add_lst:
    if i not in project_comp_lst:
        compnt_add = i
        payload = json.dumps({
            "isAssigneeTypeValid": False,
            "name": compnt_add,
            "description": component_description,
            "project": project_id
        })
        print(payload)
        response = requests.post(url, headers=headers, data=payload)
        # response = requests.request("POST", url, data=payload, headers=headers)

# list issue in project
url = jira_url + "/rest/api/2/search?jql=project=" + project_id + "&maxResults=10000"
headers = {"Accept": "application/json", "Content-Type": "application/json",
           'Authorization': 'Bearer'+' '+bearer_token }
response = requests.get(url, headers=headers)
b = response.json()
for i in b['issues']:
    issue_id = (i['key'])
    # get component from each issu
    url = jira_url + "/rest/api/2/issue/" + issue_id
    headers = {"Accept": "application/json", "Content-Type": "application/json",
               'Authorization': 'Bearer'+' '+bearer_token }
    response = requests.get(url, headers=headers)
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

        headers = {"Accept": "application/json", "Content-Type": "application/json",
                   'Authorization': 'Bearer'+' '+bearer_token }
        response = requests.put(url, headers=headers, data=payload)
# update latest component from csv
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

    headers = {"Accept": "application/json", "Content-Type": "application/json",
               'Authorization': 'Bearer'+' '+bearer_token }
    response = requests.put(url, headers=headers, data=payload)
    count += 1
    print(response)
#     a=response.json()
#     print(a)


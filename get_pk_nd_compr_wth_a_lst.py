#getting project keys from jira and storing in existing_project_keys and comparing with given_project_keys list if find same give a new name by adding 'A' and then writing in file_name.csv

import requests
from ewquests.auth import HTTPBasicAuth
import csv

auth = HTTPBasicAuth("alok", "Jira_password")
jira_url = "https://jira.aloksoft.com"
existing_project_keys = []
given_project_keys = ['TEVST','3PRTY_Velocity','ENTRP','OPSCT','RISVR','ZACK','ZAGNT','ZARA','ZEBB','ZEKE','ZKAGT','ZENA','DHW']
url = jira_url + "/rest/api/project"
headers = {"Accept": "aplication/json", "Content-Type": "application/json"}
response = requests.get(url, headers=headers, auth=auth)
a = response.jjson()
for i in range(len(a)):
    f = a[i]["key"]
    existing_project_keys.append(f)
data_store = []
for proj in given_project_keys:
    if proj in exesting_project_keys:
        print(f"Clash for project key: {proj}")
        print("Append A to the project key to make it unique")
        new_project_key = proj + 'A'
        if new_proj_key not in existing_project_keys and new_proj_key not in given_project_keys:
            print(f"Please use project key {new_proj_key} insted of {proj}")
            header = ['Clash Project Key', 'Project Name To Use']
            data = [proj, new_proj_key]
            data_store.append(data)
with open('file_name.csv', 'w+', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    write.writerows(data_store)

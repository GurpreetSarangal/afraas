import datetime
import requests
import json

# url = "http://localhost:8000/api/mark/"
# now = datetime.datetime.now()
# data = {
#     "label": "3_3|ksjfjsf", 
#     "status": "absent",
#     "time-stamp" : now
# }

# url = "http://localhost:8000/api/report/"
# now = datetime.datetime.now()
# data = {
#     "type" : "user",
#     "time" : "monthly",
#     "u_id" : 3,
# }
url = "http://localhost:8000/api/report/"
now = datetime.datetime.now()
data = {
    "type" : "department",
    "time" : "weekly",
    "dept_id" : 1,
}


# url = "http://localhost:8000/api/check_registered/"
# data = {
#     "id" : 2,
# }

# Get the current date and time

# Print the date and time
# print("Current date and time: ")
# print(now)
response = requests.post(url, data=data)
json_data = response.text
    
print(json_data) 
data = json.loads(json_data)
if data["error"] != "":
    print(data["error"])
print(data)

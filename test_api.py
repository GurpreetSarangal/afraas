import datetime
import requests
import json

# url = "http://localhost:8000/api/check_registered/"
# now = datetime.datetime.now()
# data = {
#    "id" : 7
# }

# url = "http://localhost:8000/api/mark_face_registered/"
# now = datetime.datetime.now()
# data = {
#    "id" : 7
# }

# url = "http://localhost:8000/api/mark_face_unregistered/"
# now = datetime.datetime.now()
# data = {
#    "id" : 7
# }

# url = "http://localhost:8000/api/report/"
# now = datetime.datetime.now()
# data = {
#     "type" : "user",
#     "time" : "monthly",
#     "u_id" : 3,
# }
# url = "http://localhost:8000/api/report/"
# now = datetime.datetime.now()
# data = {
#     "type" : "department",
#     "time" : "weekly",
#     "dept_id" : 1,
# }


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
if data["success"]:
    print(data["error"])
print(data)

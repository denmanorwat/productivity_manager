import socket
import jsonpickle

from NetworkClasses.RegistrationRequest import RegistrationRequest
from ActionClasses.Action import Action
from ActionClasses.Subaction import Subaction
from NetworkClasses.SetActionsRequest import SetActionsRequest
from NetworkClasses.GetActionsRequest import GetActionsRequest

socket = socket.socket()
nickname = "o"
password = 123
socket.connect(("localhost", 9104))
auth = RegistrationRequest(nickname, 123)
data = jsonpickle.encode(auth)
socket.send(data.encode("utf-8"))
data = socket.recv(8196)
response = jsonpickle.decode(data)
print("Nickname:"+response.nickname)
print("Key:"+str(response.key))
key = response.key
print("State:"+str(response.state))
print("Query:"+str(response.query))
subaction1_1 = Subaction("Denis's birthday", "2000-12-22 00:00:00", "2000-12-22 23:59:59")
subaction1_2 = Subaction("Stanislav's birthday", "2003-01-31 00:00:00", "2003-01-31 23:59:59")
subaction1_3 = Subaction("Elena's birthday", "1970-05-17 00:00:00", "1970-05-17 23:59:59")
subaction1_4 = Subaction("Christ's birthday", "0000-01-01", "0033-05-10 17:59:47")
action1 = Action("Congratulations", "Congratulate all family",
                "2020-01-01 00:00:00", "2020-12-31 23:59:59", 5)
subaction2_1 = Subaction("School start", "2005-09-01 9:00:00", "2005-09-01 15:00:00")
subaction2_2 = Subaction("School end", "2018-31-05 13:00:00", "2018-01-06 05:00:00")
action2 = Action("Graduation", "Graduate from school",
                 "2005-09-01 9:00:00", "2018-01-06 05:00:00", 4)
action1.add_subactions((subaction1_1, subaction1_2, subaction1_3, subaction1_4))
print(str(action1._subactions[0]._id) +str(action1._subactions[1]._id) +
    str(action1._subactions[2]._id) + str(action1._subactions[3]._id))
action2.add_subactions((subaction2_1, subaction2_2))
print(str(action2._subactions[0]._id) +str(action2._subactions[1]._id))
set_action_request = SetActionsRequest(nickname, key, (action1, action2), None)
data = jsonpickle.encode(set_action_request)
socket.send(data.encode("utf-8"))
print("---Data sent---")
data = socket.recv(8196)
response = jsonpickle.decode(data)
print(response.state)

get_actions_request = GetActionsRequest(nickname, key)
data = jsonpickle.encode(get_actions_request)
socket.send(data.encode("utf-8"))
print("Get query sent")
data = socket.recv(65568)
response = jsonpickle.decode(data)
for action in response.actions:
    print("Name: " + action._name + " description: " + action._description + " start_date: " + action._start_date +
          " end_date: " + action._end_date + " id: " + str(action._id) + " mark: " + str(action._mark))
    for subaction in action._subactions:
        print("Desc of subaction:" + subaction._description + " Start date of subaction:" + subaction._date_of_start +
              " End date of subaction:" + subaction._date_of_end + " id of subaction:" + str(subaction._id))
action1 = response.actions[0]
action2 = response.actions[1]
action1.update_subaction(3, "Jesus's birthday")
action2.update_name("Peter")
set_action_request = SetActionsRequest(nickname, key, (action1, action2), None)
data = jsonpickle.encode(set_action_request)
socket.send(data.encode("utf-8"))
print("---Data sent---")
data = socket.recv(8196)
response = jsonpickle.decode(data)
print(response.state)

import socket
from threading import Thread
from io import TextIOWrapper

from HTML_files.Personal_account.Personal_account import page_builder
from HTML_files.Subaction_builder.add_subaction_form import add_subaction_form
from HTML_files.Action_builder.Edit_action_form import edit_action_builder
from HTML_files.Action_builder.Correct_added_action_form import correct_action_builder
from HTML_files.Subaction_builder.correct_subaction_form import correct_subaction_form
from HTML_files.Action_builder.restore_action_form import restore_action_builder
from HTML_files.Statistics_builder.stats_builder import get_stats
from BaseHTTPRequestHandlerFix_fromStackOverflow import HTTPRequest
from ResponseHelper import ResponseHelper
from ActionClasses.Action import Action
from ActionClasses.Subaction import Subaction
from Statistics.stats import Statistics

# Нет куков => есть баги
# Статистика падает, если нечего отображать
class SocketManager:
    def __init__(self, database):
        self.database = database
        self.adr_to_nickname = dict()
        self.listenerSocket = socket.socket()
        self.listenerSocket.bind(("127.0.0.1", 9000))
        self.listenerSocket.listen(1)
# Потом метод talk пойдет ожидать в своём потоке каждого сокета

    def start_acceptance(self):
        print("Started acceptance")
        Thread(target=self.__wait_for_accept()).start()

    def __wait_for_accept(self):
        while True:
            print("Started waiting")
            conn, adr = self.listenerSocket.accept()
            Thread(target=self.__talk, args=(conn, adr)).start()

    def __talk(self, conn, adr):
        cont = True
        while cont:
            try:
                data = conn.recv(8192)
                print(str(data))
                data = HTTPRequest(data)
                #Deauth in proper place since browser always closes socket's
                """ if len(data) == 0:
                    self.database.log_out(adr)
                    break """
                cont = self.__handle(data, conn, adr)
            except ConnectionAbortedError:
                print("Connection aborted")
                self.database.log_out(adr)
                break
        print("Stopped waiting")

    def check_cookies(self, request):
        log_and_key = self.get_login_and_key(request.headers["Cookie"])
        if not isinstance(log_and_key, bool):
            print("I came in")
            login, key = self.get_login_and_key(request.headers["Cookie"])
            if self.database.check_key(login, key):
                print("Correct key")
                return True
        return "You need to log in because you are new user or your session has expired"

    @staticmethod
    def get_login_and_key(cookie_header):
        if cookie_header is not None:
            key_found = False
            login_found = False
            key = None
            login = None
            print(cookie_header)
            for cookie_str in cookie_header.split("; "):
                cookie = cookie_str.split("=")
                if cookie[0] == "key":
                    key = cookie[1]
                    key_found = True
                if cookie[0] == "login":
                    login = cookie[1]
                    login_found = True
            if key_found and login_found:
                return login, key
            else:
                return False
        return False

    @staticmethod
    def parse_post_body(request):
        text_io = TextIOWrapper(request.rfile, encoding="UTF-8")
        splitted_data = text_io.readline().split("&")
        print("Splitted data:" + str(splitted_data))
        text_io.close()
        key_value = dict()
        for data in splitted_data:
            temp = data.split("=")
            key_value.update({temp[0]: temp[1]})
        return key_value

    @staticmethod
    def format_string(string):
        dictionary = {"+": " ", "%3A": ":", "%7E": "~", "%D0%B0": "а", "%D0%B1": "б", "%D0%B2": "в",
                      "%D0%B3": "г", "%D0%B4": "д", "%D0%B5": "е", "%D1%91": "ё", "%D0%B6": "ж",
                      "%D0%B7": "з", "%D0%B8": "и", "%D0%B9": "й", "%D0%BA": "к", "%D0%BB": "л",
                      "%D0%BC": "м", "%D0%BD": "н", "%D0%BE": "о", "%D0%BF": "п", "%D1%80": "р",
                      "%D1%81": "с", "%D1%82": "т", "%D1%83": "у", "%D1%84": "ф", "%D1%85": "х",
                      "%D1%86": "ц", "%D1%87": "ч", "%D1%88": "ш", "%D1%89": "щ", "%D1%8A": "ъ",
                      "%D1%8B": "ы", "%D1%8C": "ь", "%D1%8D": "э", "%D1%8E": "ю", "%D1%8F": "я",
                      "%D0%90": "А", "%D0%91": "Б", "%D0%92": "В", "%D0%93": "Г", "%D0%94": "Д",
                      "%D0%95": "Е", "%D0%81": "Ё", "%D0%96": "Ж", "%D0%97": "З", "%D0%98": "И",
                      "%D0%99": "Й", "%D0%9A": "К", "%D0%9B": "Л", "%D0%9C": "М", "%D0%9D": "Н",
                      "%D0%9E": "О", "%D0%9F": "П", "%D0%A0": "Р", "%D0%A1": "С", "%D0%A2": "Т",
                      "%D0%A3": "У", "%D0%A4": "Ф", "%D0%A5": "Х", "%D0%A6": "Ц", "%D0%A7": "Ч",
                      "%D0%A8": "Ш", "%D0%A9": "Щ", "%D0%AA": "Ъ", "%D0%AB": "Ы", "%D0%AC": "Ь",
                      "%D0%AD": "Э", "%D0%AE": "Ю", "%D0%AF": "Я", "%21": "!", "%40": "@", "%23": "#",
                      "%24": "$", "%25": "%", "%5E": "^", "%26": "&", "%28": "(", "%29": ")", "%2B": "+",
                      "%E2%84%96": "№", "%3B": ";", "%3F": "?", "%2C": ",", "%7C": "|", "%5C": "\\",
                      "%2F": "/", "%22": "\"", "%27": "\'", "%7B": "{", "%7D": "}", "%5B": "[", "%5D": "]",
                      "%3C": "<", "%3E": ">", "#3D": "="}
        patched_string = string
        for key, value in dictionary.items():
            patched_string = patched_string.replace(key, value)
        return patched_string

    @staticmethod
    def unpackage_keys_into_action(keys):
        action = Action(keys["old_name"], keys["old_description"],
                        keys["old_start_date"] + " " + keys["old_start_time"],
                        keys["old_end_date"] + " " + keys["old_end_time"],
                        int(keys["old_mark"]))
        old_action = Action(keys["old_name"], keys["old_description"],
                        keys["old_start_date"] + " " + keys["old_start_time"],
                        keys["old_end_date"] + " " + keys["old_end_time"],
                        int(keys["old_mark"]))
        action._id = int(keys["id"])
        old_action._id = int(keys["id"])
        action.update_name(keys["name"])
        action.update_desc(keys["description"])
        action.update_start_date(keys["start_date"] + " " + keys["start_time"])
        action.update_end_date(keys["end_date"] + " " + keys["end_time"])
        action.update_mark(int(keys["mark"]))
        print("Is action modified:" + str(action.is_modified()))
        old_subactions = dict()
        new_subactions = dict()
        deleted_subactions = list()
        for key, value in keys.items():
            if "~" in key:
                if "deleted" in key:
                    deleted_subactions.append(int(key.split("~")[1]))
                subaction_id = int(key.split("~")[1])
                subaction_field = key.split("~")[0]
                is_old = False
                if "old_" in subaction_field:
                    is_old = True
                    subaction_field = subaction_field[4:]
                if is_old and subaction_id not in old_subactions.keys():
                    old_subactions.update({subaction_id: dict()})
                if not is_old and subaction_id not in new_subactions.keys():
                    new_subactions.update({subaction_id: dict()})
                if is_old:
                    old_subactions[subaction_id].update({subaction_field: value})
                if not is_old:
                    new_subactions[subaction_id].update({subaction_field: value})
        for subaction_id in old_subactions:
            print(old_subactions[subaction_id])
            subaction_dict = old_subactions[subaction_id]
            action._attach_subaction(Subaction(subaction_dict["description"],
                                               subaction_dict["start_date"] + " " + subaction_dict["start_time"],
                                               subaction_dict["end_date"] + " " + subaction_dict["end_time"],
                                               subaction_dict["type"], subaction_id))
            old_action._attach_subaction(Subaction(subaction_dict["description"],
                                               subaction_dict["start_date"] + " " + subaction_dict["start_time"],
                                               subaction_dict["end_date"] + " " + subaction_dict["end_time"],
                                               subaction_dict["type"], subaction_id))
        for subaction_id in new_subactions:
            print(new_subactions[subaction_id])
            subaction_dict = new_subactions[subaction_id]
            action.update_subaction(subaction_id, subaction_dict["description"],
                                    subaction_dict["start_date"] + " " + subaction_dict["start_time"],
                                    subaction_dict["end_date"] + " " + subaction_dict["end_time"],
                                    subaction_dict["type"])
        for subaction_id in deleted_subactions:
            action.delete_subaction(subaction_id)
        return action, old_action

    def check_updated_action(self, new_action):
        print(new_action)
        exception = ""
        action_exception = False
        subaction_exception = False
        sub_end_bigger_than_act_end = False
        sub_start_smaller_than_act_start = False
        tilda_action_exception = False
        tilda_subaction_exception = False
        if ("~" in new_action._name or "~" in new_action._description) and not tilda_action_exception:
            exception += "Symbol (~) is not allowed in action name/description<br>"
            tilda_action_exception = True
        if new_action._start_date >= new_action._end_date and not action_exception:
            exception += "End date of action must be bigger than start date<br>"
            action_exception = True
        for subaction in new_action._subactions:
            if subaction._date_of_end <= subaction._date_of_start and not subaction_exception:
                exception += "End date of subaction must be bigger than start date<br>"
                subaction_exception = True
            if subaction._date_of_end > new_action._end_date and not sub_end_bigger_than_act_end:
                sub_end_bigger_than_act_end = True
                exception += "Subaction's end date must be smaller than action's end date<br>"
            if subaction._date_of_start < new_action._start_date and not sub_start_smaller_than_act_start:
                sub_start_smaller_than_act_start = True
                exception += "Subaction's start date must be bigger than action's start date<br>"
            if ("~" in subaction._description or "~" in subaction._type) and not tilda_subaction_exception:
                tilda_subaction_exception = True
                exception += "Symbol (~) is not allowed in subaction's description/type<br>"
        if not(action_exception or subaction_exception or sub_end_bigger_than_act_end or\
        sub_start_smaller_than_act_start or tilda_subaction_exception or tilda_action_exception):
            return True
        else:
            return exception

    def check_new_action(self, new_action):
        exception = ""
        date_exception = False
        tilda_exception = False
        if new_action._start_date >= new_action._end_date and not date_exception:
            exception += "End date of action must be bigger than start date<br>"
            date_exception = True
        if ("~" in new_action._name or "~" in new_action._description) and not tilda_exception:
            exception +="Symbol (~) is not allowed in action name/description<br>"
            tilda_exception = True
        if not (tilda_exception or date_exception):
            return True
        else:
            return exception

    def check_new_subaction(self, new_subaction, action):
        exception = ""
        subaction_dates_error = False
        action_start_dates_conflict = False
        action_end_dates_conflict = False
        tilda_exception = False
        if "~" in new_subaction._description or "~" in new_subaction._type:
            tilda_exception = True
            exception += "Symbol (~) is not allowed in subaction's description/type<br>"
        if new_subaction._date_of_start >= new_subaction._date_of_end and not subaction_dates_error:
            exception += "End date of subaction must be bigger than start date<br>"
            subaction_dates_error = True
        if new_subaction._date_of_start < action._start_date and not action_start_dates_conflict:
            exception += "Start date of subaction must be bigger than action's <br>" \
                        "Action's start date:" + action._start_date +"<br>"
            action_start_dates_conflict = True
        if new_subaction._date_of_end > action._end_date and not action_end_dates_conflict:
            exception += "End date of subaction must be smaller than action's <br>" \
                        "Action's end date:" + action._end_date +"<br>"
            action_end_dates_conflict = True
        if not(subaction_dates_error or action_start_dates_conflict or
               action_end_dates_conflict or tilda_exception):
            return True
        else:
            return exception


# Этот метод будет переводить запросы и делать необходимые вещи. Для каждого действия свой метод
    def __handle(self, request, conn, adr):

        if request.path == "/authentification":
            if request.command == "POST":
                key_value = self.parse_post_body(request)

                if key_value["type"] == "Authorise":
                    result = self.database.authorise_if_exists(key_value["login"],
                                                            key_value["password"], adr)
                    if isinstance(result, bool):
                        answer = "Wrong login and/or password"
                        response = ResponseHelper.form_response(200, "Ok", "text", answer).encode("utf-8")
                    else:
                        response = ResponseHelper.form_cookie_response(302, "Found", "text",
                                                                       "", key_value["login"],
                                                                       result, "/").encode("utf-8")
                    conn.send(response)
                    conn.close()
                    return False

                if key_value["type"] == "Register":
                    result = self.database.register_if_absent(key_value["login"],
                                                              key_value["password"], adr)
                    if isinstance(result, bool):
                        answer = "Such user already exists. Try anouther one!"
                        response = ResponseHelper.form_response(200, "Ok", "text", answer).encode("utf-8")
                    else:
                        response = ResponseHelper.form_cookie_response(302, "Found", "text",
                                                                       "", key_value["login"],
                                                                       result, "/").encode("utf-8")
                    conn.send(response)
                    conn.close()
                    return False

        elif not isinstance(self.check_cookies(request), bool):
            with open("HTML_files/Registration/authorisation.html") as register:
                body = register.read()
                conn.send(ResponseHelper.form_response(200, "OK", "text", body).encode("utf-8"))
                conn.close()
                return False

        else:
            print(request)
            if request.path == "/":
                login, key = self.get_login_and_key(request.headers["Cookie"])
                actions = self.database.get_actions(login, key)
                actions_file = page_builder(actions)
                conn.send(ResponseHelper.form_response(200, "Ok", "text", actions_file).encode("utf-8"))
                conn.close()
                return False

            elif "request/" in request.path:
                if request.path == "/request/create":
                    print("Yes, create in request")
                    with open("HTML_files/Action_builder/Add action form.html") as add_action:
                        body = add_action.read()
                        conn.send(ResponseHelper.form_response(200, "OK", "text", body).encode("utf-8"))
                        conn.close()

                if request.path == "/request/delete":
                    print("Yes, delete in request")
                    keys = self.parse_post_body(request)
                    login, key = self.get_login_and_key(request.headers["Cookie"])
                    self.database.delete_action(login, key, keys["id"])
                    response = ResponseHelper().form_response(302, "Found", "text", "", "/")
                    conn.send(response.encode("utf-8"))
                    conn.close()
                    return False

                if request.path == "/request/edit":
                    keys = self.parse_post_body(request)
                    login, key = self.get_login_and_key(request.headers["Cookie"])
                    action = self.database.get_action(login, key, keys["id"])
                    body = edit_action_builder(action)
                    print(body)
                    response = ResponseHelper.form_response(200, "Ok", "text", body)
                    conn.send(response.encode("utf-8"))
                    conn.close()
                    return False

                if request.path == "/request/add":
                    keys = self.parse_post_body(request)
                    action_id = keys["id"]
                    body = add_subaction_form(action_id)
                    response = ResponseHelper.form_response(200, "Ok", "text", body)
                    conn.send(response.encode("utf-8"))
                    conn.close()
                    return False

                if request.path == "/request/statistics":
                    with open("HTML_files/Statistics_builder/statistics_preparator.html") as stats:
                        body = stats.read()
                        conn.send(ResponseHelper.form_response(200, "Ok", "text", body).encode("utf-8"))
                        conn.close()
                        return False

            elif request.path == "/add_action":
                print("Add action received")
                keys = self.parse_post_body(request)
                login, key = self.get_login_and_key(request.headers["Cookie"])
                action = Action(self.format_string(keys["name"]), self.format_string(keys["description"]),
                                self.format_string(keys["start_date"] + " " + keys["start_time"]),
                                self.format_string(keys["end_date"] + " " + keys["end_time"]))
                check = self.check_new_action(action)
                if isinstance(check, bool):
                    self.database.add_or_update_actions(login, key, [action])
                    response = ResponseHelper.form_response(302, "Found", "text", "", "/")
                else:
                    body = correct_action_builder(action, check)
                    response = ResponseHelper.form_response(422, "Unprocessable entity", "text", body)
                conn.send(response.encode("utf-8"))
                conn.close()
                return False

            elif request.path == "/add_subaction":
                keys = self.parse_post_body(request)
                login, key = self.get_login_and_key(request.headers["Cookie"])
                father_action = self.database.get_action(login, key, keys["action_id"])
                subaction = Subaction(self.format_string(keys["description"]),
                                      self.format_string(keys["start_date"] + " " + keys["start_time"]),
                                      self.format_string(keys["end_date"] + " " + keys["end_time"]),
                                      self.format_string(keys["type"]))
                check = self.check_new_subaction(subaction, father_action)
                print(father_action._start_date + " " + father_action._end_date)
                print(subaction._date_of_start + " " + subaction._date_of_end)
                if not isinstance(check, bool):
                    body = correct_subaction_form(keys["action_id"], subaction, check)
                    response = ResponseHelper.form_response(422, "Unprocessable entity", "text", body)
                else:
                    self.database.add_subaction(login, key, keys["action_id"], subaction)
                    response = ResponseHelper.form_response(302, "Found", "text", "", "/")
                conn.send(response.encode("utf-8"))
                conn.close()
                return False

            elif request.path == "/cancel":
                response = ResponseHelper.form_response(302, "Found", "text", "", "/")
                conn.send(response.encode("utf-8"))
                conn.close()
                return False

            elif request.path == "/edit":
                keys = self.parse_post_body(request)
                corrected_keys = dict()
                for key, value in keys.items():
                    corrected_keys.update({self.format_string(key): self.format_string(value)})
                login, key = self.get_login_and_key(request.headers["Cookie"])
                action, old_action = self.unpackage_keys_into_action(corrected_keys)
                check = self.check_updated_action(action)
                if not isinstance(check, bool):
                    response = ResponseHelper.form_response(422, "Unprocessable entity", "text",
                                                            restore_action_builder(old_action, action, check))
                else:
                    self.database.add_or_update_actions(login, key, [action])
                    response = ResponseHelper.form_response(302, "Found", "text", "", "/")
                conn.send(response.encode("utf-8"))
                conn.close()
                return False

            elif request.path == "/log_out":
                login, key = self.get_login_and_key(request.headers["Cookie"])
                response = ResponseHelper.form_cookie_response(302, "Found", "text",
                                                               "Log out sucessfully", "", "", "/").encode("utf-8")
                self.database.log_out(login)
                conn.send(response)
                conn.close()
                return False

            elif request.path == "/get_statistics":
                login, key = self.get_login_and_key(request.headers["Cookie"])
                keys = self.parse_post_body(request)
                start_date, end_date = (self.format_string(keys["start_date"] + " " + keys["start_time"]),
                                        self.format_string(keys["end_date"] + " " + keys["end_time"]))
                actions = self.database.get_actions_in_interval(login, key, start_date, end_date)
                if len(actions) != 0:
                    stats = Statistics(actions)
                    body = get_stats(stats)
                else:
                    with open("Statistics/No_stats.html") as no_stats:
                        body = no_stats.read()
                conn.send(ResponseHelper.form_response(200, "Ok", "text", body).encode("utf-8"))
                conn.close()
                return False

            else:
                print("No command recognised. Logging back request: \n")
                print(str(request.path) + " " + str(request.command) + " " + str(request.headers.keys()))

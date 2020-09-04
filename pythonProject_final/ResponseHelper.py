class ResponseHelper:

    @staticmethod
    def form_response(status, status_message, content_type, body, location=None):
        response = "HTTP/1.1 " + str(status) + " " + status_message + "\n" +\
                    "Server: productivity_manager\n"
        if location is not None:
            response += "Location: /" + "\n"
        response += "Content type: " + ResponseHelper.format_content_type(content_type) + "\n" +\
                    "Content legnth: " + str(len(body)) + "\n" +\
                    "Accept-Charset: utf-8" + "\n\n" +\
                    body
        return response

    @staticmethod
    def form_cookie_response(status, status_message, content_type, body, login, key, location=None):
        response = "HTTP/1.1 " + str(status) + " " + status_message + "\n" +\
                   "Server: productivity_manager\n" +\
                   "Content type: " + ResponseHelper.format_content_type(content_type) +\
                   "Content legnth: " + str(len(body)) + "\n" +\
                   "Accept-Charset: utf-8" + "\n"
        if location is not None:
            response += "Location: /" + "\n"
        response += "Set-Cookie: " + "login=" + login + "\n" +\
                   "Set-Cookie: " + "key=" + str(key) + "\n\n" +\
                   body
        return response

    @staticmethod
    def format_content_type(content_type):
        if content_type == "text":
            return "text/html; charset=utf-8"
        if content_type == "png":
            return "image/png"

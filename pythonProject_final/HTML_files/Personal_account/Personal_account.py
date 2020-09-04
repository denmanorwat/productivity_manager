def page_builder(actions):
    actions.sort(key=action_key, reverse=True)
    if actions is False:
        return "Login and/or key is wrong."
    start_string = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Title</title>
    </head>
    <body>
    <form id="empty">  </form>
    <button form=\"empty\" type=\"submit\" formmethod=\"post\" formaction=\"/log_out\"> Log out </button>
    <button form=\"empty\" type=\"submit\" formmethod=\"post\" formaction=\"/request/statistics\"> Get statistics </button>
    <h1> Your current actions: </h1>
    <button form=\"empty\" type=\"submit\" formmethod=\"post\" formaction=\"/request/create\"> Add action </button>
    <ol>
    """
    end_string = """
    </ol>
    </body>
    </html>
        """
    action_string = ""
    for action in actions:
        action_string += (
                """
        <li>
            <font size=\"+1\"> """ + action._name + """ </font>
            <br>
            <font> """ + action._description + """ </font>
            <br>
            <font> """ + "Start date: " + action._start_date + ", End date: " + action._end_date + """
            <br>
            <font> Mark=""" + str(action._mark) + """
            <br>
            <button form=\"empty\" type=\"submit\" formmethod=\"post\" formaction=\"request\\delete\" name=\"id\" value=\"""" + str(action._id) + """\"> Delete </button>
            <button form=\"empty\" type=\"submit\" formmethod=\"post\" formaction=\"request\\edit\" name=\"id\" value=\"""" + str(action._id) + """\"> Edit </button>
            <button form=\"empty\" type=\"submit\" formmethod=\"post\" formaction=\"request\\add\" name=\"id\" value=\"""" + str(action._id) + """\"> Add subaction </button>
            <ol>
            """)
        subaction_string = ""
        for subaction in action._subactions:
            subaction_string += (
                """
                <li>
                <font> """ + subaction._description + """ </font>
                <br>
                <font size=\"-1\"> Type: """ + subaction._type +""" </font>
                <br>
                <font size=\"-1\"> """ + "Start date: " + subaction._date_of_start + ", End date: " + subaction._date_of_end + """ </font>
                <br>
                </li>
                """
            )
        action_string += subaction_string + """
            </ol>
        </li>
        """
    return start_string + action_string + end_string


def action_key(action1):
    return action1._start_date

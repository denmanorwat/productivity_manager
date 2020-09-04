def get_stats(stats):
    start_string = (""" 
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>""")
    time_part = "<br> <font> Amount of time spent on subactions: </font> <br>"
    total_time = stats.total_time
    i = 0
    for type, time in stats.subactions_time.items():
        if i % 2 == 0:
            time_part += "<br>"
        time_part += "<font>" + type + ": " + str(time) + " minutes (" + \
                     str(round(time/total_time*100, 2)) + "% of total time)"
        if i % 2 == 0:
            time_part += ", "
        i += 1
    if i % 2 == 1:
        time_part = time_part[:-1]
    if i % 2 == 0:
        time_part += "<br>"
    time_part += """<font>In total, on actions only you have spent: 
    """ + str(stats.actions_time) + """ minutes (""" + \
                 str(round(stats.actions_time / stats.total_time * 100, 2)) + """% of total time) </font>"""
    mark_part = "<br><br> <font> You have completed: </font> <br>"
    marks = sorted(stats.quantity_of_marks, reverse=True)
    i = 0
    for mark in marks:
        if i % 2 == 0:
            mark_part += "<br>"
        mark_part += str(stats.quantity_of_marks[mark]) + " actions on mark " + str(mark)
        if i % 2 == 0:
            mark_part += ", "
        i += 1
    if i % 2 == 1:
        mark_part = mark_part[:-1]
    if i % 2 == 0:
        mark_part += "<br>"
    actions_part = """<p> List of your actions:</p>
    <ol>"""
    marks = sorted(stats.quantity_of_marks.keys(), reverse=True)
    for mark in marks:
        for action in stats.actions_arranged_by_marks[mark]:
            actions_part += """<li>
            <font>""" + action._name + """</font>
            <br>
            <font size="-1">""" + action._description + """</font>
            <br>
            <font size="-1"> Mark=""" + str(action._mark) + """</font>
            <br>
            <font size="-1">Time spent: """ + str(stats.time_spent_on_actions[action][0]) + "(" \
                            + str(stats.time_spent_on_actions[action][1]) + """% of action's time)
                            </font></li>"""
    end_string = """
    </ol>
</body>
</html>
<form id="empty"></form>
<button form=\"empty\" formmethod=\"post\" formaction=\"/cancel\"> Return to account </button>
    """
    return start_string + time_part + mark_part + actions_part + end_string

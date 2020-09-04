def edit_action_builder(action):
    start_string = (
        """
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="utf-8">
    <title>Title</title>
    </head>
    <body>
    
    """)
    medium_string = """
    <form method="POST" accept-charset="utf-8">
    <label for="name">Name:</label>
    <br>
    <input type="hidden" name="id" value=\"""" + str(action._id) + """\">
    <input type="text" id="name" name="name" value=\"""" + action._name + """\" required>
    <input type="hidden" name="old_name" value=\"""" + action._name + """\">
  <br>
  <label for="description">Description:</label>
  <br>
  <input type="text" id="description" name="description" placeholder="Description" value=\"""" + action._description + """\" required>
  <input type="hidden" name="old_description" value=\"""" + action._description + """\">
  <br>
  <font> Start date and time:</font>
  <br>
  <input type="date" id="start_date" name="start_date" value=\"""" + action._start_date.split(" ")[0] + """\" required><font>   </font>
  <input type="hidden" name="old_start_date" value=\"""" + action._start_date.split(" ")[0] + """\">
  <input type="time" id="start_time" name="start_time" value=\"""" + action._start_date.split(" ")[1] + """\" required>
  <input type="hidden" name="old_start_time" value=\"""" + action._start_date.split(" ")[1] + """\">
  <br>
  <font> End date and time:</font>
  <br>
  <input type="date" id="end_date" name="end_date" value=\"""" + action._end_date.split(" ")[0] + """\" required><font>  </font>
  <input type="hidden" name="old_end_date" value=\"""" + action._end_date.split(" ")[0] + """\">
  <input type="time" id="end_time" name="end_time" value=\"""" + action._end_date.split(" ")[1] + """\" required>
  <input type="hidden" name="old_end_time" value=\"""" + action._end_date.split(" ")[1] + """\">
  <br>
  <font> Mark of your action: </font>
  <input type="number" id="mark" name="mark" value=\"""" + str(action._mark) + """\" required><font>  </font>
  <input type="hidden" name="old_mark" value=\"""" + str(action._mark) + """\">
  <br>
  <br>"""
    if len(action._subactions) != 0:
        medium_string += ("""
        <font> List of subactions: </font>
        <ol>""")
    for subaction in action._subactions:
        medium_string += (
            """
    <li>
      <input type="text" name="description~""" + str(subaction._id) + """\" value=\"""" + subaction._description + """\" required>
      <input type="hidden" name="old_description~""" + str(subaction._id) + """\" value=\"""" + subaction._description + """\">
      <br>
      <input type="text" name="type~""" + str(subaction._id) + """\" value=\"""" + subaction._type + """\" required>
      <input type="hidden" name="old_type~""" + str(subaction._id) + """\" value=\"""" + subaction._type + """\">
      <br>
      <font> Start date and time:</font>
      <br>
      <input type="date" name="start_date~""" + str(subaction._id) + """\" value=\"""" + subaction._date_of_start.split(" ")[0] + """\" required><font>   </font>
      <input type="hidden" name="old_start_date~""" + str(subaction._id) + """\" value=\"""" + subaction._date_of_start.split(" ")[0] + """\">
      <input type="time" name="start_time~""" + str(subaction._id) + """\" value=\"""" + subaction._date_of_start.split(" ")[1] + """\" required>
      <input type="hidden" name="old_start_time~""" + str(subaction._id) + """\" value=\"""" + subaction._date_of_start.split(" ")[1] + """\">
      <br>
      <font> End date and time:</font>
      <br>
      <input type="date" name="end_date~""" + str(subaction._id) + """\" value=\"""" + subaction._date_of_end.split(" ")[0] + """\" required><font>  </font>
      <input type="hidden" name="old_end_date~""" + str(subaction._id) + """\" value=\"""" + subaction._date_of_end.split(" ")[0] + """\">
      <input type="time" name="end_time~""" + str(subaction._id) + """\" value=\"""" + subaction._date_of_end.split(" ")[1] + """\" required>
      <input type="hidden" name="old_end_time~""" + str(subaction._id) + """\" value=\"""" + subaction._date_of_end.split(" ")[1] + """\">
      <br>
      <label for="checkbox"> Delete </label>
      <input type="checkbox" id="checkbox" name=\"deleted~""" + str(subaction._id) + """\" value=\"\"> 
      <br>
      <br>
    </li>""")
    end_string = """    
    </ol>
    <input type="submit" formaction="/edit" id="edit" value="Edit" name="action">
    <input type="submit" formaction="/cancel" id="cancel" value="Cancel" name="action" formnovalidate>
    """
    return start_string + medium_string + end_string

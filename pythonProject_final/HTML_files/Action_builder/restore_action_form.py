def restore_action_builder(old_action, new_action, exception):
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
    <h2 style="color:red" ><b>""" + exception + """</b></h2>
    <br>
    <label for="name">Name:</label>
    <br>
    <input type="hidden" name="id" value=\"""" + str(old_action._id) + """\">
    <input type="text" id="name" name="name" value=\"""" + new_action._name + """\" required>
    <input type="hidden" name="old_name" value=\"""" + old_action._name + """\">
  <br>
  <label for="description">Description:</label>
  <br>
  <input type="text" id="description" name="description" placeholder="Description" value=\"""" + new_action._description + """\" required>
  <input type="hidden" name="old_description" value=\"""" + old_action._description + """\">
  <br>
  <font> Start date and time:</font>
  <br>
  <input type="date" id="start_date" name="start_date" value=\"""" + new_action._start_date.split(" ")[0] + """\" required><font>   </font>
  <input type="hidden" name="old_start_date" value=\"""" + old_action._start_date.split(" ")[0] + """\">
  <input type="time" id="start_time" name="start_time" value=\"""" + new_action._start_date.split(" ")[1] + """\" required>
  <input type="hidden" name="old_start_time" value=\"""" + old_action._start_date.split(" ")[1] + """\">
  <br>
  <font> End date and time:</font>
  <br>
  <input type="date" id="end_date" name="end_date" value=\"""" + new_action._end_date.split(" ")[0] + """\" required><font>  </font>
  <input type="hidden" name="old_end_date" value=\"""" + old_action._end_date.split(" ")[0] + """\">
  <input type="time" id="end_time" name="end_time" value=\"""" + new_action._end_date.split(" ")[1] + """\" required>
  <input type="hidden" name="old_end_time" value=\"""" + old_action._end_date.split(" ")[1] + """\">
  <br>
  <font> Mark of your action: </font>
  <input type="number" id="mark" name="mark" value=\"""" + str(new_action._mark) + """\" required><font>  </font>
  <input type="hidden" name="old_mark" value=\"""" + str(old_action._mark) + """\">
  <br>
  <br>"""
    if len(old_action._subactions) != 0:
        medium_string += ("""
        <font> List of subactions: </font>
        <ol>""")
    for i in range(0, len(old_action._subactions)):
        old_subaction = old_action._subactions[i]
        new_subaction = new_action._subactions[i]
        medium_string += (
                """
        <li>
          <input type="text" name="description~""" + str(new_subaction._id) + """\" value=\"""" + new_subaction._description + """\" required>
      <input type="hidden" name="old_description~""" + str(old_subaction._id) + """\" value=\"""" + old_subaction._description + """\">
      <br>
      <input type="text" name="type~""" + str(new_subaction._id) + """\" value=\"""" + new_subaction._type + """\" required>
      <input type="hidden" name="old_type~""" + str(old_subaction._id) + """\" value=\"""" + old_subaction._type + """\">
      <br>
      <font> Start date and time:</font>
      <br>
      <input type="date" name="start_date~""" + str(new_subaction._id) + """\" value=\"""" +
                new_subaction._date_of_start.split(" ")[0] + """\" required><font>   </font>
      <input type="hidden" name="old_start_date~""" + str(old_subaction._id) + """\" value=\"""" +
                old_subaction._date_of_start.split(" ")[0] + """\">
      <input type="time" name="start_time~""" + str(new_subaction._id) + """\" value=\"""" +
                new_subaction._date_of_start.split(" ")[1] + """\" required>
      <input type="hidden" name="old_start_time~""" + str(old_subaction._id) + """\" value=\"""" +
                old_subaction._date_of_start.split(" ")[1] + """\">
      <br>
      <font> End date and time:</font>
      <br>
      <input type="date" name="end_date~""" + str(new_subaction._id) + """\" value=\"""" +
                new_subaction._date_of_end.split(" ")[0] + """\" required><font>  </font>
      <input type="hidden" name="old_end_date~""" + str(old_subaction._id) + """\" value=\"""" +
                old_subaction._date_of_end.split(" ")[0] + """\">
      <input type="time" name="end_time~""" + str(new_subaction._id) + """\" value=\"""" +
                new_subaction._date_of_end.split(" ")[1] + """\" required>
      <input type="hidden" name="old_end_time~""" + str(old_subaction._id) + """\" value=\"""" +
                old_subaction._date_of_end.split(" ")[1] + """\">
      <br>
      <label for="checkbox"> Delete </label>""")
        if i in new_action._deleted_subactions:
            medium_string += ("""
            <input type="checkbox" id="checkbox" name=\"deleted~""" + str(old_subaction._id) + """\" 
            value=\"\" checked> """)
        else:
            medium_string += (
                    """ <input type="checkbox" id="checkbox" name=\"deleted~""" + str(old_subaction._id) + """\" value=\"\">
            """)
        medium_string += (
            """
      <br>
      <br>
    </li>""")
    end_string = """    
    </ol>
    <input type="submit" formaction="/edit" id="edit" value="Edit" name="action">
    <input type="submit" formaction="/cancel" id="cancel" value="Cancel" name="action" formnovalidate>
    """
    return start_string + medium_string + end_string

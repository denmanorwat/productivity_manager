def correct_subaction_form(id, subaction, exception):
    string = """
    <!DOCTYPE html>
<head>
    <meta charset="utf-8">
    <title>Title</title>
</head>
<body>

<form action="/add_subaction" method="POST" accept-charset="UTF-8">
<h2 style="color:red" ><b>""" + exception + """</b></h2>
  <label for="description">Description:</label>
  <br>
  <input type="text" id="description" name="description" placeholder="Description" 
  value=\"""" + subaction._description + """\" required>
  <br>
  <label for="type">Type:</label>
  <br>
  <input type="text" id="type" name="type" placeholder="Type" value=\"""" + subaction._type + """\" required>
  <input type="hidden" name="action_id" value=\"""" + str(id) + """\">
  <br>
  <font> Start date and time:</font>
  <br>
  <input type="date" id="start_date" name="start_date" 
  value=\"""" + subaction._date_of_start.split(" ")[0] + """\" required><font>   </font>
  <input type="time" id="start_time" name="start_time" 
  value=\"""" + subaction._date_of_start.split(" ")[1] + """\" required>
  <br>
  <font> End date and time:</font>
  <br>
  <input type="date" id="end_date" name="end_date" 
  value=\"""" + subaction._date_of_end.split(" ")[0] + """\" required><font>  </font>
  <input type="time" id="end_time" name="end_time" 
  value=\"""" + subaction._date_of_end.split(" ")[1] + """\" required>
  <br>
  <br>
  <input type="submit" id="add" value="Add" name="action">
  <input type="submit" formaction="/cancel" id="cancel" value="Cancel" name="action" formnovalidate>
</form>
</body>
</html>
    """
    return string
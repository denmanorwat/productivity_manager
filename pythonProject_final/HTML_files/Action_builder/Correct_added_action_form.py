def correct_action_builder(action, exception):
    string = """
    <!DOCTYPE html>
<head>
    <meta charset="utf-8">
    <title>Title</title>
</head>
<body>

<form action="/add_action" method="POST" accept-charset="utf-8">
<h2 style="color:red" ><b>""" + exception + """</b></h2>
  <label for="name">Name:</label>
  <br>
  <input type="text" id="name" name="name" placeholder="Action" value=\"""" + action._name + """\" required>
  <br>
  <label for="description">Description:</label>
  <br>
  <input type="text" id="description" name="description" placeholder="Description" 
  value=\"""" + action._description + """\" required>
  <br>
  <font> Start date and time:</font>
  <br>
  <input type="date" id="start_date" name="start_date" 
  value=\"""" + action._start_date.split(" ")[0] + """\" required><font>   </font>
  <input type="time" id="start_time" name="start_time" value=\"""" + action._start_date.split(" ")[1] + """\" required>
  <br>
  <font> End date and time:</font>
  <br>
  <input type="date" id="end_date" name="end_date" value=\"""" \
             + action._end_date.split(" ")[0] + """\" required><font>  </font>
  <input type="time" id="end_time" name="end_time" value=\"""" + action._end_date.split(" ")[1] + """\" required>
  <br>
  <br>
  <input type="submit" id="add" value="Add" name="action">
  <input type="submit" id="cancel" value="Cancel" name="action" formnovalidate>
</form>
</body>
</html>
    """
    return string
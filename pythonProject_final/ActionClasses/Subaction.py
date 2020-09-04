class Subaction(object):
    def __init__(self, description, start_date, end_date, subaction_type = None , subaction_id=None):
        self._description = description
        self._date_of_start = start_date
        self._date_of_end = end_date
        self._id = subaction_id
        self._type = subaction_type
        self._modified = dict()
        self._modified.update({"description": False, "date_of_start": False,
                               "date_of_finish": False, "type": False})

    def get_field_by_title(self, title):
        if title == "description":
            return "\"" + self._description + "\""
        if title == "date_of_start":
            return "\"" + self._date_of_start + "\""
        if title == "date_of_finish":
            return "\"" + self._date_of_end + "\""
        if title == "id":
            return self._id
        if title == "type":
            return self._type

    def is_modified(self):
        return self._modified["description"] or self._modified["date_of_start"] \
               or self._modified["date_of_finish"] or self._modified["type"]

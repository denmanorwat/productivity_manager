class Action(object):
    def __init__(self, name, description, start_date, end_date, mark=0):
        self._name = name
        self._description = description
        self._start_date = start_date
        self._end_date = end_date
        self._id = None
        self._mark = mark
        self._subactions = []

        self._deleted_subactions = list()
        self._updated_subactions = list()
        self._modified = dict()
        self.__subid = -1
        # При каждом перезапуске subid будет присваиваться -1, а должно быть самое последнее.
        # Исправить потом с помощью файла


    def is_modified(self):
        modified = False
        for key in self._modified:
            modified = modified or self._modified[key]
        return modified

    def update_name(self, new_name):
        if self._name != new_name:
            self._name = new_name
            if self._id is not None:
                self._modified["name"] = True

    def update_desc(self, new_desc):
        print("Old description:" + self._description)
        print("New description:" + new_desc)
        if self._description != new_desc:
            self._description = new_desc
            if self._id is not None:
                self._modified["description"] = True

    def update_start_date(self, new_start_date):
        if self._start_date != new_start_date:
            self._start_date = new_start_date
            if self._id is not None:
                self._modified["date_of_start"] = True

    def update_end_date(self, new_end_date):
        if self._end_date != new_end_date:
            self._end_date = new_end_date
            if self._id is not None:
                self._modified["date_of_finish"] = True

    def update_mark(self, new_mark):
        if self._mark != new_mark:
            self._mark = new_mark
            if self._id is not None:
                self._modified["mark"] = True

    def add_subaction(self, subaction):
        self._subactions.append(subaction)
        if self._id is not None:
            self._updated_subactions.append(subaction._id)

    def get_subaction(self, id):
        for subaction in self._subactions:
            if subaction._id == id:
                return subaction

    def add_subactions(self, subactions):
        for subaction in subactions:
            self.add_subaction(subaction)

    def _attach_subaction(self, subaction):
        self._subactions.append(subaction)

    def _attach_subactions(self, subactions):
        for subaction in subactions:
            self._attach_subaction(subaction)

    def delete_subaction(self, id):
        i = 0
        for subaction in self._subactions:
            if subaction._id == id:
                self._subactions.pop(i)
                if self._id is not None:
                    self._deleted_subactions.append(id)
                    i = 0
                    for upd_id in self._updated_subactions:
                        if upd_id == id:
                            self._updated_subactions.pop(i)
                        i += 1
                break
            i += 1


    def get_field_by_title(self, title):
        if title == "name":
            return "\"" + self._name + "\""
        if title == "description":
            return "\"" + self._description + "\""
        if title == "date_of_start":
            return "\"" + self._start_date + "\""
        if title == "date_of_finish":
            return "\"" + self._end_date + "\""
        if title == "id":
            return self._id
        if title == "mark":
            return "\"" + str(self._mark) + "\""

    def update_subaction(self, id, new_desc=None, new_start_date=None, new_end_date=None, new_type=None):
        for subaction in self._subactions:
            if subaction._id == id:
                if new_desc is not None and subaction._description != new_desc:
                    subaction._description = new_desc
                    if self._id is not None:
                        subaction._modified.update({"description": True})
                if new_start_date is not None and subaction._date_of_start != new_start_date:
                    subaction._date_of_start = new_start_date
                    if self._id is not None:
                        subaction._modified.update({"date_of_start": True})
                if new_end_date is not None and subaction._date_of_end != new_end_date:
                    subaction._date_of_end = new_end_date
                    if self._id is not None:
                        subaction._modified.update({"date_of_finish": True})
                if new_type is not None and subaction._type != new_type:
                    subaction._type = new_type
                    if self._id is not None:
                        subaction._modified.update({"type": True})
                if subaction.is_modified():
                    self._updated_subactions.append(id)
                break

    def get_tupled_deleted_subactions_with_actions(self, action_id):
        list = []
        for elem in self._deleted_subactions:
            list.append((elem, action_id))
        return tuple(list)

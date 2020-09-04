import datetime


class Statistics:
    def __init__(self, actions):
        self.total_time = 0
        self.actions_time = 0
        self.subactions_time = dict()
        self.quantity_of_marks = dict()
        self.subactions_arranged_by_types = dict()
        self.actions_arranged_by_marks = dict()
        self.time_spent_on_actions = dict()
        for action in actions:
            if action._mark not in self.quantity_of_marks.keys():
                self.quantity_of_marks.update({action._mark: 1})
                self.actions_arranged_by_marks.update({action._mark: list()})
                self.actions_arranged_by_marks[action._mark].append(action)
            else:
                self.quantity_of_marks.update({action._mark: self.quantity_of_marks[action._mark] + 1})
                self.actions_arranged_by_marks[action._mark].append(action)

            for subaction in action._subactions:
                if subaction._type not in self.subactions_arranged_by_types.keys():
                    self.subactions_arranged_by_types.update({subaction._type: list()})
                self.subactions_arranged_by_types[subaction._type].append(subaction)

        all_subactions = list()
        for type, subactions in self.subactions_arranged_by_types.items():
            print(type)
            self.subactions_time.update({type: Statistics.time_from_subactions(subactions)})
            all_subactions += self.subactions_arranged_by_types[type]
        for subaction in all_subactions:
            print(subaction._description)
        self.actions_time = Statistics.time_from_actions(actions) - \
                             Statistics.time_from_subactions(all_subactions)
        print(Statistics.time_from_subactions(all_subactions))
        for action in actions:
            action_time = self.time_from_action(action)
            if len(action._subactions) != 0:
                subaction_time = Statistics.time_from_subactions(action._subactions)
                print("Subaction time:" + str(subaction_time))
                self.time_spent_on_actions.update(
                    {action: (action_time-subaction_time,
                          round((action_time-subaction_time)/action_time*100), 2)})
            else:
                self.time_spent_on_actions.update(
                    {action: (action_time, 100)})
        self.total_time = Statistics.time_from_actions(actions)

    @staticmethod
    def time_from_dates(start_date, end_date):
        start_datetime = datetime.datetime(int(start_date[0:4]), int(start_date[5:7]),
                                           int(start_date[8:10]), int(start_date[11:13]),
                                           int(start_date[14:16]), 0)
        end_datetime = datetime.datetime(int(end_date[0:4]), int(end_date[5:7]),
                                         int(end_date[8:10]), int(end_date[11:13]),
                                         int(end_date[14:16]), 0)

        delta = end_datetime - start_datetime
        return delta.total_seconds()//60

    @staticmethod
    def time_from_action(action):
        return Statistics.time_from_dates(action._start_date, action._end_date)

    @staticmethod
    def time_from_subaction(subaction):
        return Statistics.time_from_dates(subaction._date_of_start, subaction._date_of_end)

    @staticmethod
    def time_from_subactions(subactions):
        starting_points = list()
        ending_points = list()
        starting_points.append(subactions[0]._date_of_start)
        ending_points.append(subactions[0]._date_of_end)
        print("____________________________________________________")
        for i in range(1, len(subactions)):
            print("____________________________________________________")
            print("Current subaction:" + subactions[i]._description)
            print("Starting points:" + str(starting_points))
            print("Ending   points:" + str(ending_points))
            new_start = subactions[i]._date_of_start
            new_end = subactions[i]._date_of_end
            print("New starting point:" + new_start)
            print("New ending   point:" + new_end)
            proceed = True
            if new_start <= ending_points[len(ending_points)-1]:
                for j in range(0, len(starting_points)-1):
                    if not proceed:
                        break
                    if new_start < starting_points[j]:
                        print("New starting point:" + new_start + "<" + starting_points[j] + str(j) + "th starting point")
                        for k in range(j, len(starting_points)):
                            if new_end < starting_points[k]:
                                print("New ending point")
                                for l in range(j, k):
                                    starting_points.pop(j)
                                    ending_points.pop(j)
                                starting_points.append(new_start)
                                ending_points.append(new_end)
                                proceed = False
                                break
                            elif new_end <= ending_points[k]:
                                new_end = ending_points[k]
                                for l in range(j, k+1):
                                    starting_points.pop(j)
                                    ending_points.pop(j)
                                starting_points.append(new_start)
                                ending_points.append(new_end)
                                proceed = False
                                break
                    elif new_start <= ending_points[j]:
                        for k in range(j, len(starting_points)):
                            if new_end < starting_points[k]:
                                new_start = starting_points[j]
                                for l in range(j, k+1):
                                    starting_points.pop(j)
                                    ending_points.pop(j)
                                starting_points.append(new_start)
                                ending_points.append(new_end)
                                proceed = False
                                break
                            elif new_end <= ending_points[k]:
                                new_start = starting_points[j]
                                new_end = ending_points[k]
                                for l in range(j, k+1):
                                    starting_points.pop(j)
                                    ending_points.pop(j)
                                starting_points.append(new_start)
                                ending_points.append(new_end)
                                proceed = False
                                break
                        if new_end > ending_points[len(ending_points)-1]:
                            new_start = starting_points[j]
                            for l in range(j, len(ending_points)):
                                starting_points.pop(j)
                                ending_points.pop(j)
                            starting_points.append(new_start)
                            ending_points.append(new_end)

                if new_end < starting_points[len(ending_points) - 1]:
                    starting_points.append(new_start)
                    ending_points.append(new_end)
                else:
                    new_start = min(new_start, starting_points[len(starting_points) - 1])
                    new_end = max(ending_points[len(ending_points) - 1], new_end)
                    starting_points.pop(len(starting_points) - 1)
                    ending_points.pop(len(ending_points) - 1)
                    starting_points.append(new_start)
                    ending_points.append(new_end)
            else:
                starting_points.append(new_start)
                ending_points.append(new_end)
            starting_points.sort()
            ending_points.sort()
        time = 0
        for i in range(0, len(starting_points)):
            time += Statistics.time_from_dates(starting_points[i], ending_points[i])
        return time

    @staticmethod
    def time_from_actions(actions):
        starting_points = list()
        ending_points = list()
        starting_points.append(actions[0]._start_date)
        ending_points.append(actions[0]._end_date)
        print("____________________________________________________")
        for i in range(1, len(actions)):
            print("____________________________________________________")
            print("Current subaction:" + actions[i]._description)
            print("Starting points:" + str(starting_points))
            print("Ending   points:" + str(ending_points))
            new_start = actions[i]._start_date
            new_end = actions[i]._end_date
            print("New starting point:" + new_start)
            print("New ending   point:" + new_end)
            proceed = True
            if new_start <= ending_points[len(ending_points)-1]:
                for j in range(0, len(starting_points)-1):
                    if not proceed:
                        break
                    if new_start < starting_points[j]:
                        print("New starting point:" + new_start + "<" + starting_points[j] + str(j) + "th starting point")
                        for k in range(j, len(starting_points)):
                            if new_end < starting_points[k]:
                                print("New ending point")
                                for l in range(j, k):
                                    starting_points.pop(j)
                                    ending_points.pop(j)
                                starting_points.append(new_start)
                                ending_points.append(new_end)
                                proceed = False
                                break
                            elif new_end <= ending_points[k]:
                                new_end = ending_points[k]
                                for l in range(j, k+1):
                                    starting_points.pop(j)
                                    ending_points.pop(j)
                                starting_points.append(new_start)
                                ending_points.append(new_end)
                                proceed = False
                                break
                    elif new_start <= ending_points[j]:
                        for k in range(j, len(starting_points)):
                            if new_end < starting_points[k]:
                                new_start = starting_points[j]
                                for l in range(j, k+1):
                                    starting_points.pop(j)
                                    ending_points.pop(j)
                                starting_points.append(new_start)
                                ending_points.append(new_end)
                                proceed = False
                                break
                            elif new_end <= ending_points[k]:
                                new_start = starting_points[j]
                                new_end = ending_points[k]
                                for l in range(j, k+1):
                                    starting_points.pop(j)
                                    ending_points.pop(j)
                                starting_points.append(new_start)
                                ending_points.append(new_end)
                                proceed = False
                                break
                        if new_end > ending_points[len(ending_points)-1]:
                            new_start = starting_points[j]
                            for l in range(j, len(ending_points)):
                                starting_points.pop(j)
                                ending_points.pop(j)
                            starting_points.append(new_start)
                            ending_points.append(new_end)

                if new_end < starting_points[len(ending_points) - 1]:
                    starting_points.append(new_start)
                    ending_points.append(new_end)
                else:
                    new_start = min(new_start, starting_points[len(starting_points) - 1])
                    new_end = max(ending_points[len(ending_points) - 1], new_end)
                    starting_points.pop(len(starting_points) - 1)
                    ending_points.pop(len(ending_points) - 1)
                    starting_points.append(new_start)
                    ending_points.append(new_end)
            else:
                starting_points.append(new_start)
                ending_points.append(new_end)
            starting_points.sort()
            ending_points.sort()
        time = 0
        for i in range(0, len(starting_points)):
            time += Statistics.time_from_dates(starting_points[i], ending_points[i])
        return time

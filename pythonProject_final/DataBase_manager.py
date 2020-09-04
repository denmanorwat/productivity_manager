import sqlite3
import random
from ActionClasses.Action import Action
from ActionClasses.Subaction import Subaction


class DataBaseManager:
    def __init__(self):
        self.connection = sqlite3.connect("productivity_manager.sqlite", check_same_thread=False)
        self.__cursor = self.connection.cursor()
        self.__prepare_accounts()
        self.__prepare_online()
        self.__prepare_actions()
        self.__prepare_subactions()

    def register_if_absent(self, username, password, address):
        print(username)
        self.__cursor.execute("""
        SELECT COUNT(*)
        FROM accounts
        WHERE username=(?)
        """, (username, ))
        if self.__cursor.fetchone()[0] == 0:
            self.__cursor.execute("""
            INSERT INTO accounts (username, password)
            VALUES (?, ?)
            """, (username, password))
            key = random.randint(1, 1000000)
            self.__add_key(address, username, key)
            self.connection.commit()
            return key
        else:
            return False

    def check_key(self, username, key):
        self.__cursor.execute("""
        SELECT COUNT(*) 
        FROM online
        WHERE username=? AND key=?
        """, (username, key))
        if self.__cursor.fetchone()[0] == 1:
            print("User " + username + "sent correct key.")
            return True
        else:
            print("User" + username + "sent incorrect key. Sent: " + str(key))
            return False

    def authorise_if_exists(self, username, password, address):
        self.__cursor.execute("""
                SELECT COUNT(*)
                FROM accounts
                WHERE username=? AND password=?
                """, (username, password))
        if self.__cursor.fetchone()[0] == 1:
            key = random.randint(1, 1000000)
            self.__add_key(address, username, key)
            self.connection.commit()
            return key
        else:
            return False

    def __add_key(self, address, username, key):
        self.__cursor.execute("""
        SELECT COUNT(*)
        FROM online
        WHERE username=?
        """, (username, ))
        if self.__cursor.fetchone()[0] == 1:
            self.__delete_key_by_username(username)
        address = self.address_converter(address)
        print(address)
        self.__cursor.execute("""
        INSERT INTO online (address, username, key)
        VALUES (?, ?, ?)
        """, (address, username, key))
        self.connection.commit()

    def __delete_key_by_address(self, address):
        print("delete_key_by_address called")
        address = self.address_converter(address)
        self.__cursor.execute("""
        SELECT COUNT(*)
        FROM online
        WHERE address=?
        """, (address, ))
        print("Found " + str(self.__cursor.fetchone()[0]) + " rows")
        self.__cursor.execute("""
        DELETE 
        FROM online 
        WHERE address=?
        """, (address, ))
        self.connection.commit()

    def __delete_key_by_username(self, username):
        self.__cursor.execute("""
                DELETE FROM online WHERE username=?
                """, (username, ))
        self.connection.commit()

    def log_out(self, username):
        print("Log out called")
        self.__delete_key_by_username(username)

    def add_or_update_actions(self, username, key, actions):
        if self.check_key(username, key):
            print("Number of actions sent:" + str(len(actions)))
            for action in actions:
                if action._id is None:
                    self.__add_action(action, username)
                else:
                    self.__update_action_if_new(action, username)
            return True
        return False

    def add_subaction(self, username, key, action_id, subaction):
        #Not tested yet!
        if self.check_key(username, key):
            self.__cursor.execute("""
            INSERT INTO subactions (username, action_id, description, date_of_start, date_of_finish, type)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (username, action_id, subaction._description,
                  subaction._date_of_start, subaction._date_of_end, subaction._type))
            self.connection.commit()

    def delete_actions(self, username, key, action_ids):
        if self.check_key(username, key) and action_ids is not None:
            for id in action_ids:
                self.__cursor.execute("""
                        DELETE FROM actions
                        WHERE id=? and username=?
                        """, (id, username))
            self.connection.commit()

    def delete_action(self, username, key, action_id):
        if self.check_key(username, key):
            self.__cursor.execute("""
            DELETE FROM actions
            WHERE id=? and username=?
            """, (action_id, username))
            self.connection.commit()

    def __add_action(self, action, username):
        self.__cursor.execute("""
            INSERT INTO actions (name, description, date_of_start, date_of_finish, mark, username)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (action._name, action._description, action._start_date, action._end_date, action._mark, username))
        father_id = self.__cursor.lastrowid
        insert_subactions = list()
        for subaction in action._subactions:
            insert_subactions.append((username, father_id,  subaction._description,
                                     subaction._date_of_start, subaction._date_of_end, subaction._type))
        self.__cursor.executemany("""
        INSERT INTO subactions (username, action_id, description, date_of_start, date_of_finish, type)
        VALUES (?,?,?,?,?,?)
        """, insert_subactions)
        self.connection.commit()

    def __update_action_if_new(self, action, username):
        if action.is_modified():
            update_string = ""
            for key, value in action._modified.items():
                if value:
                    update_string = update_string + " " + key + " = " + action.get_field_by_title(key) + ","
            update_string = update_string[:-1]
            self.__cursor.execute("""
            UPDATE actions
            SET """ + update_string + """
            WHERE id = ? AND username = ?
            """, (action._id, username))
        else:
            print("No actions are modified")

        if len(action._updated_subactions) > 0:
            print("Updates found")
            for subaction_id in action._updated_subactions:
                print(subaction_id)
                subaction = action.get_subaction(subaction_id)
                update_string = ""
                print("Updated subactions are:" + str(action._updated_subactions))
                print("Current subaction is:" + str(subaction_id))
                for key, value in subaction._modified.items():
                    if value:
                        update_string = update_string + " " + key + " = " + \
                                        str(subaction.get_field_by_title(key)) + ","
                update_string = update_string[:-1]
                update_subaction = (subaction._id, action._id, username)
                print(update_subaction)
                print("""
                UPDATE subactions
                SET""" + update_string + """
                WHERE id = ? AND action_id = ? AND username = ?
                """)
                self.__cursor.execute("""
                UPDATE subactions
                SET """ + update_string + """
                WHERE id = ? AND action_id = ? AND username = ?
                """, update_subaction)
        else:
            print("No subactions are modified")

        if len(action._deleted_subactions) > 0:
            print("Found subaction to delete")
            print(action._deleted_subactions)
            self.__cursor.executemany("""
            DELETE 
            FROM subactions
            WHERE id=? AND action_id=?
            """, action.get_tupled_deleted_subactions_with_actions(action._id))
        else:
            print("No actions are deleted")

        self.connection.commit()

    def get_actions(self, username, key):
        checked = self.check_key(username, key)
        if checked:
            self.__cursor.execute("""
            SELECT id, name, description, date_of_start, date_of_finish, mark
            FROM actions
            WHERE username=?
            """, (username, ))
            actions = self.__cursor.fetchall()
            compilated_actions = list()
            for action in actions:
                self.__cursor.execute("""
                SELECT id, description, date_of_start, date_of_finish, type
                FROM subactions
                WHERE action_id=? AND username=?
                """, (action[0], username))
                subactions_of_action = list()
                subactions = self.__cursor.fetchall()
                for subaction in subactions:
                    subaction_of_action = (Subaction(subaction[1], subaction[2], subaction[3]))
                    subaction_of_action._id = subaction[0]
                    subaction_of_action._type = subaction[4]
                    subactions_of_action.append(subaction_of_action)
                compilated_action = Action(action[1], action[2], action[3], action[4], action[5])
                compilated_action._id = action[0]
                compilated_action._attach_subactions(subactions_of_action)
                compilated_actions.append(compilated_action)
            return compilated_actions
        else:
            return False

    def get_actions_in_interval(self, username, key, start_date, end_date):
        checked = self.check_key(username, key)
        if checked:
            self.__cursor.execute("""
                        SELECT id, name, description, date_of_start, date_of_finish, mark
                        FROM actions
                        WHERE username=? AND date_of_start>=? AND date_of_finish<=?
                        """, (username, start_date, end_date))
            actions = self.__cursor.fetchall()
            compilated_actions = list()
            for action in actions:
                self.__cursor.execute("""
                            SELECT id, description, date_of_start, date_of_finish, type
                            FROM subactions
                            WHERE action_id=? AND username=?
                            """, (action[0], username))
                subactions_of_action = list()
                subactions = self.__cursor.fetchall()
                for subaction in subactions:
                    subaction_of_action = (Subaction(subaction[1], subaction[2], subaction[3]))
                    subaction_of_action._id = subaction[0]
                    subaction_of_action._type = subaction[4]
                    subactions_of_action.append(subaction_of_action)
                compilated_action = Action(action[1], action[2], action[3], action[4], action[5])
                compilated_action._id = action[0]
                compilated_action._attach_subactions(subactions_of_action)
                compilated_actions.append(compilated_action)
            return compilated_actions
        else:
            return False

    def get_action(self, username, key, action_id):
        if self.check_key(username, key):
            self.__cursor.execute("""
            SELECT name, description, date_of_start, date_of_finish, mark
            FROM actions
            WHERE id=? AND username=?
            """, (action_id, username))
            action = self.__cursor.fetchone()
            print(action)
            action = Action(action[0], action[1], action[2], action[3], action[4])
            action._id = action_id
            self.__cursor.execute("""
            SELECT id, description, date_of_start, date_of_finish, type
            FROM subactions
            WHERE action_id=?
            """, (action_id, ))
            for row_subaction in self.__cursor.fetchall():
                print(row_subaction)
                action._attach_subaction(Subaction(row_subaction[1], row_subaction[2],
                                                   row_subaction[3], row_subaction[4], row_subaction[0]))
            return action

    def __prepare_accounts(self):
        self.__cursor.execute("""
                SELECT COUNT(*)
                FROM sqlite_master
                WHERE type = 'table' AND name = 'accounts' """)
        if self.__cursor.fetchone()[0] == 0:
            self.__cursor.execute("""
                    CREATE TABLE accounts (
                    username varchar(255) PRIMARY KEY,
                    password varchar(255)
                    ) """)
            self.connection.commit()

    def __prepare_online(self):
        self.__cursor.execute("""
                SELECT COUNT(*)
                FROM sqlite_master
                WHERE type = 'table' AND name = 'online' """)
        if self.__cursor.fetchone()[0] == 0:
            self.__cursor.execute("""
                    CREATE TABLE online (
                    username varchar(255) PRIMARY KEY, 
                    address varchar(255),
                    key int,
                    FOREIGN KEY (username) REFERENCES accounts(username)
                    ) """)
            self.connection.commit()

    def __prepare_actions(self):
        self.__cursor.execute("""
                        SELECT COUNT(*)
                        FROM sqlite_master
                        WHERE type = 'table' AND name = 'actions' """)
        if self.__cursor.fetchone()[0] == 0:
            self.__cursor.execute("""
                            CREATE TABLE actions (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username varchar(255),
                            name varchar(255),
                            description varchar(1000),
                            date_of_start varchar(19),
                            date_of_finish varchar(19),
                            mark int,
                            FOREIGN KEY (username) REFERENCES accounts(username)
                            ) """)
            self.connection.commit()

    def __prepare_subactions(self):
        self.__cursor.execute("""
                        SELECT COUNT(*)
                        FROM sqlite_master
                        WHERE type = 'table' AND name = 'subactions' """)
        if self.__cursor.fetchone()[0] == 0:
            self.__cursor.execute("""
                            CREATE TABLE subactions (
                            username varchar(255),
                            action_id int,
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            description varchar(255),
                            date_of_start varchar(19),
                            date_of_finish varchar(19),
                            type varchar(255),
                            FOREIGN KEY (action_id) REFERENCES actions(id),
                            FOREIGN KEY (username) REFERENCES accounts(username)
                            ) """)
            self.connection.commit()

    @staticmethod
    def address_converter(address):
        return str(address[0])+":"+str(address[1])

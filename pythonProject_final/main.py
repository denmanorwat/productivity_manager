from DataBase_manager import DataBaseManager
from SocketManager import SocketManager

database = DataBaseManager()
socketManager = SocketManager(database)
socketManager.start_acceptance()

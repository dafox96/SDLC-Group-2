import hashlib
import html
from game_library import GameLibrary

class Login:                                #Class which holds list of users, and has methods for accessing and editing users  
    def __init__(self):
        self.users = []
    
    def removeUser(self, username):
        index = self.checkUser(username)
        if index == -1:
            print("No user by that name")
        else:
            self.users.pop(index)
                
    def addUser(self, username, password):    #Creates new user entity in list of users
        index = self.checkUser(username)
        if index == -1:
            self.users.append(User(username, password))
        else:
            print("User already exists")

    def listUsers(self):                    #Prints list of usernames
        for user in self.users:
            print(user.getUsername())

    def checkUser(self, username):          #Function for checking if user exists
        for i in range(0, len(self.users)):
            if self.users[i].getUsername() == username:
                return i
        return -1

    def login(self, username, password):                #Returns user object if login is successful, False and prints an error message otherwise
        index = self.checkUser(username)
        if index == -1:
            print("Login failed, user does not exist")
            return False
        else:
            success = self.users[index].checkPassword(password)
            if success:
                print("Login successful")
                return self.users[index]               #Not sure what to do at success, am just returning the user for now
            else:
                print("Login failed, incorrect password")
                return False

class User:                                 #User class holds username, hashed password, and a GameLibrary
    def __init__(self, username, password):
        self.username = username
        self.password = generateHash(password)
        self.library = GameLibrary()

    def getUsername(self):
        return(self.username)
    
    def checkPassword(self, password):
        hash = generateHash(password)
        if(hash == self.password):
            return True
        else:
            return False


def generateHash(password):  
    sha512 = hashlib.sha512()
    sha512.update(password.encode())
    hash = sha512.hexdigest()
    print(hash)
    return hash

def sanitize(input):                    
    return html.escape(input)


login = Login()

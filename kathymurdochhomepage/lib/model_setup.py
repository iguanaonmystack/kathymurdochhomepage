from sqlobject import connectionForURI, sqlhub

from ..model import Recipe, User

def setup(dburi):
    connection = connectionForURI(dburi)
    sqlhub.processConnection = connection
    # The sqlhub.processConnection assignment means that all classes will,
    # by default, use this connection

    Recipe.createTable(ifNotExists=True)
    User.createTable(ifNotExists=True)
    
    return connection


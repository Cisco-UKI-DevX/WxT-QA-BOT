import os
import sys
import mysql.connector

# Connect to MySQL database
def connectToDB():
    try:
        db = mysql.connector.connect(
            user=os.environ['DB_user'],
            host=os.environ['DB_host'],
            port=os.environ['DB_port'],
            password=os.environ['DB_password'],
            database=os.environ['DB_database']
        )
        # Instantiate cursor
        cursor = db.cursor()
        print("Sucessfully connected to DB")
        return cursor, db
        
    except:
        print("Failed to connect to DB. MySQL Connection not available.")

# Close cursor and connection to DB
def closeConnectionToDB(db, cursor):
    try:
        db.commit()
        cursor.close()
        db.close()
    except:
        print("Failed to close connection to DB")

# Add a user and the hashed Password to the DB
def addUser(user, hashedPassword, role):
    try:
        cursor, db = connectToDB()
        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (user, hashedPassword, role))
        cursor.execute("SELECT id FROM users WHERE username=%s", (user,))
        userID = cursor.fetchall()[0][0]
        closeConnectionToDB(db, cursor)
        print("Successfully added user to the database")
        return userID, user
    except:
        print("Error adding user into the database")
        return("Failure")

def getUser(user):
    try:
        cursor, db = connectToDB()
        cursor.execute("SELECT username FROM users WHERE username=%s", (user,))
        result = cursor.fetchall()
        if not result:
            err_userNotFound = True
            closeConnectionToDB(db, cursor)
            raise(err_user)
        
        user = result[0][0]
        closeConnectionToDB(db, cursor)
        return(user)
    
    except:
        if "err_userNotFound" in locals():
            print("Error! Username: "+str(user)+" does not exist.")
            return None
        else:
            print("Error getting Username:"+str(user)+" from the database.")
            return("Failure")

def getUserbyID(id):
    try:
        cursor, db = connectToDB()
        cursor.execute("SELECT username FROM users WHERE id=%s", (id,))
        result = cursor.fetchall()
        if not result:
            err_userNotFound = True
            closeConnectionToDB(db, cursor)
            raise(err_user)
        
        user = result[0][0]
        closeConnectionToDB(db, cursor)
        return(user)
    
    except:
        if "err_userNotFound" in locals():
            print("Error! User ID: "+str(id)+" does not exist.")
            return None
        else:
            print("Error getting username with ID: "+str(id)+" from the database.")
            return("Failure")

def getPasswordHash(user):
    try:
        cursor, db = connectToDB()
        cursor.execute("SELECT password FROM users WHERE username=%s", (user,))
        result = cursor.fetchall()
        if not result:
            err_userNotFound = True
            closeConnectionToDB(db, cursor)
            raise(err_user)
        
        passwordHash = result[0][0]
        closeConnectionToDB(db, cursor)
        return(passwordHash)
    
    except:
        if "err_userNotFound" in locals():
            print("Error! Failed to get hashed password as username: "+str(user)+" does not exist.")
            return None
        else:
            print("Error getting hashed password from Username: "+str(id)+" from the database.")
            return("Failure")

def getRole(user):
    try:
        cursor, db = connectToDB()
        cursor.execute("SELECT role FROM users WHERE username=%s", (user,))
        result = cursor.fetchall()
        if not result:
            err_userNotFound = True
            closeConnectionToDB(db, cursor)
            raise(err_user)
        
        role = result[0][0]
        closeConnectionToDB(db, cursor)
        return role
    
    except:
        if "err_userNotFound" in locals():
            print("Error! Username: "+str(user)+" does not exist.")
            return None
        else:
            print("Error getting role from Username: "+str(user))
            return("Failure")
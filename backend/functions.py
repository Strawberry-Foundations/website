import sqlite3 as sql
import argon2

def hash_password(password):
    ph = argon2.PasswordHasher()
    hashed_password = ph.hash(password)
    
    return hashed_password

def verify_password(stored_password, entered_password):
    ph = argon2.PasswordHasher()
    
    try:
        ph.verify(stored_password, entered_password)
        return True
    
    except argon2.exceptions.VerifyMismatchError:
        return False
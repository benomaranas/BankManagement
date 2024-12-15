import mysql.connector
from typing import Dict, Optional
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="bank_db"
    )
    
    
def get_all_accounts():
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM bank_accounts ORDER BY balance DESC")
    accounts = cursor.fetchall()
    db.close()
    return accounts
def create_account(account_number, account_holder, balance=0.0):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO bank_accounts (account_number, account_holder, balance) VALUES (%s, %s, %s)",
        (account_number, account_holder, balance)
    )
    db.commit()
    db.close()
def get_account(account_number):
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM bank_accounts WHERE account_number = %s", (account_number,))
    account = cursor.fetchone()
    db.close()
    return account
def delete_account(account_number):
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("DELETE FROM bank_accounts WHERE account_number = %s", (account_number,))
    db.commit()
    db.close()
""" def deposit(account_number, amount):
    db = connect_db()
    
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT balance FROM bank_accounts WHERE account_number = %s", (account_number,))
    account: Dict[str,str,str, float] = cursor.fetchone()
    
    
    if not account:
        db.close()
        raise ValueError("Le compte n'existe pas")
    
    
    new_balance=account['balance'] + amount  """
if __name__ == "__main__":
    print(get_all_accounts())
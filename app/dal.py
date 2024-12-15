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
def deposit_to_account(account_number, amount):
    db = connect_db()
    
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT balance FROM bank_accounts WHERE account_number = %s", (account_number,))
    account = cursor.fetchone()
    
    
    if not account:
        db.close()
        raise ValueError("Le compte n'existe pas")
    
    
    new_balance=account["balance"] + amount
    cursor.execute("UPDATE bank_accounts SET balance = %s WHERE account_number = %s", (new_balance, account_number))
    db.commit()
    
    
    cursor.execute(
        "INSERT INTO transactions (account_number, operation_type, amount) VALUES ((SELECT id FROM bank_accounts WHERE account_number = %s), 'Deposit', %s)", (account_number, amount))
    db.commit()
    db.close()
def withdraw_from_account(account_number:str, amount:float):
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("SELECT balance FROM bank_accounts WHERE account_number = %s", (account_number,))
    account = cursor.fetchone()
    if not account:
        db.close()
        raise ValueError("Le compte n'existe pas")
    
    if amount > account["balance"]:
        db.close()
        raise ValueError("Fonds insuffisants pour effectuer le retrait")
    new_balance = account["balance"] - amount
    cursor.execute("UPDATE bank_accounts SET balance = %s WHERE account_number = %s", (new_balance, account_number))
    db.commit()
    
    cursor.execute(
        "INSERT INTO transactions (account_id, operation_type, amount) VALUES ((SELECT id FROM bank_accounts WHERE account_number = %s), 'Withdrawal', %s)", (account_number, amount))
    db.commit()
    db.close()
def transfer_between_accounts(from_account_number:str, to_account_number:str, amount:float):
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("SELECT balance FROM bank_accounts WHERE account_number = %s", (from_account_number,))
    from_account = cursor.fetchone()
    if not from_account:
        db.close()
        raise ValueError("Le compte source n'existe pas")
    cursor.execute("SELECT balance FROM bank_accounts WHERE account_number = %s", (to_account_number,))
    to_account = cursor.fetchone()
    if not to_account:
        db.close()
        raise ValueError("Le compte de destination n'existe pas")
    if amount > from_account["balance"]:
        db.close()
        raise ValueError("Fonds insuffisants pour effectuer le transfert")
    
    
    new_balance_from = from_account["balance"] - amount
    new_balance_to = to_account["balance"] + amount
    
    
    cursor.execute("UPDATE bank_accounts SET balance = %s WHERE account_number = %s", (new_balance_from, from_account_number))
    db.commit()
    cursor.execute("UPDATE bank_accounts SET balance = %s WHERE account_number = %s", (new_balance_to, to_account_number))
    db.commit()
    
    cursor.execute(
        "INSERT INTO transactions (account_id, operation_type, amount) VALUES ((SELECT id FROM bank_accounts WHERE account_number = %s),'Transfer IN '%s)",(from_account_number, amount))
    db.commit()
    cursor.execute(
        "INSERT INTO transactions (account_id, operation_type, amount) VALUES ((SELECT id FROM bank_accounts WHERE account_number = %s),'Transfer OUT '%s)",(to_account_number, amount))
    db.commit()
    db.close()
def get_transactions(account_number:str):
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT t.operation_type, t.amount, t.created_at
        FROM transactions t
        JOIN bank_accounts b ON t.account_id = b.id
        WHERE b.account_number = %s
        ORDER BY t.created_at DESC
    """, (account_number,))
    transactions = cursor.fetchall()
    db.close()
    return transactions
if __name__ == "__main__":
    print(get_all_accounts())
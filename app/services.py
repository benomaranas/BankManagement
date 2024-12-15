from app.dal import create_account, get_all_accounts, get_account,delete_account, deposit_to_account, withdraw_from_account,transfer_between_accounts, get_transactions



def create_new_account(account_number, account_holder, balance):
    """
    Creates a new account by validating input and delegating to the DAL layer.
    """
    if balance < 0:
        raise ValueError("Le solde initial ne peut pas être négatif.")
    create_account(account_number, account_holder, balance)

def fetch_all_accounts():
    """
    Fetches all accounts from the database using the DAL layer.
    """
    return get_all_accounts()
def search_account(account_number):
    account = get_account(account_number)
    if not account : 
        raise ValueError("Compte non trouvé")
    return account
def remove_account(account_number):
    account = get_account(account_number)
    if not account :
        raise ValueError("Compte non trouvé")
    delete_account(account_number)
    
def deposit(account_number:str, amount:float):
    
    
    
    if amount <= 0:
        raise ValueError("Le montant doit être positif.")
    deposit_to_account(account_number, amount)
    # Delegate deposit logic to the DAL layer (implement DAL deposit method as needed).
    # Example: update_account_balance(account_id, amount) 
def withdraw(account_number:str, amount:float):
    if amount <= 0:
        raise ValueError("Le montant doit être positif.")
    withdraw_from_account(account_number,amount)

def transfer(from_account_number:str, to_account_number:str, amount:float):
    if amount <= 0:
        raise ValueError("Le montant doit être positif.")
    transfer_between_accounts(from_account_number, to_account_number, amount)
def get_account_transactions(account_number:str):
    
    return get_transactions(account_number)
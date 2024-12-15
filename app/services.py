from app.dal import create_account, get_all_accounts, get_account,delete_account



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
    
""" def deposit(account_id, amount):
    
    
    
    if amount <= 0:
        raise ValueError("Le montant doit être positif.")
    # Delegate deposit logic to the DAL layer (implement DAL deposit method as needed).
    # Example: update_account_balance(account_id, amount) """

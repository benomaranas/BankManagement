class BankAccount:
    def __init__(self, account_number, account_holder, balance=0.0) -> None:
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = balance
        
class Transaction:
    def __init__(self, account_id, operation_type, amount):
        self.account_id = account_id
        self.operation_type = operation_type
        self.amount = amount
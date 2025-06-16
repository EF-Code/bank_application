class BankAccount:
    def __init__(self, account_number, holder_name, balance=0):
        self.account_number = account_number
        self.holder_name = holder_name
        self.balance = balance
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return f"Deposited {amount}. New balance: {self.balance}"
        return "Invalid deposit amount."

    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            return f"Withdrew {amount}. New balance: {self.balance}"
        return "Insufficient balance or invalid amount."

class SavingsAccount(BankAccount):
    def __init__(self, account_number, holder_name, balance=0, withdrawal_limit=100000):
        super().__init__(account_number, holder_name, balance)
        self.withdrawal_limit = withdrawal_limit

    def withdraw(self, amount):
        if amount > self.withdrawal_limit:
            return f"Cannot withdraw more than {self.withdrawal_limit} at a time."
        return super().withdraw(amount)


class CurrentAccount(BankAccount):
    pass

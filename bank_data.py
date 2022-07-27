import csv


class Account:
    def __init__(self, data_dict):
        self.data = data_dict
        self.is_validated_pin = False

    def validate_pin_number(self, pin_number):
        if self.data['pin_number'] == str(pin_number):
            self.is_validated_pin = True
            return True
        return False

    def check_pin_validate(self):
        if not self.is_validated_pin:
            raise LookupError('\n![ERROR]not validated')

    def get_balance(self):
        return self.data['balance']

    def deposit(self, amount):
        updated_balance = int(self.data['balance']) + int(amount)
        self.data['balance'] = str(updated_balance)

    def withdraw(self, amount):
        self.check_pin_validate()
        updated_balance = int(self.data['balance']) - int(amount)
        if updated_balance < 0:
            raise ValueError('\n![ERROR]balance is insufficient.')
        self.data['balance'] = str(updated_balance)


class Database:
    def __init__(self):
        self.fields = ['card_number', 'pin_number', 'name', 'balance']
        f = open('database.csv')
        self.data_dict = dict()
        for data in list(csv.DictReader(f)):
            self.data_dict[data['card_number']] = data
        f.close()

    def select_account_by_card_number(self, card_number):
        account = self.data_dict.get(card_number, None)
        if account:
            return Account(account)
        raise ValueError('\n![ERROR]Invalid Card')

    def is_card_number_exist(self, card_number):
        account = self.data_dict.get(card_number)
        if account:
            return True
        return False

    def create_account(self, card_number, pin_number, name):
        if self.is_card_number_exist(card_number):
            raise ValueError('\n[ERROR]card number already exist')
        self.data_dict[card_number] = {
            'card_number': card_number, 'name': name, 'balance': 0, 'pin_number': pin_number
        }
        account = Account(self.data_dict[card_number])
        self.commit(account)
        return account

    def commit(self, account):
        f = open('database.csv', 'w+')
        f.truncate()

        data = account.data
        self.data_dict[data['card_number']] = data

        writer = csv.DictWriter(f, fieldnames=self.fields)
        writer.writeheader()
        for _, value in self.data_dict.items():
            writer.writerow(value)
        f.close()


database = Database()

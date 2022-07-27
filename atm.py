import click
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
            raise LookupError('not validated')

    def get_balance(self):
        return self.data['balance']

    def deposit(self, amount):
        updated_balance = int(self.data['balance']) + int(amount)
        self.data['balance'] = str(updated_balance)

    def withdraw(self, amount):
        self.check_pin_validate()
        updated_balance = int(self.data['balance']) - int(amount)
        if updated_balance < 0:
            raise ValueError('balance is insufficient.')
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
        raise ValueError('Invalid Card')

    def commit(self, account):
        f = open('database.csv', 'w+')
        f.truncate()

        data = account.data
        self.data_dict[data['card_number']] = data

        writer = csv.DictWriter(f, fieldnames=self.fields)
        writer.writeheader()
        for _, value in self.data_dict.items():
            writer.writerow(value)


@click.group
def cli():
    pass


@click.command()
@click.argument('card_number')
def insert_card(card_number):
    """Insert Credit Card"""
    account = database.select_account_by_card_number(card_number)

    pin_number = input('PLEASE INSERT YOUR PIN NUMBER')
    is_valid = account.validate_pin_number(pin_number)
    if not is_valid:
        click.echo('INVALID PIN NUMBER')
        return

    while True:
        click.echo(f'BALANCE: {account.data["balance"]} \n')
        click.echo(f'SELECT YOUR TASK')
        click.echo(f'1) Deposit 2) Withdraw 3) Exit')

        task = str(input())
        if task == '1' or task == '2':
            task_dict = {'1': account.deposit, '2': account.withdraw}
            amount = input('ENTER THE AMOUNT\n')
            task_dict[task](amount)
            database.commit(account)
        else:
            click.echo('GOOD BYE')
            return


cli.add_command(insert_card)

if __name__ == '__main__':
    database = Database()
    cli()

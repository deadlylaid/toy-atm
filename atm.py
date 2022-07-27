import click
from bank_data import database


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

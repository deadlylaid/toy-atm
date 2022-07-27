import click
import random

from bank_data import database


@click.group
def cli():
    pass


class BankFront:
    @staticmethod
    @click.command()
    def create_card():
        """Create New Credit Card"""
        name = input('INSERT YOUR NAME')
        pin_number = input('INSERT YOUR PIN NUMBER')

        while True:
            try:
                card_number = '-'.join([str(x) for x in random.sample(range(1000, 9999), 4)])
                account = database.create_account(card_number, pin_number, name)
                click.echo('\n')
                click.echo(f'card_number: {account.data["card_number"]}')
                click.echo('\n')
                break
            except ValueError:
                pass


cli.add_command(BankFront.create_card)

if __name__ == '__main__':
    cli()

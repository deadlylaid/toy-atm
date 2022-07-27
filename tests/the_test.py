import unittest

import atm


class TestATM(unittest.TestCase):
    def test_create_database_object(self):
        database = atm.Database()
        data_dict = {
            '5389-2000-5651-9669': {
                'card_number': '5389-2000-5651-9669', 'pin_number': '1234', 'name': '사람1', 'balance': '1000000'
            },
            '1234-1444-4951-8143': {
                'card_number': '1234-1444-4951-8143', 'pin_number': '2222', 'name': '사람2', 'balance': '1405000'
            }
        }

        self.assertEqual(database.data_dict, data_dict)

    def test_database_select_account_by_card_number(self):
        database = atm.Database()
        inserted_card = '5389-2000-5651-9669'
        account = database.select_account_by_card_number(inserted_card)
        self.assertEqual(
            account.data,
            {'balance': '1000000', 'card_number': '5389-2000-5651-9669', 'name': '사람1', 'pin_number': '1234'}
        )

        inserted_invalid_cared = '1'
        self.assertRaises(ValueError, database.select_account_by_card_number, inserted_invalid_cared)

    def test_validate_pin_number(self):
        database = atm.Database()
        inserted_card = '5389-2000-5651-9669'
        account = database.select_account_by_card_number(inserted_card)

        pin_number = 1234
        is_valid = account.validate_pin_number(pin_number)
        self.assertEqual(is_valid, True)

        invalid_pin_number = 3333
        is_valid = account.validate_pin_number(invalid_pin_number)
        self.assertEqual(is_valid, False)

    def test_deposit(self):
        database = atm.Database()
        inserted_card = '5389-2000-5651-9669'
        account = database.select_account_by_card_number(inserted_card)

        account.deposit('10')
        self.assertEqual(account.get_balance(), '1000010')

    def test_withdraw(self):
        database = atm.Database()
        inserted_card = '5389-2000-5651-9669'
        account = database.select_account_by_card_number(inserted_card)

        pin_number = 1234
        account.validate_pin_number(pin_number)

        account.withdraw('10')
        self.assertEqual(account.get_balance(), '999990')


if __name__ == '__main__':
    unittest.main()

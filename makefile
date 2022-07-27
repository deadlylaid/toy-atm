tests:
	python -m unittest tests/test_logic.py

create-card:
	python bank.py create-card

insert-card:
	python atm.py insert-card $(number)
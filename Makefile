install:
	pip install poetry && \
	poetry install

start:
	poetry run python Telegram-Bot/Bot.py
rebuild:
		docker-compose down -v
		docker-compose up -d

runserver:
		docker-compose up -d
		./venv/bin/python server.py

tests:
		./venv/bin/python -m pytest

build: create_venv install_dependencies up_db

flush_db:
	docker-compose down -v
	docker-compose up -d

up_db:
	docker-compose up -d

create_venv:
	python3 -m venv venv

install_dependencies:
	./venv/bin/pip install -r requirements.txt

runserver:
	docker-compose up -d
	./venv/bin/python server.py

generate_devices:
	./venv/bin/python data_comparator.py run

run_tests:
	./venv/bin/python -m pytest

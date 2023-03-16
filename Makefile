make run:
	python manage.py runserver --settings=core.settings_dev

make admin:
	python manage.py createsuperuser

make migrate:
	python manage.py makemigrations
	python manage.py migrate

make static:
	python manage.py collectstatic

make test:
	python manage.py test

make shell:
	python manage.py shell

make docker-down:
	docker-compose down 
	docker system prune -a 
	docker volume prune

make up:
	docker-compose up

make down:
	docker-compose down

make docker-admin:
	docker-compose exec main_api python manage.py createsuperuser


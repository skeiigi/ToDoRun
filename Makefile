up:
	docker-compose up -d --build

down:
	docker-compose down

restart: down up

logs:
	docker-compose logs -f

migrate:
	docker-compose exec web python manage.py migrate

createsuperuser:
	docker-compose exec web python manage.py createsuperuser

test:
	docker-compose exec web python manage.py test

clean:
	docker-compose down -v
	docker system prune -a -f

update-changelog:
    cz changelog --incremental
    git add CHANGELOG.md

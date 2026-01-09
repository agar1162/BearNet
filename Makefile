.PHONY: start stop restart logs rebuild rebuild-clean rebuild-backend rebuild-frontend

start:
	docker compose up --build -d
	sleep 2
	open http://localhost:5173
	open http://localhost:8000/docs

stop:
	docker compose down

restart: stop start

logs:
	docker compose logs -f

rebuild:
	docker compose down
	docker compose build
	docker compose up -d

rebuild-clean:
	docker compose down -v --remove-orphans
	docker compose build --no-cache
	docker compose up -d

rebuild-backend:
	docker compose build backend
	docker compose up -d backend

rebuild-frontend:
	docker compose build frontend
	docker compose up -d frontend
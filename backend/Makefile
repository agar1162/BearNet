# ---------- Config ----------
ALEMBIC = alembic

# ---------- Alembic ----------
.PHONY: migrate revision upgrade downgrade current history

# Create a new migration from model changes
# Usage: make revision m="add email to user"
revision:
	$(ALEMBIC) revision --autogenerate -m "$(m)"

# Apply all pending migrations
upgrade:
	$(ALEMBIC) upgrade head

# Roll back one migration
downgrade:
	$(ALEMBIC) downgrade -1

# Show current migration version
current:
	$(ALEMBIC) current

# Show migration history
history:
	$(ALEMBIC) history

# ---------- Dev helpers ----------
.PHONY: reset-db

# ⚠️ DANGEROUS: wipes DB volume (dev only)
reset-db:
	docker compose down -v
	docker compose up -d
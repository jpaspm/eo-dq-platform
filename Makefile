.PHONY: test coverage validate runtime lint clean help

# --------------------------------------------------
# Run Unit Tests
# --------------------------------------------------

test:
	pytest -v

# --------------------------------------------------
# Run Unit Tests with Coverage
# --------------------------------------------------

coverage:
	pytest --cov=. --cov-report=term-missing

# --------------------------------------------------
# Validate Enterprise DQ Catalogue
# --------------------------------------------------

validate:
	python eo-dq-engine/catalogue/validate_catalogue.py \
		--catalogue eo-dq-engine/catalogue/Enterprise_DQ_Rules.xlsx

# --------------------------------------------------
# Generate Runtime Configuration
# --------------------------------------------------

runtime:
	python eo-dq-engine/catalogue/generate_runtime.py \
		--catalogue eo-dq-engine/catalogue/Enterprise_DQ_Rules.xlsx \
		--output eo-dq-engine/config

# --------------------------------------------------
# Lint
# --------------------------------------------------

lint:
	ruff check .

# --------------------------------------------------
# Clean
# --------------------------------------------------

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

# --------------------------------------------------
# Help
# --------------------------------------------------

help:
	@echo "Available targets:"
	@echo "  make test       - Run unit tests"
	@echo "  make coverage   - Run tests with coverage"
	@echo "  make validate   - Validate Enterprise DQ rule catalogue"
	@echo "  make runtime    - Generate runtime YAML/JSON from catalogue"
	@echo "  make lint       - Run Ruff linter"
	@echo "  make clean      - Remove cache files"

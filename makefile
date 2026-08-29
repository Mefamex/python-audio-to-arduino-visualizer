.DEFAULT_GOAL := help
.PHONY: install run format clean tree help

help: ## Show this help message
	@echo "Usage: make [command]"
	@echo ""
	@echo "Available commands:"
	@LC_ALL=C grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

install: ## Creates the virtual environment and installs dependencies automatically
	uv sync

run: ## Executes the program safely using uv's environment awareness
	uv run sound-to-usb-serial

format: ## Auto-formats your Python files using the industry-standard ruff formatter
	@echo ""
	@echo "FORMATTING PYTHON FILES..."
	@echo ""
	uvx ruff check --fix src/
	uvx ruff format src/
	rm -rf ./.ruff_cache

clean: ## Removes cached files to reset the environment
	@echo ""
	@echo "CLEANING UP THE ENVIRONMENT..."
	@echo ""
	rm -rf .venv
	find . -type d -name "__pycache__" -exec rm -rf {} +

tree: ## Generates a clean directory tree structure text file
	@echo ""
	@echo "GENERATING DIRECTORY TREE STRUCTURE..."
	@echo ""
	@echo "Project Structure:" > tree.txt
	@echo "" >> tree.txt
	@echo "PYTHON AUDIO TO ARDUINO VISUALIZER" >> tree.txt
	@tree -I '.venv|__pycache__|.git|*.egg-info' >> tree.txt
	@echo "" >> tree.txt
	@echo "Generated on $$(date)" >> tree.txt
	@echo "" >> tree.txt
	@cat tree.txt

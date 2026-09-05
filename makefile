.DEFAULT_GOAL := help
.PHONY: install lint format build run clean tree help

help: ## Show this help message
	@echo "Usage: make [command]"
	@echo ""
	@echo "Available commands:"
	@LC_ALL=C grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

install: ## Creates the virtual environment and installs dependencies automatically
	uv sync

lint: ## Lints the Python source files with ruff
	uvx ruff check src/

run: ## Executes the program safely using uv's environment awareness
	uv run python-audio-to-arduino-visualizer

format: ## Auto-formats your Python files using the industry-standard ruff formatter
	@echo ""
	@echo "FORMATTING PYTHON FILES..."
	@echo ""
	uvx ruff check --fix src/
	uvx ruff format src/

build: ## Builds the package into dist/ with uv build
	@echo ""
	@echo "BUILDING PACKAGE..."
	@echo ""
	uv build

clean: ## Removes cached files to reset the environment
	@echo ""
	@echo "CLEANING UP THE ENVIRONMENT..."
	@echo ""
	rm -rf .venv dist build .ruff_cache
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

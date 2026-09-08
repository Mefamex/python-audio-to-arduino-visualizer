.DEFAULT_GOAL := help
.PHONY: install build run clean tree help

help: ## Show this help message
	@echo "Usage: make [command]"
	@echo ""
	@echo "Available commands:"
	@LC_ALL=C grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

install: ## Creates the virtual environment and installs dependencies automatically
	uv sync

run: ## Executes the program safely using uv's environment awareness
	uv run python-audio-to-arduino-visualizer

build: ## Builds the package into dist/ with uv build
	@echo ""
	@echo "BUILDING PACKAGE..."
	@echo ""
	uv build

clean: ## Removes cached files to reset the environment
	@echo ""
	@echo "CLEANING UP THE ENVIRONMENT..."
	@echo ""
	rm -rf dist build
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
	@echo "Generated on $$(date '+%Y-%m-%d %H:%M:%S')" >> tree.txt
	@echo "" >> tree.txt
	@cat tree.txt

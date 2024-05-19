# Binary name
BINARY_NAME=search-recommendation-magang-merdeka.exe

# Parameter
TAILWINDCMD=tailwindcss
CSSBUILD=$(TAILWINDCMD) -i
PYTHONCMD=python

.PHONY: install_deps build run

all: install_deps build

install_deps:
    # Install Python dependencies
    pip install -r requirements.txt

build: install_deps
    # Compile Tailwind CSS
    $(CSSBUILD) ./static/src/main.css -o ./static/dist/main.css --minify

run: build
    # Run the Python application
    $(PYTHONCMD) app.py

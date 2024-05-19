# Binary name
BINARY_NAME=search-recommendation-magang-merdeka.exe

# Parameter
TAILWINDCMD=tailwindcss
CSSBUILD=$(TAILWINDCMD) -i
PYTHONCMD=python

.PHONY: build run

all: build

build:
	# Compile Tailwind CSS
	$(CSSBUILD) ./static/src/main.css -o ./static/dist/main.css --minify

run: build
	# Run the Python application
	$(PYTHONCMD) app.py

all: build deploy

build:
    docker build -t sentanalysis .

deploy:
	docker run -d -p 8501:8501 sentanalysis
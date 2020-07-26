.PHONY: build sh fmt check

build:
	docker build -f Dockerfile -t python/jocus:dev .

sh:
	docker run --rm -it --mount type=bind,source="$(shell pwd)",target=/app python/jocus:dev bash

fmt:
	docker run --rm -it --mount type=bind,source="$(shell pwd)",target=/app python/jocus:dev black .
	docker run --rm -it --mount type=bind,source="$(shell pwd)",target=/app python/jocus:dev isort .

check:
	docker run --rm -it --mount type=bind,source="$(shell pwd)",target=/app python/jocus:dev mypy

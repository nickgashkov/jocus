.PHONY: build sh fmt check

build:
	docker build -f Dockerfile -t python/strip:dev .

sh:
	docker run --rm -it --mount type=bind,source="$(shell pwd)",target=/app python/strip:dev bash

fmt:
	docker run --rm -it --mount type=bind,source="$(shell pwd)",target=/app python/strip:dev black
	docker run --rm -it --mount type=bind,source="$(shell pwd)",target=/app python/strip:dev isort .

check:
	docker run --rm -it --mount type=bind,source="$(shell pwd)",target=/app python/strip:dev mypy

SHELL := /bin/sh

-include .env
-include .env.local
export

.DEFAULT_GOAL := help

.PHONY: help build publish publish-no-build generate clean verify-publish-env

help:
	@printf '%s\n' \
		'make build            Build source and wheel distributions with uv.' \
		'make publish          Build and publish to PyPI using UV_PUBLISH_TOKEN.' \
		'make publish-no-build Publish existing dist artifacts to PyPI.' \
		'make generate         Regenerate the low-level client from OpenAPI.' \
		'make clean            Remove local build artifacts.'

build:
	uv build

publish: verify-publish-env build
	uv publish

publish-no-build: verify-publish-env
	uv publish

generate:
	./scripts/generate.sh

clean:
	./scripts/clean.sh

verify-publish-env:
	@if [ -z "$(UV_PUBLISH_TOKEN)" ]; then \
		echo 'UV_PUBLISH_TOKEN is not set. Copy .env.example to .env and add your PyPI token.'; \
		exit 1; \
	fi

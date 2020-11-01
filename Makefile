# Makefile

include .lily/lily_assistant.makefile

deploy_to_pypi:
	rm -rf dist && \
	python setup.py sdist && \
	twine upload dist/*

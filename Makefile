.PHONY: clean-pyc clean-build docs

help:
	@echo "build27 - build Python 2.7 virtualenv"
	@echo "build33 - build Python 3.3 virtualenv"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "testall - run tests on every Python version with tox"
	@echo "release - package and upload a release"
	@echo "sdist - package"

build27:
	virtualenv -p python2.7 env
	env/bin/pip install --use-mirrors -r requirements.txt

build33:
	virtualenv -p python3.3 env
	env/bin/pip install --use-mirrors -r requirements.txt

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lint:
	flake8 unshortenit tests

test:
	python setup.py test

test-all:
	tox

release: clean
	python setup.py sdist upload

sdist: clean
	python setup.py sdist
	ls -l dist

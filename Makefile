.PHONY: clean-pyc clean-build docs

help:
	@echo "build27 - build Python 2.7 virtualenv"
	@echo "build33 - build Python 3.3 virtualenv"
	@echo "build-pyv8-py33 - build PyV8 package for Python 3.3"
	@echo "build-pyv8-py27 - build PyV8 package for Python 2.7"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "testall - run tests on every Python version with tox"
	@echo "release - package and upload a release"
	@echo "sdist - package"
	@echo "setup - internal used by setup.py install"

build27:
	virtualenv -p python2.7 env
	env/bin/pip install --use-mirrors -r requirements.txt
	make build-pyv8-py27
	cd build/pyv8-read-only && V8_HOME=$(CURDIR)/build/v8 env/bin/python setup.py install && cd ../../

build33:
	virtualenv -p python3.3 env
	env/bin/pip install --use-mirrors -r requirements.txt
	make build-pyv8-py33
	cd build/pyv8-read-only && V8_HOME=$(CURDIR)/build/v8 env/bin/python setup.py install && cd ../../

build-pyv8-py33:
	sudo apt-get install gyp subversion build-essential libboost-python-dev python3.3-dev libboost-system-dev libboost-thread-dev
	mkdir -p build
	svn checkout http://v8.googlecode.com/svn/trunk/ build/v8
	svn checkout http://pyv8.googlecode.com/svn/trunk/ build/pyv8-read-only
	$(MAKE) -C build/v8 dependencies
	sed -i.bak s/\'boost\_python\'/\'boost_python-py33\'/ build/pyv8-read-only/setup.py
	cd build/pyv8-read-only && V8_HOME=$(CURDIR)/build/v8 python3.3 setup.py build && cd ../../

build-pyv8-py27:
	sudo apt-get install gyp subversion build-essential libboost-python-dev python2.7-dev libboost-system-dev libboost-thread-dev
	mkdir -p build
	svn checkout http://v8.googlecode.com/svn/trunk/ build/v8
	svn checkout http://pyv8.googlecode.com/svn/trunk/ build/pyv8-read-only
	$(MAKE) -C build/v8 dependencies
	cd build/pyv8-read-only && V8_HOME=$(CURDIR)/build/v8 python3.3 setup.py build && cd ../../

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

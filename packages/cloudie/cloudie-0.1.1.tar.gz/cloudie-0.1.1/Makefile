.PHONY: all dist install install-dev test qa

all:

install:
	pip3 install -r requirements/requirements.txt --no-binary :all:
	./setup.py install

install-dev:
	pip3 install -r requirements/requirements.txt --no-binary :all:
	pip3 install -r requirements/requirements-dev-1.txt --no-binary :all:
	pip3 install -r requirements/requirements-dev-2.txt --no-binary :all:
	pip3 install -r requirements/requirements-dev-3.txt --no-binary :all:
	./setup.py develop

test:
	python3 -m unittest -q

qa:
	coverage run -m unittest -q
	coverage report -m
	isort --check-only --diff --recursive .
	mypy .
	pycodestyle .
	pyflakes .
	pylint --output-format parseable setup.py cloudie tests
	yapf --diff --recursive .

dist:
	rm -rf dist tmp
	git checkout-index --all --prefix="tmp/"

	cd tmp && \
	./setup.py sdist && \
	fname=$$(ls dist/*.tar.gz) && \
	gpg --detach-sign --armor --output $${fname}.asc $$fname

	mv tmp/dist .
	rm -rf tmp

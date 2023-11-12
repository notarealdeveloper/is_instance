PKG := is_instance

build:
	python -m build

install:
	@# note: this doesn't resolve dependencies
	@# pip install dist/*.tar.gz
	@# this does
	pip install .

develop:
	pip install -e .

check:
	pytest tests/

uninstall:
	pip uninstall $(PKG)

clean:
	rm -rfv dist build/ src/*.egg-info

push-test:
	python -m twine upload --repository testpypi dist/*

pull-test:
	pip install -i https://test.pypi.org/simple/ $(PKG)

push-prod:
	python -m twine upload dist/*

pull-prod:
	pip install $(PKG)


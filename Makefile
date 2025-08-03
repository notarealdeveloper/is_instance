PKG := is_instance

build:
	pip install build
	python -m build

install: clean build
	pip install dist/*.tar.gz

uninstall:
	pip uninstall $(PKG)

develop:
	pip install -e .[develop]

check:
	pip install pytest
	pytest -v tests/

clean:
	rm -rfv dist/ build/ src/*.egg-info

push-test:
	pip install twine
	python -m twine upload --repository testpypi dist/*

pull-test:
	pip install -i https://test.pypi.org/simple/ $(PKG)

push-prod:
	pip install twine
	python -m twine upload dist/*

pull-prod:
	pip install $(PKG)

PKG := is_instance

build:
	pip install build
	python -m build

install:
	pip install dist/*.tar.gz

uninstall:
	pip uninstall $(PKG)

develop:
	pip install -e .[develop]

check:
	pytest -v tests/

clean:
	rm -rfv dist/ build/ src/*.egg-info

push-test:
	python -m twine upload --repository testpypi dist/*

pull-test:
	pip install -i https://test.pypi.org/simple/ $(PKG)

push-prod:
	python -m twine upload dist/*

pull-prod:
	pip install $(PKG)

PKG := is_instance

# user targets
install:
	pip install .

uninstall:
	pip uninstall $(PKG)

# contributor targets
develop:
	pip install -e .[develop]

check:
	pytest -v tests/

# maintainer targets
build:
	pip install build
	python -m build

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

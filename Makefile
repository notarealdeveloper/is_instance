PKG := is_instance

build:
	python -m build

install:
	pip install .

develop:
	pip install -e .

check:
	@python -c "__import__('is_instance').__test__()"

upload:
	python -m twine upload --repository testpypi dist/*

download:
	pip install -i https://test.pypi.org/simple/ is_instance

uninstall:
	pip uninstall $(PKG)

clean:
	rm -rfv dist/ build/ src/*.egg-info

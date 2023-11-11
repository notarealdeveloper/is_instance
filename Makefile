PKG := is_instance

build:
	python -m build

install:
	pip install .

develop:
	pip install -e .

check:
	@python -c "__import__('is_instance').__test__()"

uninstall:
	pip uninstall $(PKG)

clean:
	rm -rfv dist/ build/ src/*.egg-info

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

push-test:
	python -m twine upload --repository testpypi dist/*

pull-test:
	pip install -i https://test.pypi.org/simple/ is_instance

push-prod:
	python -m twine upload dist/*

pull-prod:
	pip install is_instance

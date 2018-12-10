test:
	pytest

lint:
	python3 -m pylint pyicmd

publish: test lint
	python3 setup.py sdist bdist_wheel
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

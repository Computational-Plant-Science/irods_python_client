test:
	pytest

lint:
	python3 -m pylint --enable=spelling --spelling-dict en_US --spelling-private-dict-file tests/spelling_dict.txt  pyicmd

publish-test: test lint
	python3 setup.py sdist bdist_wheel
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

publish: test lint
	python3 setup.py sdist bdist_wheel
	twine upload dist/*

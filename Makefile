default: 
	python3 main.py

fmt:
	black . $(ARGS)

install:
	pip3 install --user -r requirements.txt

install-dev:
	pip3 install --user -r requirements-dev.txt

lint:
	pylint main.py

test:
	python -m pytest -s -vv -W ignore tests

.PHONY: \
	fmt \
	install	\
	install-dev \
	lint \
	test
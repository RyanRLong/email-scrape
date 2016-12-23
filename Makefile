TEST_PATH=./tests

clean:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '*~' -exec rm --force {} +

lint:
	pylint ./email_scrape/*

lint-report:
	pylint ./email_scrape/* > lint_report

init:
	pip install -r requirement.txt

test:
	nosetests tests

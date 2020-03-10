black: 
	black setup.py
	black libsemigroups_cppyy/*.py
	black tests/*.py

check:
	tox -- -x tests/

# JDM: couldn't get the coverage target to work outside a virtual env
coverage:
	pip install .
	coverage run -m nose --where tests/
	coverage html
	@echo "See: htmlcov/index.html" 

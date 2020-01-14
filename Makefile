black:
	black libsemigroups_cppyy/*.py
	black tests/*.py
check:
	tox -- -x tests/

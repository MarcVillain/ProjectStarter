.PHONY: format

check:
	pytest tests

format:
	black -l 120 .

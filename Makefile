clean:
	@find ./ -name "*.pyc" -exec rm {} \;


update:
	poetry shell
	poetry check
	poetry update
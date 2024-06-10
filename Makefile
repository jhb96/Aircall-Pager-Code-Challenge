
install:
	@echo "install"
	@pip install -r requirements.txt

test: 
	@echo "test"
	@python -m unittest discover -v -s ./tests -p "test_*.py"

start-server:
	@echo "start server"
	@python -m uvicorn server:app --reload

HOW TO's:

I. Install the necessary dependencies for this project:
pip install -r requirements.txt

II. Run the program for tasks 1 and 2:
- Task 1:
python parse.py --part1

- Task 2:
python parse.py --part2

*If flags are omitted, Part1 is run by default*
III. Run tests without coverage
- the whole suite of tests:
pytest

- selecting certain test files to run:
pytest tests/<test filename>

IV. Run the whole suite of tests for each file WITH coverage 
and then retrieve report:
coverage run -m pytest
coverage report --omit venv\* -m

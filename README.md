# RoboLabs API

### Design decisions
- I decided to use `flask` library because it is a simple and lightweight framework.
I was considering `FastApi`, but `Flask` is better suited for handling frontend and
`FastApi` is better for developing API and in this case I needed to use the API.
- I decided to use `requests` library because I wanted to keep the code simple.
- I decided to use `poetry` for dependency management because it is a modern tool, it is easy to use, and it's
been my go-to virtual environment tool for a while now.
- I decided to use `pytest` for testing because I like `fixture` approach.
- I decided to use `pre-commit` because it applies many formatting options at once.
Plus it runs automatically everytime you run `git commit`.
- I decided to use `python-dotenv` for environment variables because it is a simple and lightweight library.
- I decided to use `structlog` for logging because it provides a convenient way to log structured data.
And it's colorful by default.


## Running the app

### 1. Install poetry environment
Installing poetry environment will install all the dependencies required for the project.

If you don't have poetry installed on your machine, you can install it with the following command:
```bash
pip install poetry
```
Then, you can initiate the poetry environment with the following command:
```bash
poetry install
```
If you don't want to use poetry, you can use any other virtual environment.
Requirements file is provided, so activate the virtual environment of your choice and run the following command:
```bash
pip install -r requirements.txt
```

### 2. Create a `.env` file
Create a `.env` file in the `src` directory of the project. You can use the `.env.example` file as a template.
Replace the placeholder values in `.env.example` file with your own.

### 3. Run the app

You can run the app with the following command:
```bash
poetry run python -m robolabs_api
```

## Running the tests

To run all tests use the following command:
```bash
poetry run pytest
```

## Running the linter

If you made any changes and want to format the code,
run `pre-commit` with the following command:
```bash
poetry run pre-commit run -a
```

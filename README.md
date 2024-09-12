
# LLM-driven Data Engineering

## Project Overview

This project leverages Large Language Models (LLMs) to automate and enhance various data engineering tasks. The primary focus is on generating SQL queries, creating Airflow DAGs, and managing data transformations using a Postgres backend.

## Setup

To set up the project, follow these steps:

1. **Store the API key as an environment variable**:
    ```sh
    export OPENAI_API_KEY=<your_api_key>
    ```
    If you are using Windows, set the environment variable accordingly.

2. **Install the required libraries**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Restore the database**:
    To restore the database, run the following command:
    ```sh
    pg_restore -h localhost -p 5432 -d postgres -U postgres --clean --if-exists --no-owner --disable-triggers --no-acl data/halo_data_dump.dump
    ```
    Make sure you have Postgres up and running either via Homebrew or Docker.

## Project Structure

The project directory is structured as follows:

```
__init__.py
.gitignore
.vscode/
    settings.json
data/
    halo_data_dump.dump
docker-compose.yaml
documentation.log
output/
    airflow_dag.py
    documentation.md
    player_scd_generation.sql
poetry.lock
pyproject.toml
README.md
requirements.txt
schemas/
    actor_films.sql
    game_details.sql
    games.sql
    player_seasons.sql
    players_scd_table.sql
    players.sql
    t_r_customer_service_reporting.sql
src/
    __init__.py
    __pycache__/
    generate_dag_script.py
    generate_documentation_script.py
    generate_sql_script.py
    ...
```

## Key Components

### 1. Environment Variables

The project relies on environment variables for configuration. Ensure you have the following variables set

:



- [`OPENAI_API_KEY`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Ffoliveira%2Fprojects%2Fpersonal%2Fllm_data_engineering%2FREADME.md%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A7%2C%22character%22%3A11%7D%7D%5D%2C%2230b83037-dc5c-4a31-a33d-bf1f46fcd973%22%5D "Go to definition"): Your OpenAI API key.
- `LANGCHAIN_DATABASE_URL`: The URL for your Postgres database.
- `YOUR_EMAIL`: Your email address for notifications.

### 2. Scripts

- **`generate_dag_script.py`**: Generates an Airflow DAG for incremental data processing.
- **`generate_documentation_script.py`**: Generates documentation for the project.
- **`generate_sql_script.py`**: Generates SQL scripts for data transformations.

### 3. Utilities

- **`util.py`**: Contains utility functions such as `get_api_key()` to retrieve the API key from environment variables.

## Usage

### Generating an Airflow DAG

To generate an Airflow DAG, run the `generate_dag_script.py` script:

```sh
python src/generate_dag_script.py
```

This script will read the schemas from the [`schemas`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Ffoliveira%2Fprojects%2Fpersonal%2Fllm_data_engineering%2Fschemas%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%2230b83037-dc5c-4a31-a33d-bf1f46fcd973%22%5D "/home/foliveira/projects/personal/llm_data_engineering/schemas") directory, generate a system prompt, and create an Airflow DAG based on the provided requirements.

### Generating Documentation

To generate documentation, run the `generate_documentation_script.py` script:

```sh
python src/generate_documentation_script.py
```

This script will generate documentation based on the project's structure and components.

### Generating SQL Scripts

To generate SQL scripts, run the `generate_sql_script.py` script:

```sh
python src/generate_sql_script.py
```

This script will generate SQL scripts for data transformations based on the provided schemas.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For any questions or inquiries, please contact [your_email@example.com](mailto:your_email@example.com).
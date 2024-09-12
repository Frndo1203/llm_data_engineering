# LLM-driven Data Engineering
## Setup

To set up the project, follow these steps:

1. Store the API key as an environment variable. Run the following command:
    ```
    export OPENAI_API_KEY=<your_api_key>
    ```
    If you are using Windows, set the environment variable accordingly.

2. Install the required libraries by running the command:
    ```
    pip install -r requirements.txt
    ```

## Lab

In this lab, we will be using the schemas from Dimensional Data Modeling Week 1 to generate queries using LLMs

### Setup

If you are watching live, you will be provided with a cloud database URL to use. Set the environment variable using the following command:
```
export LANGCHAIN_DATABASE_URL=<value zach gives in Zoom>
```

If you are not watching live, you can use the `halo_data_dump.dump` file located in the `data` folder. To restore the database, run the following command:
```
pg_restore -h localhost -p 5432 -d postgres -U postgres --clean --if-exists --no-owner --disable-triggers --no-acl data/halo_data_dump.dump
```

Make sure you have Postgres up and running either via Homebrew or Docker.

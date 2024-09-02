# LLM-driven Data Engineering

## Setup

Store the API key as an environment variable like:
`export OPENAI_API_KEY=<your_api_key>`
Or set it in Windows

Run the command `pip install -r requirements.txt` to get the OpenAI and Pandas libraries

## Day 1 Lab

We'll be using the schemas from Dimensional Data Modeling Week 1 and generating the queries from the homework and labs except this time we'll do it via LLMs


## Day 2 Lab

We'll be using Langchain to auto generate SQL queries for us based on tables and writing LinkedIn posts in Zach Wilson's voice
### Setup

If you are watching live, you will be given a cloud database URL to use.
`export LANGCHAIN_DATABASE_URL=<value zach gives in Zoom>`

If you aren't watching live, you'll need to use the `halo_data_dump.dump` file located in the `data` folder

Running `pg_restore` with your local database should get you up and running pretty quickly. 

- example command, assuming you got Postgres up and running either via Homebrew or Docker:
 - `pg_restore -h localhost -p 5432 -d postgres -U postgres --clean --if-exists --no-owner --disable-triggers --no-acl data/halo_data_dump.dump`
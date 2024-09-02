from openai import OpenAI
from util import get_api_key

client = OpenAI(api_key=get_api_key())
import os
from util import get_api_key

schema_files = os.listdir('schemas')

all_schemas = {}

for file in schema_files:
    opened_file = open('schemas/' + file, 'r')
    all_schemas[file] = opened_file.read()

system_prompt = """
                You are a highly skilled data engineer tasked with generating an Airflow pipeline 
                DAG skeleton. The DAG should be designed to manage data transformations 
                using a Postgres backend. Your goal is to define the structure and 
                dependencies of the DAG, without delving into the specific SQL queries, 
                ensuring that it can be easily integrated with the appropriate SQL details later.
            """

user_prompt = f"""
Create a skeleton for an Airflow DAG that performs incremental data processing, transforming the data from:

Input Schema: {all_schemas['player_seasons.sql']}
Output Schema: {all_schemas['players.sql']}

### Requirements:
- **Task Structure**: The DAG should be structured to scan and process one season's data at a time.
- **Dependencies**: The DAG should depend on the last season's data from the `players` table. Ensure the DAG is configured with `depends_on_past=True` to maintain data consistency across runs.
- **Joins and Filters**: Each DAG run should perform a FULL OUTER JOIN of the current season's data with previous seasons, using the `ds` Airflow parameter to filter by the season.
- **Table Creation**: Ensure all `CREATE TABLE` statements within the DAG include the `IF NOT EXISTS` clause to prevent re-creation of existing tables.
- **Output Format**: Provide the DAG structure in markdown format, emphasizing readability and correct task dependencies.
- **Database**: Assume that Postgres is the backend for all data operations within the DAG.
- Use the most recent steps for creating, like context managing, and, if apllicable, decorators

### Additional Notes:
- The focus is on defining the skeleton and structure of the DAG, not the specific SQL transformations.
- Ensure that the DAG is modular and scalable, capable of handling additional seasons' data in future runs.
"""

print(system_prompt)
print(user_prompt)

response = client.chat.completions.create(model="gpt-4",
messages=[
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt}
],
temperature=0)
answer = response.choices[0].message.content

if not os.path.exists('output'):
    os.mkdir('output')

output = filter(lambda x: x.startswith('python'), answer.split('```'))
# Open the file with write permissions
with open('output/airflow_dag.py', 'w') as file:
    # Write some data to the file
    file.write('\n'.join(output))



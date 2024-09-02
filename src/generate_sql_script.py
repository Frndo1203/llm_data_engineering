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

system_prompt = """You are an expert data engineer specializing in SQL transformations 
and data warehousing. Your current task is to design and generate SQL queries that 
create and manage slowly-changing dimension (SCD) tables. Your solutions should handle 
versioning of data while maintaining the integrity and history of changes, specifically 
focusing on tracking the state of critical dimensions over time."""

user_prompt = f"""
Given the following input schema for the cumulative table:

{all_schemas['players.sql']}

and the expected output schema for the slowly-changing dimension table:

{all_schemas['players_scd_table.sql']}

Generate a SQL query to perform a slowly-changing dimension transformation. This query should 
track changes specifically in the `is_active` and `scoring_class` columns. Ensure that your 
solution handles inserts, updates, and historical tracking of these dimensions. 
"""

print(system_prompt)
print(user_prompt)

response = client.chat.completions.create(model="gpt-4o-mini",
messages=[
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt}
],
temperature=0)
print(response)
answer = response.choices[0].message.content


if not os.path.exists('output'):
    os.mkdir('output')

# ```sql
# SELECT * FROM table
# ```

output = filter(lambda x: x.startswith('sql'), answer.split('```'))
# Open the file with write permissions
with open('output/player_scd_generation.sql', 'w') as file:
    # Write some data to the file
    file.write('\n'.join(output))



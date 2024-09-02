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

system_prompt = """You are a meticulous data engineer responsible for creating comprehensive documentation for your datasets. Your documentation should include detailed descriptions of each dataset, its columns, data types, and relationships, formatted in a clear and accessible manner."""

user_prompt = f"""Using cumulative table input schema {all_schemas['players.sql']}
                 Generate a pipeline documentation in markdown 
                    that shows how this is generated from 
                {all_schemas['player_seasons.sql']}
                make sure to include example queries that use the season stats array
                make sure to document all columns seprately for both input and output in a markdown table having column type and description
                make sure to document all created types as well
            """

print(system_prompt)
print(user_prompt)

response = client.chat.completions.create(model="gpt-4o-mini",
messages=[
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt}
],
temperature=0)
answer = response.choices[0].message.content

if not os.path.exists('output'):
    os.mkdir('output')
# Open the file with write permissions
with open('output/documentation.md', 'w') as file:
    # Write some data to the file
    file.write(answer)



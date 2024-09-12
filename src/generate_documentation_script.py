import os
from openai import OpenAI
from util import get_api_key

def read_schema_files():
    schema_files = os.listdir('schemas')
    all_schemas = {}

    for file in schema_files:
        with open(f'schemas/{file}', 'r') as opened_file:
            all_schemas[file] = opened_file.read()

    return all_schemas

def generate_documentation():
    system_prompt = """
        You are a meticulous data engineer responsible for creating comprehensive 
        documentation for individual database tables. Your task is to produce 
        detailed and clear documentation for a table based on its DDL. This 
        documentation should include descriptions of each column, data types, 
        and any relevant constraints or relationships. The output should be 
        formatted in markdown for easy readability and accessibility.
    """

    all_schemas = read_schema_files()

    user_prompt = f"""
        Using the schema definition (DDL) for the table:

        **Table Schema**: {all_schemas['t_r_customer_service_reporting.sql']}

        ### Documentation Requirements:

        1. **Table Description**:
           - Provide a brief overview of the table, summarizing its purpose and role within 
           the database.

        2. **Column Details**:
           - Create a markdown table that includes the following columns:
             - **Column Name**: The name of each column in the table.
             - **Data Type**: The data type of each column.
             - **Description**: A brief explanation of what each column represents or its 
             significance.

        ### Example Markdown Table Format:

        | Column Name | Data Type | Description |
        |-------------|-----------|-------------|
        | id          | INT       | Unique identifier for each player. |
        | name        | VARCHAR   | Name of the player. |
        | is_active   | BOOLEAN   | Indicates whether the player is currently active. |

        ### Additional Notes:
        - The documentation should be concise and focus on providing essential information 
        about the table and its columns.
        - Ensure that the markdown table is formatted correctly and is easy to read.
    """

    client = OpenAI(api_key=get_api_key())
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0
    )
    answer = response.choices[0].message.content

    if not os.path.exists('output'):
        os.mkdir('output')

    with open('output/documentation.md', 'w') as file:
        file.write(answer)

    # Add trace for function output
    print("Generated documentation successfully.")

if __name__ == "__main__":
    generate_documentation()

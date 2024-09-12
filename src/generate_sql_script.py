import os
from openai import OpenAI
from util import get_api_key

class SQLGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=get_api_key())
        self.schema_files = os.listdir('schemas')
        self.all_schemas = {}

    def read_schemas(self):
        for file in self.schema_files:
            with open(f'schemas/{file}', 'r') as opened_file:
                self.all_schemas[file] = opened_file.read()

    def generate_sql_query(self):
        system_prompt = """You are an expert data engineer specializing in SQL transformations 
        and data warehousing. Your current task is to design and generate SQL queries that 
        create and manage slowly-changing dimension (SCD) tables. Your solutions should handle 
        versioning of data while maintaining the integrity and history of changes, specifically 
        focusing on tracking the state of critical dimensions over time."""

        user_prompt = f"""
        Given the following input schema for the cumulative table:

        {self.all_schemas['players.sql']}

        and the expected output schema for the slowly-changing dimension table:

        {self.all_schemas['players_scd_table.sql']}

        Generate a SQL query to perform a slowly-changing dimension transformation. This query should 
        track changes specifically in the `is_active` and `scoring_class` columns. Ensure that your 
        solution handles inserts, updates, and historical tracking of these dimensions. 
        """

        response = self.client.chat.completions.create(model="gpt-4o-mini",
                                                      messages=[
                                                          {"role": "system", "content": system_prompt},
                                                          {"role": "user", "content": user_prompt}
                                                      ],
                                                      temperature=0)
        answer = response.choices[0].message.content

        if not os.path.exists('output'):
            os.mkdir('output')

        output = filter(lambda x: x.startswith('sql'), answer.split('```'))
        with open('output/player_scd_generation.sql', 'w') as file:
            file.write('\n'.join(output))

if __name__ == "__main__":
    sql_generator = SQLGenerator()
    sql_generator.read_schemas()
    sql_generator.generate_sql_query()

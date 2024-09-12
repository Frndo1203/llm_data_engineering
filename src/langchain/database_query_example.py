import os
import argparse
from dotenv import load_dotenv
from langchain_openai.chat_models import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain_community.agent_toolkits.gmail.toolkit import GmailToolkit
from langchain_community.tools.gmail.utils import build_resource_service, get_gmail_credentials
from langchain.agents import initialize_agent, AgentType

class LLM:
    def __init__(self, temperature, openai_api_key, model_name):
        self.temperature = temperature
        self.openai_api_key = openai_api_key
        self.model_name = model_name

    def initialize(self):
        return ChatOpenAI(temperature=self.temperature, openai_api_key=self.openai_api_key, model_name=self.model_name)

class GmailToolkitFactory:
    @staticmethod
    def create_toolkit():
        credentials = get_gmail_credentials(
            token_file="token.json",
            scopes=["https://mail.google.com/"],
            client_secrets_file="credentials.json",
        )
        api_resource = build_resource_service(credentials=credentials)
        return GmailToolkit(api_resource=api_resource)

class GmailAgentFactory:
    @staticmethod
    def create_agent(llm, toolkit):
        return initialize_agent(
            tools=toolkit.get_tools(),
            llm=llm,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        )


class DatabaseFactory:
    @staticmethod
    def create_database(database_url, include_tables):
        return SQLDatabase.from_uri(
            database_url,
            include_tables=include_tables
        )


class DatabaseChainFactory:
    @staticmethod
    def create_database_chain(llm, database):
        return SQLDatabaseChain(llm=llm, database=database, verbose=True)


class PromptHandler:
    def __init__(self, db_chain, agent=None, email=None):
        self.db_chain = db_chain
        self.agent = agent
        self.email = email

    def get_prompt(self):
        print("Type 'exit' to quit")

        while True:
            prompt = input("Enter a prompt: ")

            if prompt.lower() == 'exit':
                print('Exiting...')
                break
            else:
                try:
                    question = self._format_query(prompt)
                    results = self.db_chain.run(question)
                    print(results)
                    if self.agent:
                        self.agent.run(
                            "Create an email with these results in a table: " + results +
                            " Then send it to {email} with the subject".format(email=self.email) +
                            " " + prompt
                        )
                except Exception as e:
                    print(e)

    def _format_query(self, prompt):
        QUERY = """
        Given an input question, first create a syntactically correct postgresql query to run, then look at the results of the query and return the answer.
        Use the following format:

        Question: Question here
        SQLQuery: SQL Query to run
        SQLResult: Result of the SQLQuery
        Answer: Final answer here

        {question}

        Example:
        Question: What is the total number of medals won by each player?
        SQL Query: SELECT player_name, COUNT(*) as total_medals FROM medals_matches_players GROUP BY player_name;
        SQL Result: 
        player_name | total_medals
        ------------+--------------
        John        | 5
        Sarah       | 3
        ...
        Answer: The total number of medals won by each player is displayed in the SQL Result.
        """
        return QUERY.format(question=prompt)


def main():
    API_KEY = os.environ.get('OPENAI_API_KEY')
    database_url = 'postgresql+psycopg2://postgres:postgres@localhost:5432/postgres'
    temperature = 0  # TODO Set your desired temperature value here
    openai_api_key = API_KEY  # TODO Set your OpenAI API Key here
    model_name = 'gpt-4o-mini'  # TODO Set your desired model name here
    email = ''  # Set your email here
    include_tables = ['medals', 'match_details', 'matches', 'medals_matches_players']  # TODO Set your desired tables to include here

    load_dotenv()

    llm = LLM(temperature=temperature, openai_api_key=openai_api_key, model_name=model_name)
    llm_instance = llm.initialize()

    agent = None
    if email:
        credentials = get_gmail_credentials(
            token_file="token.json",
            scopes=["https://mail.google.com/"],
            client_secrets_file="credentials.json",
        )
        api_resource = build_resource_service(credentials=credentials)
        toolkit = GmailToolkitFactory.create_toolkit(api_resource)
        agent = GmailAgentFactory.create_agent(llm_instance, toolkit)

    database = DatabaseFactory.create_database(database_url, include_tables)
    db_chain = DatabaseChainFactory.create_database_chain(llm_instance, database)

    prompt_handler = PromptHandler(db_chain, agent, email)
    prompt_handler.get_prompt()


if __name__ == "__main__":
    main()

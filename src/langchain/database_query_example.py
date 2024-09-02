from dotenv import load_dotenv
from langchain_openai.chat_models import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain_community.agent_toolkits.gmail.toolkit import GmailToolkit
from langchain_community.tools.gmail.utils import build_resource_service, get_gmail_credentials
from langchain.agents import initialize_agent, AgentType
import os


load_dotenv()

API_KEY = os.environ.get('OPENAI_API_KEY')
# setup llm
llm = ChatOpenAI(temperature=0, openai_api_key=API_KEY, model_name='gpt-4o-mini')

def create_gmail_toolkit():
    # Can review scopes here https://developers.google.com/gmail/api/auth/scopes
    # For instance, readonly scope is 'https://www.googleapis.com/auth/gmail.readonly'
    credentials = get_gmail_credentials(
        token_file="token.json",
        scopes=["https://mail.google.com/"],
        client_secrets_file="credentials.json",
    )
    api_resource = build_resource_service(credentials=credentials)
    return GmailToolkit(api_resource=api_resource)

def create_gmail_agent(llm, toolkit):
    return initialize_agent(
        tools=toolkit.get_tools(),
        llm=llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    )

# setup email agent if you want to send the results somewhere
# Make sure to have a credentials.json file with a google app with Gmail enabled
# Create a google app here: https://console.cloud.google.com/apis
YOUR_EMAIL = ''# os.environ.get('YOUR_EMAIL')
agent = None
if YOUR_EMAIL:
    toolkit = create_gmail_toolkit()
    agent = create_gmail_agent(llm, toolkit)

database_url = 'postgresql+psycopg2://postgres:postgres@localhost:5432/postgres'#os.environ['LANGCHAIN_DATABASE_URL']

# Setup database
db = SQLDatabase.from_uri(
    database_url,
    include_tables=['medals', 'match_details', 'matches', 'medals_matches_players']
)

# Create db chain
QUERY = """
Given an input question, first create a syntactically correct postgresql query to run, then look at the results of the query and return the answer.
Use the following format:

Question: Question here
SQLQuery: SQL Query to run
SQLResult: Result of the SQLQuery
Answer: Final answer here

{question}
"""

# Setup the database chain
db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)

def get_prompt():
    print("Type 'exit' to quit")

    while True:
        prompt = input("Enter a prompt: ")

        if prompt.lower() == 'exit':
            print('Exiting...')
            break
        else:
            try:
                question = QUERY.format(question=prompt)
                results = db_chain.run(question)
                print(results)
                if agent:
                    agent.run(
                        "Create an email with these results in a table: " + results +
                        " Then send it to {email} with the subject".format(email=YOUR_EMAIL) +
                        " " + prompt
                    )
            except Exception as e:
                print(e)

get_prompt()
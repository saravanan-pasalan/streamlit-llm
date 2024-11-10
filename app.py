import streamlit as st
import os
import sqlite3
import json
import logging

from dotenv import load_dotenv
from openai import AzureOpenAI,RateLimitError
from azure.identity import DefaultAzureCredential,get_bearer_token_provider

load_dotenv()

# cred = DefaultAzureCredential()
# token_provider = get_bearer_token_provider(cred,"https://cognitiveservices.azure.com/default")


# client = AzureOpenAI (
#     azure_ad_token_provider = token_provider,
#     api_version="2024-11-09",
#     azure_endpoint = 'https://aomething.openai.azure.com'
# )

# response = client.completions.create(model='gpt-35-turbo',prompt='tell me a joke',max_token=80)
# print("\n###########")
# print(response.choices[0].text)

try:
    DEPLOYMENT_NAME = os.environ['DEPLOYMENT_NAME']
    ENDPOINT_URL = os.environ['ENDPOINT_URL']
    ENDPOINT_KEY = os.environ['ENDPOINT_KEY']
except:
    print('Missing required environemtn variables')
    exit()

logger = logging.getLogger(__name__)
logging.basicConfig(filename='app.log',level=logging.INFO)

client = AzureOpenAI(
    api_key = ENDPOINT_KEY,
    api_version="2024-10-01-preview",
    azure_endpoint = ENDPOINT_URL
    
)

with open('DatabaseMetadata.sql','r') as file:
    tableMetadata = file.read().replace('\n', '')

st.title('# Natural Language to SQL')

try:
    con = sqlite3.connect('database.db')
except:
    print('Database connection doesnot exist')
    st.error('Database connection doesnot exist')
    exit()

context = f'''Generate an SQL query ready 
to run on sqlite database  with the 
following tables {tableMetadata}
that will be used to answer the following question
Answer only with sql query.
'''

with st.form("Natural Language input"):
    question = st.text_input('Ask a Question')

    Submitted= st.form_submit_button('Submit')
    if Submitted:
        if len(question) == 0:
            st.error('Ask a quest first')
            #exit()
        try:
            completion = client.chat.completions.create(
                model=DEPLOYMENT_NAME,
                messages=[{
                    "role": "system",
                    "content": context
                },{
                    "role": "user",
                    "content": question
                }],
                max_tokens=40
            )
        except RateLimitError:
            st.error('Too many requests try again in a while')
            #exit()
        except Exception as e:
            st.error(f'Unkown error while sending request to OpenAI {e}')
            #exit()
        answer = json.loads(completion.to_json())




        #Preprocess the answer to get only the query
        message = answer["choices"][0]["message"]["content"]
        selectPos = message.upper().find('SELECT')
        semiColonPos= message[selectPos:].find(';') + selectPos
        query = message[selectPos:semiColonPos+1]

        if len(query) ==0:
            st.error('Respond did not contain a query')
            #exit()
        
        try:
            result = con.execute(query)
            resulSet = result.fetchall()
        except:
            st.error('There was a error while execting a query, try re phrasing it')
            #exit()
        
        with st.expander('Query'):
            st.write('The Query which is used to generate this results')
            st.code(query)
        
        columnLabels = {index+1: item[0] for index, item in enumerate(result.description)}

        st.write('Result')
        st.dataframe(resulSet,column_config=columnLabels,use_container_width=True)

        logger.info(f'Question {question}')
        logger.info(f'Answer {message}')
        logger.info(f'Query {query}')
        logger.info(f'Results {resulSet}')
        logger.info(f'Description of Results {result.description}')


# with open('database.sql','r') as file:
#     dbsetup = file.read()

# con.executescript(dbsetup)

# con.close()
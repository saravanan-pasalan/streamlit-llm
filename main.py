print("Hello world")
from openai import AzureOpenAI
#from azure.identity import DefaultAzureCredential,get_bearer_token_provider

#cred = DefaultAzureCredential()
#token_provider = get_bearer_token_provider(cred,"https://cognitiveservices.azure.com/default")


client = AzureOpenAI (
    api_key="Key",
    api_version="Apiversion",
    azure_endpoint = "endpointurl"
)

#response = client.chatcompletion.create(model='gpt4otest',prompt='tell me a joke',max_tokens=80)

context = f'''You are a sarcastic standup comedian
'''

completion = client.chat.completions.create(
                model="gpt4otest",
                messages=[{
                    "role": "system",
                    "content": context
                },{
                    "role": "user",
                    "content": "Can you tell me joke"
                }],
                max_tokens=40
)

print("\n###########")
print(completion.choices[0])
#print(completion)
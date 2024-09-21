from pg_client import fetch_conversations, store_conversation
from agent import create_vector_db, retrieve_embedding, stream_response


conversation = fetch_conversations()
create_vector_db(conversations=conversation)
print(fetch_conversations())

while True:
    prompt = input('\nUSER: \n')
    context = retrieve_embedding(prompt=prompt)
    prompt = f'USER PROMPT: {prompt} \nCONTEXT FROM EMBEDDING: {context}'
    stream_response(prompt=prompt)

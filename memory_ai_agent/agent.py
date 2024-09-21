import ollama
from pg_client import fetch_conversations, store_conversation
from chroma_client import client


system_prompt = (
    'You are an AI assistant that has memory of every conversation you have ever had with this user.'
    'On every prompt from the user, the system has checked for any relevant messages you have had with the user'
    'If any embedded previous conversation are attached, use them for context to responding to the user,'
    'if the context is not relevant and useful to responding. If the recalled conversation are irrelevant, '
    'disregard speaking about them and respond normally as an AI assistant. Do not talk about recalling conversations.'
    'Just use any useful data from the previous conversation and respond normally as an ingelligent AI assistant.'
)
convo = [{'role': 'system', 'content': system_prompt}]


def stream_response(prompt):
    convo.append({'role': 'user', 'content': prompt})
    response = ''
    stream = ollama.chat(model='llama3.1', messages=convo, stream=True)
    print('\nASSISTANT:')

    for chunk in stream:
        content = chunk['message']['content']
        response += content
        print(content, end='', flush=True)

    print('\n')
    store_conversation(prompt=prompt, response=response)
    convo.append({'role': 'assistant', 'content': response})

def create_vector_db(conversations):
    vector_db_name = 'conversations'
    try:
        client.delete_collection(name=vector_db_name)
    except ValueError:
        pass

    vector_db = client.create_collection(name=vector_db_name)

    for c in conversations:
        serialized_convo = f'prompt: {c["prompt"]}, response: {c["response"]}'
        response = ollama.embeddings(model='nomic-embed-text', prompt=serialized_convo)
        embedding = response['embedding']

        vector_db.add(
            ids=[str(c['id'])],
            embeddings=[embedding],
            documents=[serialized_convo]
        )

def retrieve_embedding(prompt):
    response = ollama.embeddings(model='nomic-embed-text', prompt=prompt)
    prompt_embedding = response['embedding']

    vector_db = client.get_collection(name='conversations')
    results = vector_db.query(query_embeddings=[prompt_embedding], n_results=1)
    best_embedding = results['documents'][0][0]

    return best_embedding
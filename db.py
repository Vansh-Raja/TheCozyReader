import couchdb
import base64
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".config/.env")

# Set CouchDB username and password from .env file
couchdb_user = os.getenv('COUCHDB_USER')
couchdb_password = os.getenv('COUCHDB_PASSWORD')
couchdb_url = os.getenv('COUCHDB_URL')

# Connect to CouchDB server with authentication
couch = couchdb.Server('http://localhost:5984/')
couch.resource.credentials = (couchdb_user, couchdb_password)

# Create or select a database
db_name = 'users_db'
if db_name in couch:
    db = couch[db_name]
else:
    db = couch.create(db_name)

def create_user(username:str):
    "Insert a new user."
    
    user = {
        '_id': username,
        'stories': []
    }
    db.save(user)
    print(f'User {username} created.')

def insert_story(username:str, title:str, story:str, audio_file_path:str):
    "Insert a story for a given user."
    
    user = db.get(username)
    if user:
        with open(audio_file_path, 'rb') as f:
            audio_data = f.read()
        
        story = {
            'title': title,
            'story': story,
            'audio_file': base64.b64encode(audio_data).decode('utf-8')
        }
        user['stories'].append(story)
        db.save(user)
        print(f'Story inserted for user {username}.')
        return True
    else:
        print(f'User {username} not found.')
        raise ValueError(f'User {username} not found.')

def retrieve_stories(username:str):
    "Retrieve stories for a given user."
    
    user = db.get(username)
    if user:
        stories = []
        for story in user['stories']:
            audio_data = base64.b64decode(story['audio_file'])
            stories.append({
                'title': story['title'],
                'story': story['story'],
                'audio_file': audio_data
            })
        return stories
    else:
        raise Exception(f'User {username} not found.')

def delete_story(username:str, title:str):
    "Delete a story for a given user."
    
    user = db.get(username)
    if user:
        original_length = len(user['stories'])
        user['stories'] = [story for story in user['stories'] if story['title'] != title]
        if len(user['stories']) < original_length:
            db.save(user)
            return f'Story {title} deleted for user {username}.'
        else:
            raise Exception(f'Story {title} not found for user {username}.')
    else:
        raise Exception(f'User {username} not found.')

# create_user('rbriggs')


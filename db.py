import couchdb
import base64
import os
from dotenv import load_dotenv

load_dotenv()

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

def insert_user(username):
    "Insert a new user."
    
    user = {
        '_id': username,
        'username': username,
        'stories': []
    }
    db.save(user)
    print(f'User {username} inserted.')

def insert_story(username, title, content, audio_file_path):
    "Insert a story for a given user."
    
    user = db.get(username)
    if user:
        with open(audio_file_path, 'rb') as f:
            audio_data = f.read()
        
        story = {
            'title': title,
            'content': content,
            'audio_file': base64.b64encode(audio_data).decode('utf-8')
        }
        user['stories'].append(story)
        db.save(user)
        return f'Story {title} inserted for user {username}.'
    else:
        return f'User {username} not found.'

def retrieve_stories(username):
    "Retrieve stories for a given user."
    
    user = db.get(username)
    if user:
        stories = []
        for story in user['stories']:
            audio_data = base64.b64decode(story['audio_file'])
            stories.append({
                'title': story['title'],
                'content': story['content'],
                'audio_file': audio_data
            })
        return stories
    else:
        return f'User {username} not found.'

def delete_story(username, title):
    "Delete a story for a given user."
    
    user = db.get(username)
    if user:
        original_length = len(user['stories'])
        user['stories'] = [story for story in user['stories'] if story['title'] != title]
        if len(user['stories']) < original_length:
            db.save(user)
            return f'Story {title} deleted for user {username}.'
        else:
            return f'Story {title} not found for user {username}.'
    else:
        return f'User {username} not found.'

# Example usage
insert_user('johnd')
# print(result)
# result = insert_story('johnd', 'First Story', 'This is the *Markdown* content of the first story.', 'path_to_your_audio_file.wav')
# print(result)
# stories = retrieve_stories('johnd')
# for story in stories:
#     print(f"Title: {story['title']}")
#     print(f"Content: {story['content']}")
#     with open(f'retrieved_{story["title"].replace(" ", "_")}.wav', 'wb') as f:
#         f.write(story['audio_file'])
# result = delete_story('johnd', 'First Story')
# print(result)

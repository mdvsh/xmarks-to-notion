from notion_client import Client
import json, time, os
from typing import List, Dict, Any

def save_notion_progress(processed_urls: set, filename='notion_progress.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(list(processed_urls), f)

def load_notion_progress(filename='notion_progress.json'):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return set(json.load(f))
    return set()

def sync_to_notion(notion_token: str, database_id: str, bookmarks: List[Dict[str, Any]], batch_size: int = 10):
    notion = Client(auth=notion_token)
    
    processed_urls = load_notion_progress()
    print(f"Found {len(processed_urls)} previously processed bookmarks")
    
    bookmarks_to_process = [b for b in bookmarks if b['url'] not in processed_urls]
    print(f"Processing {len(bookmarks_to_process)} new bookmarks")
    
    for i in range(0, len(bookmarks_to_process), batch_size):
        batch = bookmarks_to_process[i:i + batch_size]
        print(f"Processing batch {i//batch_size + 1} of {(len(bookmarks_to_process) + batch_size - 1)//batch_size}")
        
        for bookmark in batch:
            if bookmark['url'] in processed_urls:
                continue
                
            try:
                notion.pages.create(
                    parent={"database_id": database_id},
                    properties={
                        "Name": {"title": [{"text": {"content": bookmark['text'][:100]}}]},
                        "URL": {"url": bookmark['url']},
                        "Created": {"date": {"start": bookmark['timestamp']}}
                    }
                )
                processed_urls.add(bookmark['url'])
                save_notion_progress(processed_urls)
                print(f"Added: {bookmark['url'][:60]}...")
                time.sleep(0.5) 
                
            except Exception as e:
                print(f"Error adding bookmark: {e}")
                print(f"Failed URL: {bookmark['url']}")
                if "Could not find database" in str(e):
                    raise ValueError("DB connection failed. Check your database ID and integration settings.")
                    
        time.sleep(2) 
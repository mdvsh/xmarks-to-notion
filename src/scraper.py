from playwright.sync_api import sync_playwright
from datetime import datetime
import os
import time
import re
import json

def save_bookmarks_to_file(bookmarks, filename='bookmarks_cache.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(bookmarks, f, indent=2)
    
    with open('bookmarks.md', 'w', encoding='utf-8') as f:
        f.write("# X (Twitter) Bookmarks Export\n\n")
        for bookmark in bookmarks:
            f.write(f"## {bookmark['timestamp']}\n")
            f.write(f"URL: {bookmark['url']}\n\n")
            f.write(f"```\n{bookmark['text']}\n```\n\n")
            f.write("---\n\n")

def load_cached_bookmarks(filename='bookmarks_cache.json'):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def wait_for_user_login(page):
    print("log in to X in the browser window...")
    print("Once logged in and on the bookmarks page, press Enter to continue...")
    input()
    return True

def scrape_bookmarks():
    cached_bookmarks = load_cached_bookmarks()
    if cached_bookmarks:
        print("Found cached bookmarks! Loading them...")
        return cached_bookmarks

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        page.goto('https://x.com/login')
        wait_for_user_login(page)
        
        page.goto('https://x.com/i/bookmarks')
        time.sleep(3)
        
        bookmarks = set()
        last_height = 0
        
        while True:
            tweets = page.locator('article').all()
            
            for tweet in tweets:
                try:
                    text = tweet.text_content()
                    link_element = tweet.locator('a[href*="/status/"]').first
                    link = link_element.get_attribute('href')
                    
                    status_id = re.search(r'/status/(\d+)', link).group(1)
                    clean_url = f'https://x.com/i/status/{status_id}'
                    
                    bookmark_data = {
                        'text': text.strip(),
                        'url': clean_url,
                        'timestamp': datetime.now().isoformat()
                    }
                    bookmarks.add(str(bookmark_data))
                    print(f"Added bookmark: {clean_url[:60]}...")
                except Exception as e:
                    print(f"Error processing tweet: {e}")
                    continue
            
            # scroll and check for end
            page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(2)
            
            new_height = page.evaluate('document.body.scrollHeight')
            if new_height == last_height:
                print("Reached end of bookmarks")
                break
            last_height = new_height
            print(f"Found {len(bookmarks)} unique bookmarks so far...")
            
        bookmarks = [eval(b) for b in bookmarks]
        save_bookmarks_to_file(bookmarks)
        return bookmarks
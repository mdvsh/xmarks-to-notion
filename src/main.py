import os
import sys
from scraper import scrape_bookmarks
from notion_sync import sync_to_notion

def check_env_variables():
    notion_token = os.getenv('NOTION_TOKEN')
    database_id = os.getenv('NOTION_DATABASE_ID')
    
    if not notion_token:
        notion_token = input("Enter Notion integration token: ")
        os.environ['NOTION_TOKEN'] = notion_token
    
    if not database_id:
        database_id = input("Enter Notion DB ID: ")
        os.environ['NOTION_DATABASE_ID'] = database_id.replace('-', '')

def main():
    print("Checking environment setup...")
    check_env_variables()
    
    try:
        print("\nStarting bookmark scraping...")
        bookmarks = scrape_bookmarks()
        print(f"Found {len(bookmarks)} bookmarks")
        
        print("\nSyncing to Notion...")
        sync_to_notion(
            notion_token=os.getenv('NOTION_TOKEN'),
            database_id=os.getenv('NOTION_DATABASE_ID'),
            bookmarks=bookmarks
        )
        print("\ndone! check your Notion database")
        
    except KeyboardInterrupt:
        print("\n\nProcess interrupted. Progress has been saved.")
        print("Run script again to continue from where you left off.")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        print("Check the error message above and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()
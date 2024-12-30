## xmarks-to-notion

Dump your X bookmarks into Notion. no fuss.

### what it does

- scrapes all your X bookmarks
- dumps them into a Notion database
- caches everything locally (so you don't lose progress if something breaks)
- handles rate limits and retries

### quick start

1. clone & setup
```bash
git clone <>
cd xmarks-to-notion
pip install -r requirements.txt
```

2. get your notion ready
- make a new integration here
- create an empty database in Notion
- copy your database ID
  - (it's in the URL, after `https://www.notion.so/` and before `?v=`)
- share your database with the integration

3. run it
```bash
python src/main.py
```

---

### notes
- uses Firefox (change browser in config if needed)
- saves bookmarks locally in JSON + markdown
- creates these columns in Notion: Name, URL, Created
- handles interruptions gracefully (just run it again)


### contributing
Found a bug? Want to add something cool? PRs welcome!

### credits
Started as a weekend project to avoid losing my X bookmarks and coming back to it later/integrating in PKM. Built using:

- playwright (browser automation)
- notion-client (Notion API)
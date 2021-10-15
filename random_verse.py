from requests import get, post
API_URL = "https://labs.bible.org/api/?passage=random&type=json"

def get_random_verse():
    response = get(API_URL).json()[0]
    book = response["bookname"]
    chapter = response["chapter"]
    verse = response["verse"]
    text = response ["text"]
    return f"'{text}\n\n📖{book} {chapter}:{verse}'\n\n🔑 Remember not to cherry pick scriptures, read in context, pray and test the word!"
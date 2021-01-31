import notion.client
from bs4 import BeautifulSoup
from urllib.request import urlopen


book_table = []
goodreads_url = "https://www.goodreads.com/book/show/"
# Obtain the `token_v2` value by inspecting your browser cookies on a logged-in (non-guest) session on Notion.so
client = notion.client.NotionClient(token_v2="---TOKEN---")

# Access a database using the URL of the database page or the inline block
# Copy link from the Book Tracker, making sure to copy the 'list' object under it. Should be a '?v=' in the link.
cv = client.get_collection_view("---LINK---")

for row in cv.collection.get_rows():
    case = {'id': row.id, 'Book_Id': row.Book_Id, 'Image': row.Image}
    book_table.append(case)

for idx, val in enumerate(book_table):
    url = goodreads_url + str(book_table[idx]['Book_Id'])
    url_open = urlopen(url)
    soup = BeautifulSoup(url_open, 'html.parser')
    tag = soup.find("img", {"id": "coverImage"})
    try:
        book_table[idx]['Image'] = tag['src']
    except:
        print("Book:", url, "found with no cover, try changing edition.")

for idx, row in enumerate(book_table):
    cv.collection.get_rows()[idx].Image = book_table[idx]['Image']
    print('Updating: ', cv.collection.get_rows()[idx].Name)


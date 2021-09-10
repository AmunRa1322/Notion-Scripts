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

print('Getting data from Notion...')

for row in cv.collection.get_rows():
    case = {'id': row.id, 'Book_Id': row.Book_Id, 'Image': row.Image}
    book_table.append(case)

print('Splitting the data into chunks of 10 elements...\n')

def split(list_a, chunk_size):
    for i in range(0, len(list_a), chunk_size):
        yield list_a[i:i + chunk_size]

book_table = list(split(book_table, 10))

print(str(len(book_table)) + ' chunks created.')

for idy, valA in enumerate(book_table):
    print('----')
    print('chunk ' + str(idy) + ' in progress')
    for idx, val in enumerate(valA):
        if len(val['Image']) == 0:
            url = goodreads_url + str(val['Book_Id'])
            url_open = urlopen(url)
            soup = BeautifulSoup(url_open, 'html.parser')
            tag = soup.find("img", {"id": "coverImage"})
            try:
                cv.collection.get_rows(search=f"{val['Book_Id']}")[0].Image = tag['src']
                print(str(idx + 1) + ' / 10 - ' + 'Updating: ', cv.collection.get_rows(search=f"{val['Book_Id']}")[0].Image)
            except:
                print("Book:", url, "found with no cover, try changing edition.")
        else:
            print(str(idx + 1) + ' / 10 - The image field is not empty, skipping this...')
    print('chunk ' + str(idy) + ' finished')

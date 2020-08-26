""" Main file """

from notion.client import NotionClient
from app import my_secrets

if __name__ == "__main__":
    print("Starting app...")

    client = NotionClient(token_v2=my_secrets.TOKEN_V2)

    collection_view = client.get_collection_view(
        url_or_id=my_secrets.MEMORIZATION_TIMES_TABLE_URL
    )

    print("Retrieving data from: " + collection_view.collection.name)
    for row in collection_view.collection.get_rows():
        print(f"Time: {row.time} \t Date: {row.date}")

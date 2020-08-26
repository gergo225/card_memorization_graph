""" Main file """

from notion.client import NotionClient
from app import my_secrets
from app.memorization_time import MemorizationTime

if __name__ == "__main__":
    print("Starting app...")

    client = NotionClient(token_v2=my_secrets.TOKEN_V2)

    collection_view = client.get_collection_view(
        url_or_id=my_secrets.MEMORIZATION_TIMES_TABLE_URL
    )

    memorization_times = []
    print("Retrieving data from: " + collection_view.collection.name)
    for row in collection_view.collection.get_rows():
        date = row.date
        if len(date) > 13:
            date = date[:14]
        mt = MemorizationTime(date=date, duration=row.time)
        memorization_times.append(mt)

    for time in memorization_times:
        print(f"Time: {time.duration} \t Date: {time.date}")

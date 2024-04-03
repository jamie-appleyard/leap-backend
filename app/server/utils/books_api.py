import requests

async def create_books(query, num=10):
    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_scholar",
        "q": query,
        "api_key": "e38fe8525f05569fd86cb0af9e619e714bc73291d6bb5672b3f8747b69f5c32f",
        "num": num
    }

    search = requests.get(url, params=params)
    data = search.json()
    books = data["organic_results"]
    
    return books

# print(create_books("Egypt"))

#title
#link
#snippet
#publication_info
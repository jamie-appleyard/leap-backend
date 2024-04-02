import requests
def bing_search(query, count=10):
    url = "https://api.bing.microsoft.com/v7.0/search"
    api_key = "e087a6d3ce5a49359b0c363e3661d68d"
    
    params = {
        "q": query,
        "count": count
    }
    
    headers = {
        "Ocp-Apim-Subscription-Key": api_key
    }
    
    try:
        response = requests.get(url, params=params, headers=headers) # Make a GET request to API
        response.raise_for_status() # Raises HTTPError for status codes between 400 and 600
        data = response.json() # Get JSON from api
        web_pages = data.get('webPages', {}).get('value', []) #Accessing URL value in JSON object
        
        urls = []; # Append urls found in each search result to this list (array)
        for page in web_pages:
            url = page.get('url')
            if url:
                #if an individual URL retrieval fails due to any reason (such as a missing URL or an error in the response), the function continues to process the remaining URLs and prints the list of URLs that were successfully retrieved
                urls.append(url)
        
        # print("Feeding URL to Cohere LLM:", urls) #Here we would return with that list to feed into Cohere
        
    except requests.exceptions.HTTPError as err:
        print(f'HTTP Error: {err}')
        
    except Exception as err:
        print(f'Error: {err}')

    return urls

# print(bing_search("Stonemasonry", count=10))
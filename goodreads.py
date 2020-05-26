import requests

def main():
    res = requests.get(f"https://www.goodreads.com/book/isbn/{isbn}?format=json", params={"key": "QikazWK11kUJNnHXepN9Iw", "isbn": book.isbn})
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")   
        print(res.json())
    

if __name__ == "__main__":
    main()
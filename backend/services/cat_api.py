from typing import Any
import requests
from config import Config

CAT_API_KEY = Config.CAT_API_KEY
if not CAT_API_KEY:
    raise ValueError("CAT_API_KEY is not set in the environment variables.")

BASE_URL = "https://api.thecatapi.com/v1"

HEADERS = {"x-api-key": CAT_API_KEY}


def get_id(breed=None) -> Any | None:
    """Gets the breed ID associated with a breed of cat.
    If no breed is specified, returns None.
    If the breed is not found, returns None.
    Args:
        breed (str): The breed of cat to search for.
    """
    if not breed:
        return None
    response = requests.get(f"{BASE_URL}/breeds", headers=HEADERS)
    if response.status_code == 200:
        breeds = response.json()
        if breed:
            for b in breeds:
                if b["name"].lower() == breed.lower():
                    return b["id"]
        else:
            print("Breed not found.")
            return None
    else:
        print("Error fetching breeds:", response.status_code)
        return None


def get_cat_urls(breed=None, number=1) -> list[str]:
    """Gets the requested number of URLs for a random cat image or a cat image of a specific breed.
    If no breed is specified, returns a random cat image.
    If number is not specified, returns one URL.
    If no breed is specified but number is specified, returns the requested number of random cat images.

    Args:
        breed (str): The breed of cat to search for.
        number (int): The number of URLs to return.
    """
    breed_id = get_id(breed)

    if breed_id:
        response = requests.get(f"{BASE_URL}/images/search?breed_ids={breed_id}&limit={number}", headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            return [d["url"] for d in data]

        else:
            print("Error fetching image:", response.status_code)
            return []
    else:
        response = requests.get(f"{BASE_URL}/images/search?limit={number}", headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            return [d["url"] for d in data]
        else:
            print("Error fetching random images:", response.status_code)
            return []

if __name__ == "__main__":
    # Test case 1: Get 10 Bengal cat images
    print("Fetching 10 Bengal cat images...")
    bengal_images = get_cat_urls(breed="Bengal", number=10)
    print("Bengal Cat Images:", bengal_images)

    # Test case 2: Get 5 random cat images
    print("Fetching 5 random cat images...")
    random_images = get_cat_urls(number=5)
    print("Random Cat Images:", random_images)

    # Test case 3: Get images for a breed that doesn't exist
    print("Fetching images for a non-existent breed...")
    unknown_breed_images = get_cat_urls(breed="Unicorn", number=5)
    print("Unknown Breed Cat Images:", unknown_breed_images)

    # Test case 4: Get 1 random cat image
    print("Fetching 1 random cat image...")
    one_random_image = get_cat_urls(number=1)
    print("One Random Cat Image:", one_random_image)

    # Test case 5: Get 1 siamese cat image
    print("Fetching 1 siamese cat image...")
    siamese_image = get_cat_urls(breed="Siamese", number=1)
    print("Siamese Cat Image:", siamese_image)

    # Test case 6: Get id of siamese cat
    print("Fetching id of Siamese cat...")
    siamese_id = get_id(breed="Siamese")
    print("Siamese Cat ID:", siamese_id)


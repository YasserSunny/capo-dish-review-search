from fastapi import FastAPI
from dotenv import load_dotenv
from dish_review_search.gen_ai_modules.ranker import RankerLLM
from dish_review_search.search_modules.rest_review_search import RestReviewSearch
import os
import nltk

if os.path.exists(".env"):
    load_dotenv(override=True)

# Download NLTK data files (if not already downloaded)
nltk.download('punkt')
nltk.download('stopwords')

app = FastAPI()


@app.get("/health")
def status_update():
    return {"status": "ok"}

@app.post("/search")
def search_dish_reviews(dish_name: str, location: str = None):
    """
    Search for reviews of a specific dish.
    """
    # Placeholder for actual search logic
    # In a real application, you would query a database or an external API
    # to get the reviews for the specified dish.
    resturant_search = RestReviewSearch(dish_name, location)
    resturants_review = resturant_search.extract_reviews()

    ranker_result = RankerLLM.get_resturant_ranking(dish_name, resturants_review)
    return {"dish_name": dish_name, "ranking": ranker_result}
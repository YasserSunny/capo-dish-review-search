import googlemaps
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


class RestReviewSearch:
    def __init__(self, dish_name, location):
        self.dish_name = dish_name
        self.location = location
        self.gmaps = googlemaps.Client(key=os.getenv("GOOGLE_MAPS_API_KEY"))

    def _search_restaurants_google(self, radius=5000, max_results=10):
        """Searches for restaurants using Google Maps Places API (Python SDK)."""
        try:
            restaurants = []
            response = self.gmaps.places(
                query=f"{self.dish_name} restaurants in {self.location}",
                radius=radius,
                location=self.location  # Can also provide lat/lng coordinates
            )

            if response['status'] == 'OK':
                restaurants.extend(response.get('results', [])) # Add first page results

                # Handle pagination to get more results if available
                while 'next_page_token' in response and len(restaurants) < max_results:
                    next_page_token = response['next_page_token']
                    # Wait briefly before requesting the next page (required by API)
                    import time
                    time.sleep(2)  # Wait 2 seconds (adjust if needed)

                    response = self.gmaps.places(
                        query=f"{self.dish_name} restaurants in {self.location}",
                        radius=radius,
                        location=self.location,
                        page_token=next_page_token
                    )

                    if response['status'] == 'OK':
                        restaurants.extend(response.get('results', []))
                    else:
                        print(f"Error getting next page: {response['status']} - {response.get('error_message', 'No message')}")
                        break  # Stop if there's an error on a subsequent page

                return restaurants[:max_results]  # Return at most max_results
            else:
                print(f"Error: {response['status']} - {response.get('error_message', 'No message')}")
                return []
        except Exception as e:
            print(f"An error occurred: {e}")
            return []
        
    def _get_place_details(self, place_id, fields=["name", "formatted_address", "rating", "reviews"]):
        """Retrieves details for a specific place using Google Maps Places API (Python SDK)."""
        try:
            response = self.gmaps.place(
                place_id=place_id,
                fields=fields
            )

            if response['status'] == 'OK':
                place_details = response.get('result', {})
                return place_details
            else:
                print(f"Error: {response['status']} - {response.get('error_message', 'No message')}")
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    def _filter_reviews(self,reviews, dish_cuisine, top_n=20):
        """Filters reviews based on relevance to the dish/cuisine using keyword matching."""
        stop_words = set(stopwords.words('english'))
        dish_cuisine_tokens = word_tokenize(dish_cuisine.lower())  # Tokenize the search term
        filtered_reviews = []

        for review in reviews:
            review_text = review['text'].lower()
            review_tokens = word_tokenize(review_text)

            # Remove stop words and check for dish/cuisine keywords
            relevant_words = [w for w in review_tokens if w not in stop_words and w in dish_cuisine_tokens]

            if len(relevant_words) > 0:  # if any relevant word appear in the review, we assume that review is relavant.
                filtered_reviews.append(review_text)

        return filtered_reviews[:top_n]  # Return top N reviews
        
    def extract_reviews(self):
        """Extracts reviews from the Google Maps API for the given dish and location."""
        restaurants = self._search_restaurants_google()
        restaurant_reviews = {}

        for restaurant in restaurants:
            place_id = restaurant.get('place_id')
            if place_id:
                place_details = self._get_place_details(place_id)
                if place_details and 'reviews' in place_details:
                    reviews = place_details['reviews']
                    filtered_reviews = self._filter_reviews(reviews, self.dish_name)
                    restaurant_reviews[restaurant['name']] = filtered_reviews

        return restaurant_reviews
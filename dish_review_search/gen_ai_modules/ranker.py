from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain_google_genai import GoogleGenerativeAI
from dish_review_search.gen_ai_modules.llm_builder import LLMBuilder

class RankerLLM(object):

    @staticmethod
    def get_chat_model():
        # return chat model
        llm: GoogleGenerativeAI = LLMBuilder.build_llm()
        return llm
    
    @staticmethod
    def get_ranker_prompt():
        # return ranker prompt
        return ChatPromptTemplate.from_template(
            '''
            You are an experienced restaurant critic with expertise in analyzing dining establishments and their dishes across various cuisines. You will evaluate a set of restaurant reviews provided in a dictionary format, where each entry contains customer feedback about their dining experiences.

            Task:
            Analyze the reviews for the specified dish_name across multiple restaurants and create a comprehensive ranking from best to worst.

            Input:
            - dish_name: {dish_name} (The specific dish being compared across restaurants)
            - restaurant_reviews_dict: {restaurant_reviews_dict} (A dictionary where keys are restaurant names and values are collections of customer reviews)

            Please provide:
            1. A ranked list of restaurants from best to worst
            2. For each restaurant in the ranking:
            - Restaurant name
            - Ranking position
            - A detailed explanation (2-3 sentences) justifying the ranking, including:
                * Key positive/negative factors from reviews
                * Consistency across reviews
                * Quality indicators mentioned
                * Any notable patterns in customer feedback
            
            Additional considerations:
            - Account for the number of reviews per restaurant
            - Consider the recency of reviews if available
            - Weight specific mentions of the dish more heavily than general restaurant feedback
            - Factor in service and ambiance only as they directly relate to the dish experience
            - Note any potential biases or outliers in the reviews

            Format your response as:
            1. [Restaurant Name]
            Explanation: [Your detailed justification]

            2. [Restaurant Name]
            Explanation: [Your detailed justification]

            [Continue for all restaurants]

            If there are any restaurants with insufficient data to make a fair assessment, please note this separately at the end of your analysis.
            '''
        )
    
    @staticmethod
    def get_resturant_ranking(dish_name, restaurant_reviews_dict):
        ranking_prompt = RankerLLM.get_ranker_prompt()
        llm = RankerLLM.get_chat_model()
        _chain = ranking_prompt | llm | StrOutputParser()
        response = _chain.invoke({
            "dish_name": dish_name,
            "restaurant_reviews_dict": restaurant_reviews_dict
        })
        return response

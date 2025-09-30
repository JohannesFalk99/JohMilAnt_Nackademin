"""
rating.py - Rating class
"""

class Rating:
    def __init__(self, rating_id: int, user_id: int, meal_id: int, rating: int, comment: str):
        self.id = rating_id
        self.user_id = user_id
        self.meal_id = meal_id
        self.rating = rating
        self.comment = comment

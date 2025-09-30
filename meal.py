"""
meal.py - Meal class
"""

class Meal:
    def __init__(self, meal_id: int, name: str, day: str, meal_type: str, allergens: str):
        self.id = meal_id
        self.name = name
        self.day = day
        self.meal_type = meal_type
        self.allergens = allergens

    def __str__(self):
        return f"{self.day} - {self.meal_type}: {self.name} ({self.allergens})"

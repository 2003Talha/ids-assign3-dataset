#!/usr/bin/env python3
"""
recipe_processor.py
Utility functions for processing and managing recipe data.
"""

import re
import json
from typing import List, Dict, Optional


def parse_ingredients(raw_text: str) -> List[Dict]:
    """
    Parse ingredient lines into structured dicts.
    Each ingredient dict contains: amount, unit, name.
    """
    ingredients = []
    lines = raw_text.strip().split("\n")
    pattern = re.compile(r"([\d./]+)?\s*([a-zA-Z]+)?\s+(.+)")
    for line in lines:
        line = line.strip("-").strip()
        match = pattern.match(line)
        if match:
            amount, unit, name = match.groups()
            ingredients.append({"amount": amount or "", "unit": unit or "", "name": name.strip()})
    return ingredients


def filter_by_cuisine(recipes: List[Dict], cuisine: str) -> List[Dict]:
    """
    Filter recipes by cuisine type.
    :param recipes: list of recipe dicts
    :param cuisine: target cuisine string (case-insensitive)
    :return: filtered list
    """
    return [r for r in recipes if r.get("cuisine", "").lower() == cuisine.lower()]


def filter_by_time(recipes: List[Dict], max_minutes: int) -> List[Dict]:
    """
    Filter recipes that can be made within max_minutes total time.
    """
    result = []
    for r in recipes:
        total = r.get("prep_time", 0) + r.get("cook_time", 0)
        if total <= max_minutes:
            result.append(r)
    return result


def filter_by_dietary(recipes: List[Dict], diet: str) -> List[Dict]:
    """
    Filter recipes by dietary restriction (e.g., gluten-free, vegan).
    """
    return [r for r in recipes if diet.lower() in [d.lower() for d in r.get("dietary", [])]]


def exclude_ingredient(recipes: List[Dict], ingredient: str) -> List[Dict]:
    """
    Exclude recipes that contain a specific ingredient.
    Useful for allergy filtering.
    """
    filtered = []
    for r in recipes:
        ing_names = [i["name"].lower() for i in r.get("ingredients", [])]
        if ingredient.lower() not in ing_names:
            filtered.append(r)
    return filtered


def recommend_recipes(recipes: List[Dict], query: Dict) -> List[Dict]:
    """
    Main recommendation function combining multiple filters.
    Query can have: cuisine, max_time, dietary, exclude_ingredient
    """
    results = recipes[:]
    if "cuisine" in query:
        results = filter_by_cuisine(results, query["cuisine"])
    if "max_time" in query:
        results = filter_by_time(results, query["max_time"])
    if "dietary" in query:
        results = filter_by_dietary(results, query["dietary"])
    if "exclude" in query:
        results = exclude_ingredient(results, query["exclude"])
    return results


def recipe_to_json(recipe: Dict) -> str:
    """Serialize a recipe dict to a JSON string."""
    return json.dumps(recipe, indent=2)


if __name__ == "__main__":
    sample = [
        {"name": "Margherita Pizza", "cuisine": "Italian", "prep_time": 15, "cook_time": 12,
         "dietary": ["vegetarian"], "ingredients": [{"name": "mozzarella"}, {"name": "tomato"}]},
        {"name": "Banana Bread", "cuisine": "American", "prep_time": 10, "cook_time": 55,
         "dietary": ["gluten-free"], "ingredients": [{"name": "banana"}, {"name": "almond flour"}]},
    ]
    print("Filtered by cuisine 'Italian':", filter_by_cuisine(sample, "Italian"))
    print("Filtered by max_time 30 min:", filter_by_time(sample, 30))

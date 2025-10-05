"""
Open Food Facts API Integration
Hämtar livsmedelsdata från Open Food Facts och TheMealDB
Implementerar extern data-hämtning enligt kurskrav med requests och json modulerna
"""

import requests
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import random

class FoodAPI:
    """API-klass för att hämta livsmedelsdata från Open Food Facts och TheMealDB"""
    
    def __init__(self) -> None:
        self.openfoodfacts_url: str = "https://world.openfoodfacts.org"
        self.themealdb_url: str = "https://www.themealdb.com/api/json/v1/1"
        self.headers: Dict[str, str] = {
            'User-Agent': 'SchoolLunchSystem/1.0 (Educational Project)',
            'Accept': 'application/json'
        }
    
    def search_food_products(self, search_term: str, page_size: int = 10) -> Dict[str, Any]:
        """
        Sök livsmedel via Open Food Facts API
        
        Args:
            search_term: Sökterm (t.ex. "pasta", "kyckling", "potatis")
            page_size: Antal produkter att hämta
            
        Returns:
            Dict med produkter eller felmeddelande
        """
        try:
            url = f"{self.openfoodfacts_url}/cgi/search.pl"
            params = {
                'search_terms': search_term,
                'json': 1,
                'page_size': page_size,
                'fields': 'product_name,brands,categories,ingredients_text,allergens,nutrition_grades,energy_100g,sugars_100g,fat_100g,proteins_100g,salt_100g'
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            return data
            
        except requests.exceptions.RequestException as e:
            return {"error": f"Kunde inte söka livsmedel: {e}"}
        except json.JSONDecodeError:
            return {"error": "Ogiltigt JSON-svar från Open Food Facts"}
    
    def get_product_by_barcode(self, barcode: str) -> Dict[str, Any]:
        """
        Hämta specifik produkt via streckkod
        
        Args:
            barcode: Produktens streckkod
            
        Returns:
            Dict med produktinformation
        """
        try:
            url = f"{self.openfoodfacts_url}/api/v0/product/{barcode}.json"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return {"error": f"Kunde inte hämta produkt: {e}"}
        except json.JSONDecodeError:
            return {"error": "Ogiltigt JSON-svar"}
    
    def get_random_meals_themealdb(self, count: int = 5) -> Dict[str, Any]:
        """
        Hämta slumpmässiga måltider från TheMealDB som komplement
        
        Args:
            count: Antal måltider att hämta
            
        Returns:
            Dict med måltider eller felmeddelande
        """
        meals = []
        errors = []
        
        for i in range(count):
            try:
                url = f"{self.themealdb_url}/random.php"
                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                if data and 'meals' in data and data['meals']:
                    meals.extend(data['meals'])
                
            except requests.exceptions.RequestException as e:
                errors.append(f"TheMealDB anrop {i+1}: {str(e)}")
            except json.JSONDecodeError:
                errors.append(f"TheMealDB anrop {i+1}: Ogiltigt JSON-svar")
        
        return {
            "meals": meals,
            "count": len(meals),
            "errors": errors if errors else None
        }
    
    def convert_openfoodfacts_to_local(self, openfood_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Konvertera Open Food Facts data till vårt lokala format
        
        Args:
            openfood_data: Rådata från Open Food Facts API
            
        Returns:
            List med måltider i vårt format
        """
        local_meals = []
        
        if "error" in openfood_data:
            return local_meals
        
        products = openfood_data.get('products', [])
        if not products:
            return local_meals
        
        for product in products:
            # Extrahera produktinformation
            name = product.get('product_name', 'Okänd produkt')
            if not name or name == 'Okänd produkt':
                continue
                
            # Skapa beskrivning från ingredienser
            ingredients = product.get('ingredients_text', '')
            description = ingredients[:150] + "..." if len(ingredients) > 150 else ingredients
            if not description:
                description = f"Livsmedel: {name}"
            
            # Beräkna pris baserat på näringsinnehåll och kategori
            estimated_price = self._estimate_price_from_nutrition(product)
            
            # Kategorisera baserat på Open Food Facts kategorier
            category = self._categorize_from_openfoodfacts(product)
            
            local_meal = {
                "name": name,
                "description": description,
                "price": estimated_price,
                "category": category,
                "source": "Open Food Facts",
                "allergens": product.get('allergens', ''),
                "nutrition_grade": self._get_nutrition_grade_description(product.get('nutrition_grades', 'N/A')),
                "energy_100g": product.get('energy_100g', 0)
            }
            
            local_meals.append(local_meal)
        
        return local_meals
    
    def _estimate_price_from_nutrition(self, product: Dict[str, Any]) -> float:
        """
        Uppskatta pris baserat på näringsinnehåll och produkttyp med match-case
        Demonstrerar Python 3.10+ pattern matching funktionalitet
        """
        base_price = 25.0
        
        # Hämta och konvertera protein-värde säkert
        proteins_raw = product.get('proteins_100g', 0)
        try:
            proteins = float(proteins_raw) if proteins_raw else 0
        except (ValueError, TypeError):
            proteins = 0.0
            
        # Använd match-case för proteininnehållskategorisering  
        match proteins:
            case p if p > 20:
                protein_bonus = 20.0  # Mycket högt protein (kött, fisk)
            case p if p > 15:
                protein_bonus = 15.0  # Högt protein
            case p if p > 8:
                protein_bonus = 8.0   # Medel protein
            case p if p > 3:
                protein_bonus = 3.0   # Lågt protein
            case _:
                protein_bonus = 0.0   # Mycket lågt/okänt protein
        
        # Kategorisera produkttyp med match-case
        categories = product.get('categories', '').lower()
        category_bonus = self._get_category_price_bonus(categories)
            
        return round(base_price + protein_bonus + category_bonus, 2)
    
    def _get_category_price_bonus(self, categories: str) -> float:
        """Beräkna prisbonus baserat på produktkategori med match-case"""
        # Använd match-case för kategoriprishantering
        match categories:
            case cat if any(word in cat for word in ['kött', 'meat', 'beef', 'pork', 'lamb']):
                return 25.0  # Kött - dyrast
            case cat if any(word in cat for word in ['fisk', 'fish', 'seafood', 'salmon']):
                return 22.0  # Fisk & skaldjur
            case cat if any(word in cat for word in ['chicken', 'kyckling', 'poultry']):
                return 18.0  # Kyckling - billigare än rött kött
            case cat if 'organic' in cat or 'ekologisk' in cat:
                return 12.0  # Ekologiskt - premium men inte kött
            case cat if any(word in cat for word in ['cheese', 'ost', 'dairy']):
                return 10.0  # Mejeriprodukter
            case cat if any(word in cat for word in ['pasta', 'bread', 'cereals']):
                return 5.0   # Kolhydrater - basvaror
            case _:
                return 0.0   # Okänd kategori - ingen bonus
    
    def _get_nutrition_grade_description(self, grade: str) -> str:
        """
        Konvertera nutrition grade till svensk beskrivning med match-case
        Open Food Facts använder A-E skala där A är bäst
        """
        normalized_grade = grade.upper().strip() if grade else 'N/A'
        
        # Använd match-case för nutrition grade översättning
        match normalized_grade:
            case 'A':
                return 'a'  # Mycket bra näringsinnehåll
            case 'B':
                return 'b'  # Bra näringsinnehåll  
            case 'C':
                return 'c'  # Acceptabelt näringsinnehåll
            case 'D':
                return 'd'  # Dåligt näringsinnehåll
            case 'E':
                return 'e'  # Mycket dåligt näringsinnehåll
            case 'N/A' | '' | None:
                return 'okänt'  # Okänt näringsinnehåll
            case _:
                return f'{normalized_grade.lower()}'  # Fallback för okända grades
    
    def _categorize_from_openfoodfacts(self, product: Dict[str, Any]) -> str:
        """Kategorisera produkt baserat på Open Food Facts kategorier"""
        categories = product.get('categories', '').lower()
        name = product.get('product_name', '').lower()
        
        # Svensk kategorisering
        if any(word in categories + name for word in ['kött', 'meat', 'beef', 'pork']):
            return 'Kött'
        elif any(word in categories + name for word in ['fisk', 'fish', 'seafood']):
            return 'Fisk & Skaldjur'  
        elif any(word in categories + name for word in ['chicken', 'kyckling', 'poultry']):
            return 'Kyckling'
        elif any(word in categories + name for word in ['vegetarian', 'vegetarisk', 'vegan', 'vegansk']):
            return 'Vegetariskt'
        elif any(word in categories + name for word in ['pasta', 'noodles']):
            return 'Pasta'
        elif any(word in categories + name for word in ['soup', 'soppa']):
            return 'Soppa'
        elif any(word in categories + name for word in ['dessert', 'efterrätt', 'sweet']):
            return 'Efterrätt'
        else:
            return 'Huvudrätt'
    
    def convert_themealdb_to_local(self, mealdb_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Konvertera TheMealDB data till vårt lokala format
        """
        local_meals = []
        
        if "error" in mealdb_data:
            return local_meals
        
        meals_data = mealdb_data.get('meals', [])
        if not meals_data:
            return local_meals
        
        for meal in meals_data:
            name = meal.get('strMeal', 'Okänd rätt')
            description = meal.get('strInstructions', name)[:200] + "..." if meal.get('strInstructions') else name
            
            # Översätt från engelska kategorier  
            category_english = meal.get('strCategory', 'Main')
            category_swedish = self._translate_category(category_english)
            
            # Uppskatta pris baserat på ingredienser
            estimated_price = self._estimate_price_from_themeal_ingredients(meal)
            
            local_meal = {
                "name": name,
                "description": description,
                "price": estimated_price,
                "category": category_swedish,
                "source": "TheMealDB"
            }
            
            local_meals.append(local_meal)
        
        return local_meals
    
    def _translate_category(self, english_category: str) -> str:
        """Översätt engelska kategorier till svenska"""
        translations = {
            'Beef': 'Nötkött',
            'Chicken': 'Kyckling', 
            'Dessert': 'Efterrätt',
            'Lamb': 'Lammkött',
            'Miscellaneous': 'Blandat',
            'Pasta': 'Pasta',
            'Pork': 'Fläskkött',
            'Seafood': 'Fisk & Skaldjur',
            'Side': 'Tillbehör',
            'Starter': 'Förrätter',
            'Vegan': 'Vegansk',
            'Vegetarian': 'Vegetarisk',
            'Breakfast': 'Frukost'
        }
        return translations.get(english_category, 'Huvudrätt')
    
    def _estimate_price_from_themeal_ingredients(self, meal: Dict[str, Any]) -> float:
        """Uppskatta pris baserat på ingredienser från TheMealDB"""
        # Räkna antal ingredienser
        ingredient_count = 0
        for i in range(1, 21):
            ingredient_key = f'strIngredient{i}'
            if meal.get(ingredient_key) and meal[ingredient_key].strip():
                ingredient_count += 1
        
        # Basera pris på komplexitet
        base_price = 35.0
        if ingredient_count > 15:
            return base_price + 15.0
        elif ingredient_count > 10:
            return base_price + 10.0
        elif ingredient_count > 5:
            return base_price + 5.0
        else:
            return base_price
    
    def convert_themealdb_to_local(self, mealdb_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Konvertera TheMealDB data till vårt lokala format
        
        Args:
            mealdb_data: Rådata från TheMealDB API
            
        Returns:
            List med måltider i vårt format
        """
        local_meals = []
        
        if "error" in mealdb_data:
            return local_meals
        
        # Hantera TheMealDB struktur
        meals_data = mealdb_data.get('meals', [])
        if not meals_data:
            return local_meals
        
        for meal in meals_data:
            # Extrahera data från TheMealDB format
            name = meal.get('strMeal', 'Okänd rätt')
            description = meal.get('strInstructions', name)[:200] + "..." if meal.get('strInstructions') else name
            
            # Översätt från engelska kategorier
            category_english = meal.get('strCategory', 'Main')
            category_swedish = self._translate_category(category_english)
            
            # Uppskatta pris baserat på ingredienser
            estimated_price = self._estimate_price_from_ingredients(meal)
            
            local_meal = {
                "name": name,
                "description": description,
                "price": estimated_price,
                "category": category_swedish,
                "source": "TheMealDB"
            }
            
            local_meals.append(local_meal)
        
        return local_meals
    
    def _translate_category(self, english_category: str) -> str:
        """Översätt engelska kategorier till svenska"""
        translations = {
            'Beef': 'Nötkött',
            'Chicken': 'Kyckling', 
            'Dessert': 'Efterrätt',
            'Lamb': 'Lammkött',
            'Miscellaneous': 'Blandat',
            'Pasta': 'Pasta',
            'Pork': 'Fläskkött',
            'Seafood': 'Fisk & Skaldjur',
            'Side': 'Tillbehör',
            'Starter': 'Förrätter',
            'Vegan': 'Vegansk',
            'Vegetarian': 'Vegetarisk',
            'Breakfast': 'Frukost',
            'Goat': 'Getkött'
        }
        return translations.get(english_category, 'Huvudrätt')
    
    def _estimate_price_from_ingredients(self, meal: Dict[str, Any]) -> float:
        """Uppskatta pris baserat på ingredienser från TheMealDB"""
        # Räkna antal ingredienser för att uppskatta komplexitet
        ingredient_count = 0
        for i in range(1, 21):  # TheMealDB har upp till 20 ingredienser
            ingredient_key = f'strIngredient{i}'
            if meal.get(ingredient_key) and meal[ingredient_key].strip():
                ingredient_count += 1
        
        # Basera pris på komplexitet
        base_price = 35.0
        if ingredient_count > 15:
            return base_price + 15.0  # Komplicerad rätt
        elif ingredient_count > 10:
            return base_price + 10.0  # Medel komplicerad
        elif ingredient_count > 5:
            return base_price + 5.0   # Enkel
        else:
            return base_price         # Mycket enkel
    
# Hjälpfunktioner för enkel användning
def search_food_ingredients(search_term: str = "pasta") -> List[Dict[str, Any]]:
    """
    Sök livsmedel från Open Food Facts (ENDAST PRODUKTER - INGA RECEPT)
    Huvudfunktion för att hämta extern data enligt kurskrav
    """
    api = FoodAPI()
    
    # Hämta produkter från Open Food Facts
    result = api.search_food_products(search_term, page_size=10)
    
    if "error" in result or not result.get('products'):
        return []
    
    # Konvertera till vårt format och filtrera bort recept-liknande innehåll
    meals = api.convert_openfoodfacts_to_local(result)
    
    # Extra filter för att garantera att inga recept kommer med
    product_meals = []
    for meal in meals:
        desc = meal.get('description', '').lower()
        name = meal.get('name', '').lower()
        
        # Skippa om det verkar vara instruktioner eller recept
        recipe_indicators = ['step', 'cook for', 'preheat', 'mix in', 'add the', 'heat the', 'bake for', 'fry for']
        is_recipe = any(indicator in desc for indicator in recipe_indicators)
        
        if not is_recipe:
            product_meals.append(meal)
    
    return product_meals

def fetch_random_recipes(count: int = 3) -> List[Dict[str, Any]]:
    """
    Hämta slumpmässiga recept från TheMealDB som komplement
    """
    api = FoodAPI()
    
    # Hämta recept från TheMealDB
    result = api.get_random_meals_themealdb(count)
    
    if "error" in result or not result.get('meals'):
        return []
    
    # Konvertera till vårt format (vi behöver implementera denna)
    return api.convert_themealdb_to_local({"meals": result['meals']})

def get_product_info_by_barcode(barcode: str) -> Dict[str, Any]:
    """
    Hämta detaljerad produktinformation via streckkod
    """
    api = FoodAPI()
    
    result = api.get_product_by_barcode(barcode)
    
    if "error" in result:
        return result
    
    # Returnera produktinformation
    product = result.get('product', {})
    return {
        "name": product.get('product_name', 'Okänd'),
        "ingredients": product.get('ingredients_text', ''),
        "allergens": product.get('allergens', ''),
        "nutrition_grade": product.get('nutrition_grades', 'N/A'),
        "categories": product.get('categories', '')
    }

if __name__ == "__main__":
    # Test av API:et
    print("🍽️ Testar Open Food Facts API + TheMealDB...")
    
    # Test 1: Sök livsmedel på Open Food Facts
    print("\n📋 Test 1: Söker 'pasta' på Open Food Facts")
    pasta_products = search_food_ingredients("pasta")
    
    if pasta_products:
        print(f"✅ Hittade {len(pasta_products)} pasta-produkter:")
        for product in pasta_products[:3]:  # Visa första 3
            allergens = product.get('allergens', 'Inga kända')
            nutrition = product.get('nutrition_grade', 'N/A')
            print(f"  - {product['name']} ({product['price']}kr)")
            print(f"    Kategori: {product['category']}, Näring: {nutrition}")
    else:
        print("❌ Kunde inte hämta pasta-produkter")
    
    # Test 2: Sök kött-produkter
    print("\n📋 Test 2: Söker 'chicken' på Open Food Facts")
    chicken_products = search_food_ingredients("chicken")
    
    if chicken_products:
        print(f"✅ Hittade {len(chicken_products)} kyckling-produkter:")
        for product in chicken_products[:2]:  # Visa första 2
            print(f"  - {product['name']} ({product['price']}kr) - {product['category']}")
    else:
        print("❌ Kunde inte hämta kyckling-produkter")
    
    # Test 3: RECEPT-TEST AVAKTIVERAD (enligt användarens begäran)
    print("\n📋 Test 3: Recept-funktionalitet avaktiverad")
    print("✅ Använder endast Open Food Facts produkter (inga recept)")
    # random_recipes = fetch_random_recipes(2)  # Avaktiverad
    
    # Test 4: Test specifik streckkod (Barilla pasta som exempel)
    print("\n📋 Test 4: Hämtar produkt med streckkod")
    barcode_info = get_product_info_by_barcode("8076809513197")  # Exempel streckkod
    
    if "error" not in barcode_info and barcode_info.get('name'):
        print(f"✅ Produkt hittad: {barcode_info['name']}")
        if barcode_info.get('allergens'):
            print(f"    Allergener: {barcode_info['allergens']}")
    else:
        print("❌ Kunde inte hämta produkt via streckkod (normalt för test)")

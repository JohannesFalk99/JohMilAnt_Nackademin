#!/usr/bin/env python3
"""
Test av Skolmaten.se API integration
Verifierar att API-anropen fungerar och data kan importeras
"""

import sys
import os

# Lägg till projektets root-katalog till Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from skolmaten_api import FoodAPI, search_food_ingredients
from lunch_system_database import SchoolLunchDB

def test_api_connection():
    """Test grundläggande API-anslutning till Open Food Facts"""
    print("🔗 Testar API-anslutning till Open Food Facts...")
    
    try:
        api = FoodAPI()
        result = api.search_food_products("pasta", page_size=3)
        
        if "error" in result:
            print(f"❌ API-fel: {result['error']}")
            return False
        
        products = result.get('products', [])
        print(f"✅ Hittade {len(products)} produkter för 'pasta'")
        
        if products:
            first_product = products[0]
            print(f"   Första produkten: {first_product.get('product_name', 'Okänt namn')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Anslutningsfel: {e}")
        return False

def test_food_search():
    """Test hämtning av livsmedel"""
    print("\n🍽️  Testar sökning av livsmedel...")
    
    try:
        meals = search_food_ingredients("chicken")
        
        if not meals:
            print("❌ Inga livsmedel kunde hämtas")
            return False
        
        print(f"✅ Hämtade {len(meals)} livsmedel")
        
        # Visa första 3 produkter
        for i, meal in enumerate(meals[:3], 1):
            nutrition = meal.get('nutrition_grade', 'N/A')
            print(f"   {i}. {meal['name']} - {meal['price']}kr ({meal['category']}) [Näring: {nutrition}]")
        
        return True
        
    except Exception as e:
        print(f"❌ Fel vid hämtning: {e}")
        return False

def test_database_import():
    """Test import till databas"""
    print("\n💾 Testar import till databas...")
    
    try:
        # Kontrollera om databas finns
        if not os.path.exists('test.db'):
            print("❌ Ingen test.db hittades. Kör 'python create_sample_database.py' först")
            return False
        
        # Skapa databasanslutning
        db = SchoolLunchDB('test.db')
        
        # Räkna måltider före import
        meals_before = db.get_all_meals()
        count_before = len(meals_before) if meals_before else 0
        
        # Importera från Open Food Facts
        result = db.import_meals_from_openfoodfacts("pasta")
        
        if "error" in result:
            print(f"❌ Import-fel: {result['error']}")
            return False
        
        # Räkna måltider efter import  
        meals_after = db.get_all_meals()
        count_after = len(meals_after) if meals_after else 0
        
        print(f"✅ Import slutförd!")
        print(f"   Sökterm: {result.get('search_term', 'pasta')}")
        print(f"   Källor: {result.get('sources', 'API')}")
        print(f"   Måltider före: {count_before}")
        print(f"   Måltider efter: {count_after}")
        print(f"   Nya måltider: {result.get('added', 0)}")
        print(f"   Hoppade över: {result.get('skipped', 0)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Databasfel: {e}")
        return False

def main():
    """Huvudfunktion för tester"""
    print("🧪 TESTAR OPEN FOOD FACTS API INTEGRATION")
    print("=" * 50)
    
    tests = [
        ("API-anslutning", test_api_connection),
        ("Livsmedels-sökning", test_food_search),
        ("Databas-import", test_database_import)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Test: {test_name}")
        if test_func():
            passed += 1
        else:
            print(f"💥 Test '{test_name}' misslyckades")
    
    print(f"\n📊 RESULTAT: {passed}/{total} tester lyckades")
    
    if passed == total:
        print("🎉 Alla tester lyckades! API:et är redo att användas.")
    else:
        print("⚠️  Vissa tester misslyckades. Kontrollera internetanslutning och beroenden.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

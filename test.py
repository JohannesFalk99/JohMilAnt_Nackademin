import sqlite3

def visa_meny() -> None:
    print("\n=== LUNCHSYSTEM MENY ===")
    print("1. Visa elever")
    print("2. Visa mat")  
    print("3. Visa detaljerad måltidsinformation")
    print("4. Statistik")
    print("5. Hämta PRODUKTER från Open Food Facts API (INGA RECEPT)")
    print("6. Avsluta")


def visa_elever() -> None:
    conn = sqlite3.connect('test.db')
    for rad in conn.execute("SELECT name, class, allergies FROM students"):
        print(f"{rad[0]} - {rad[1]} ({rad[2]})")

    conn.close()


def visa_mat() -> None:
    conn = sqlite3.connect('test.db')
    for rad in conn.execute("SELECT name, price, rating FROM meals"):
        print(f"{rad[0]} - {rad[1]}kr ⭐{round(rad[2], 1)}")
        
    conn.close()


def visa_detaljerad_mat() -> None:
    """Visa all detaljerad information om måltider från API"""
    conn = sqlite3.connect('test.db')
    
    print("\n🍽️ === DETALJERAD MÅLTIDSINFORMATION ===")
    print("=" * 60)
    
    # Hämta alla måltider med tillgänglig information
    query = """
    SELECT id, name, category, price, rating, description, 
           rating_count, created_at
    FROM meals 
    ORDER BY created_at DESC, name
    """
    
    meal_count = 0
    
    for rad in conn.execute(query):
        id_val, name, category, price, rating, description, rating_count, created_at = rad
        
        meal_count += 1
        print(f"\n🍽️  #{meal_count} {name}")
        print(f"   🆔 ID: {id_val}")
        print(f"   📂 Kategori: {category or 'Okänd'}")
        print(f"   💰 Pris: {price}kr")
        print(f"   ⭐ Betyg: {round(rating, 1)}/5 ({rating_count} röster)")
        print(f"   📅 Skapad: {created_at}")
        
        if description and description.strip():
            desc_short = description[:100] + "..." if len(description) > 100 else description
            print(f"   📝 Beskrivning: {desc_short}")
        
        print("   " + "─" * 40)
    
    if meal_count == 0:
        print("❌ Inga måltider hittades i databasen")
    else:
        print(f"\n📊 Totalt: {meal_count} måltider i databasen")
    
    conn.close()


def visa_statistik() -> None:
    conn = sqlite3.connect('test.db')
    elever = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    mat = conn.execute("SELECT COUNT(*) FROM meals").fetchone()[0]
    transaktioner = conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
    print(f"📊 Statistik:")
    print(f"  Elever: {elever}")
    print(f"  Maträtter: {mat}")
    print(f"  Transaktioner: {transaktioner}")

    conn.close()

def hamta_fran_api() -> None:
    """Hämta och importera ENDAST PRODUKTER från Open Food Facts API (inga recept)"""
    try:
        from lunch_system_database import SchoolLunchDB
        
        print("\n🥫 Hämtar PRODUKTER från Open Food Facts...")
        print("📝 OBS: Endast livsmedelsproduktser hämtas - INGA RECEPT")
        
        # Be användaren om sökterm
        sokterm = input("Ange livsmedel att söka efter (tryck Enter för 'pasta'): ").strip()
        if not sokterm:
            sokterm = "pasta"
        
        print(f"🔍 Söker efter produkter: {sokterm}")
        
        # Skapa databasanslutning
        db = SchoolLunchDB('test.db')
        
        # Importera ENDAST produkter från Open Food Facts
        result = db.import_meals_from_openfoodfacts(sokterm)
        
        if "error" in result:
            print(f"❌ Fel: {result['error']}")
        else:
            print(f"✅ Framgångsrikt!")
            print(f"  Sökterm: {result['search_term']}")
            print(f"  Datakällor: {result['sources']}")
            print(f"  Nya produkter: {result['added']}")
            print(f"  Hoppade över: {result['skipped']}")
            print(f"  Totalt funna: {result['total_found']}")
            
            if "errors" in result:
                print(f"  Varningar: {len(result['errors'])}")
        
    except ImportError as e:
        print(f"❌ Kunde inte importera API-moduler: {e}")
    except Exception as e:
        print(f"❌ Oväntat fel: {e}")

    

def main() -> None:
    while True:
        visa_meny()
        val: str = input("\nAnge ditt val (1-6): ")
        if val == "1": 
            visa_elever()
        elif val == "2": 
            visa_mat()
        elif val == "3": 
            visa_detaljerad_mat()
        elif val == "4": 
            visa_statistik()
        elif val == "5": 
            hamta_fran_api()
        elif val == "6": 
            print("👋 Hej då!")
            break
        else:
            print("❌ Ogiltigt val. Välj 1-6.")

if __name__ == "__main__":
    main()
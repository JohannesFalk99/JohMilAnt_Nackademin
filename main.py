"""
Lunchsystem - Huvudstartfil (main.py)
=====================================

Detta är huvudstartfilen för lunchsystemet enligt kurskrav.
Programmet använder match-case statements (Python 3.10+) för menyhantering.

Författare: Johan Milovanovic, Antonia Henriksson
Kurs: Nackademin - Programmering i Python
"""

from typing import NoReturn
import sys
import subprocess
import os

# Add current directory to path to ensure we import our local test.py
if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import from our local test module
import admin_menu as admin_cli
visa_elever = admin_cli.visa_elever
visa_mat = admin_cli.visa_mat  
visa_detaljerad_mat = admin_cli.visa_detaljerad_mat
visa_statistik = admin_cli.visa_statistik
hamta_fran_api = admin_cli.hamta_fran_api


def visa_huvudmeny() -> None:
    """Visar huvudmenyn för lunchsystemet"""
    print("\n🍽️  === SKOLANS LUNCHSYSTEM ===")
    print("1. 👥 Visa elever")
    print("2. 🍕 Visa mat")
    print("3. 📋 Detaljerad måltidsinformation")
    print("4. 📊 Statistik")
    print("5. 🌐 Hämta data från API")
    print("6. 🌍 Starta Web Server")
    print("7. ❌ Avsluta")
    print("═" * 30)


def starta_web_server() -> None:
    """Startar Flask web servern"""
    try:
        print("\n🌍 === STARTAR WEB SERVER ===")
        print("🚀 Startar Flask server på http://127.0.0.1:5000")
        print("💡 Tryck Ctrl+C för att stoppa servern och återgå till menyn")
        print("⏳ Startar...")
        
        # Starta Flask servern
        web_server_path = os.path.join("web_interface", "flask_server.py")
        
        if not os.path.exists(web_server_path):
            print(f"❌ Kunde inte hitta {web_server_path}")
            return
            
        # Kör Flask servern som subprocess
        subprocess.run([sys.executable, web_server_path], check=False)
        
        print("\n✅ Web servern stoppades")
        print("🔙 Återgår till huvudmenyn...")
        
    except KeyboardInterrupt:
        print("\n\n⚡ Web servern stoppades av användaren")
        print("🔙 Återgår till huvudmenyn...")
    except Exception as e:
        print(f"\n❌ Fel vid start av web server: {e}")


def hantera_menyval(val: str) -> bool:
    """
    Hanterar användarens menyval med match-case statements.
    
    Args:
        val: Användarens val som sträng
        
    Returns:
        bool: True om programmet ska fortsätta, False om det ska avslutas
    """
    match val.strip():
        case "1":
            print("\n👥 === VISA ELEVER ===")
            visa_elever()
            return True
            
        case "2":
            print("\n🍕 === VISA MATRÄTTER ===") 
            visa_mat()
            return True
            
        case "3":
            print("\n📋 === DETALJERAD MÅLTIDSINFORMATION ===")
            visa_detaljerad_mat()
            return True
            
        case "4":
            print("\n📊 === STATISTIK ===")
            visa_statistik()
            return True
            
        case "5":
            print("\n🌐 === HÄMTA FRÅN API ===")
            hamta_fran_api()
            return True
            
        case "6":
            print("\n🌍 === STARTA WEB SERVER ===")
            starta_web_server()
            return True
            
        case "7":
            print("\n👋 Tack för att du använt lunchsystemet!")
            print("🔒 Stänger ner programmet...")
            return False
            
        case _:  # Default case för ogiltiga val
            print(f"\n❌ Ogiltigt val: '{val}'")
            print("💡 Välj ett nummer mellan 1-7")
            return True




def main() -> NoReturn:
    """
    Huvudfunktionen som startar lunchsystemet.
    Implementerar en evighetsloop med match-case för menyhantering.
    """
    print("🚀 Startar Skolans Lunchsystem...")
   
    try:
        while True:
            visa_huvudmeny()
            
            try:
                användarval = input("\n➤ Ange ditt val (1-7): ")
                
                # Använd match-case för menyhantering
                if not hantera_menyval(användarval):
                    break  # Användaren valde att avsluta (val 7)
                    
            except KeyboardInterrupt:
                print("\n\n⚡ Programmet avbröts med Ctrl+C")
                print("👋 Hej då!")
                break
                
            except EOFError:
                print("\n\n📄 EOF upptäckt - avslutar program")
                break
                
    except Exception as e:
        print(f"\n💥 Oväntat fel i huvudprogrammet: {e}")
        print("🔍 Kontakta systemadministratör om problemet kvarstår")
        sys.exit(1)
    
    print("\n✅ Lunchsystemet avslutat korrekt")
    sys.exit(0)


if __name__ == "__main__":
    # Detta är programmets ingångspunkt enligt kurskrav
    # "Programmet skall startas från main.py"
    main()

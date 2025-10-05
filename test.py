import sqlite3

def visa_meny() -> None:
    print("\n1. Elever 2. Mat 3. Statistik 4. Avsluta")


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


def visa_statistik() -> None:
    conn = sqlite3.connect('test.db')
    elever = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    mat = conn.execute("SELECT COUNT(*) FROM meals").fetchone()[0]
    print(f"Elever: {elever}, Maträtter: {mat}")

    conn.close()

    

def main() -> None:
    while True:
        visa_meny()
        val: str = input("Val: ")
        if val == "1": visa_elever()
        elif val == "2": visa_mat()
        elif val == "3": visa_statistik()
        elif val == "4": break

if __name__ == "__main__":
    main()
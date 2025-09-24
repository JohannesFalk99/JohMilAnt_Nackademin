#!/usr/bin/env python3
import os
import tempfile
from database import DatabaseHandler

def testa_database_py_funktioner():
    # Skapa testdatabas
    test_db_path = "test_database1.db"
    db = None
    try:
        db = DatabaseHandler(test_db_path)
        # Lägg till poster
        alice_id = db.add_record({"name": "Donald Duck", "value": "10", "example_field": "Duck"})
        bob_id = db.add_record({"name": "Bob Odenkirk", "value": "999"})
        charlie_id = db.add_record({"name": "Charlie Sheen", "value": "0", "example_field": "Tiger blood"})
        # Hämta post
        print(db.get_record(alice_id))
        print(db.get_record(999))
        # Hämta alla
        print(db.get_all_records())
        # Uppdatera
        print(db.update_record(alice_id, {"value": "69", "example_field": "dead senior dev"}))
        print(db.get_record(alice_id))
        # Sök
        print(db.search_records("Alice"))
        print(db.search_records("dev"))
        # Räkna
        print(db.get_record_count())
        # Ta bort
        print(db.delete_record(bob_id))
        print(db.get_record_count())
        # Edge cases
        print(db.search_records(""))
        print(db.update_record(999, {"name": "fail"}))
        print(db.delete_record(999))
        print(db.update_record(alice_id, {}))
        # SQL injection test
        malicious_id = db.add_record({
            "name": "'; DROP TABLE records; --",
            "value": "1; DELETE FROM records; --"
        })
        print(malicious_id)
        print(db.get_record_count())
        # Slutresultat
        print(db.get_all_records())
        
        # EXTRA TESTS - Let's try more stuff!
        print("\n=== TRYING MORE STUFF ===")
        
        # Test with special characters and unicode
        special_id = db.add_record({
            "name": "åäö ÅÄÖ éèê çñü 中文 🚀",
            "value": "∞",
            "example_field": "Special chars & émojis! @#$%^&*()"
        })
        print(f"Special chars record: {special_id}")
        
        # Test with very long strings
        long_text = "A" * 1000
        long_id = db.add_record({
            "name": long_text,
            "value": "Long text test",
            "example_field": "This is a very long field " * 50
        })
        print(f"Long text record: {long_id}")
        
        # Test with numbers as strings vs actual data
        numbers_id = db.add_record({
            "name": "Number Test",
            "value": "42.5",
            "example_field": "3.14159"
        })
        print(f"Numbers record: {numbers_id}")
        
        # Test bulk operations
        print(f"\n--- BULK OPERATIONS ---")
        bulk_ids = []
        for i in range(10):
            bulk_id = db.add_record({
                "name": f"Bulk User {i}",
                "value": str(i * 10),
                "example_field": f"Category {i % 3}"
            })
            bulk_ids.append(bulk_id)
        print(f"Added 10 bulk records: {bulk_ids}")
        
        # Search tests
        print(f"\n--- SEARCH TESTS ---")
        category_results = db.search_records("Category 1")
        print(f"Category 1 results: {len(category_results)}")
        
        bulk_results = db.search_records("Bulk")
        print(f"'Bulk' search results: {len(bulk_results)}")
        
        unicode_results = db.search_records("åäö")
        print(f"Unicode search results: {len(unicode_results)}")
        
        # Test updating non-existent fields
        print(f"\n--- UPDATE TESTS ---")
        # Only update valid fields
        update_result = db.update_record(special_id, {
            "value": "Updated special value",
            "example_field": "Updated field"
        })
        print(f"Update with valid fields: {update_result}")
        
        # Try to update with mixed valid/invalid (will cause error, but that's expected)
        print("Testing invalid column handling...")
        try:
            invalid_update = db.update_record(special_id, {
                "invalid_field": "This should fail",
                "value": "This won't be applied"
            })
            print(f"Invalid update result: {invalid_update}")
        except Exception as e:
            print(f"Expected error with invalid field: {type(e).__name__}")
            # Recover by doing a valid update
            db.update_record(special_id, {"value": "Recovered after error"})
        
        # Mass delete test
        print(f"\n--- MASS DELETE ---")
        deleted_count = 0
        for bulk_id in bulk_ids[:5]:  # Delete first 5 bulk records
            if db.delete_record(bulk_id):
                deleted_count += 1
        print(f"Deleted {deleted_count} bulk records")
        
        # Final count and state
        final_count = db.get_record_count()
        print(f"Final record count: {final_count}")
        
        # Test empty database operations
        print(f"\n--- STRESS TEST ---")
        # Add and immediately delete records
        stress_ids = []
        for i in range(50):
            stress_id = db.add_record({
                "name": f"Stress {i}",
                "value": str(i),
                "example_field": "temp"
            })
            stress_ids.append(stress_id)
            
            # Delete every other one immediately
            if i % 2 == 0:
                db.delete_record(stress_id)
        
        stress_final = db.get_record_count()
        print(f"After stress test: {stress_final} records")
        
        # Search for everything
        all_search = db.search_records("")
        print(f"Search all (empty string): {len(all_search)} results")
        
        print("\n=== FINAL DATABASE STATE ===")
        all_final = db.get_all_records()
        print(f"Total records: {len(all_final)}")
        for record in all_final[-5:]:  # Show last 5 records
            name_preview = record['name'][:30] + "..." if len(record['name']) > 30 else record['name']
            print(f"  ID {record['id']}: {name_preview} = {record['value']}")
    finally:
        if db is not None:
            db.close()
        # Keep the database file for inspection
        print(f"Database saved as: {test_db_path}")

if __name__ == "__main__":
    testa_database_py_funktioner()

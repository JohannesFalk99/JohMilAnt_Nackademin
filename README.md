### **initial stuff**

### **DatabaseHandler**

* Initialize/open database
* Create tables
* Add a record
* Retrieve a specific record
* Retrieve all records
* Update a record
* Delete a record
* Close connection

---

#### **MenuGUI (PyQt GUI)**

* Initialize main window
* Build layout (frames, widgets, containers)
* Add buttons, labels, input fields, lists/tables
* Display messages/popups
* Clear/reset input fields
* Bind GUI events to **controller functions**
* Refresh/redraw interface dynamically
* Start GUI main loop

---

### **Controller**

* Receives events from GUI
* Calls appropriate **DatabaseHandler** methods
* Validates input data
* Updates GUI after database changes

*(Acts as the middleman between GUI and database, keep shit decoupled)*

---
This ensures:

* GUI Knows jack shit about database
* Database knows jack shit about GUI
* Controller handles all interactions between the two

Minimal dependency, keeping everything as decoupled as possible. 
Ensures the codebase is easy to maintain and modular
---

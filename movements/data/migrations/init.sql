CREATE TABLE MOVEMENTS (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		datepurchase TEXT NOT NULL,
		timepurchase TEXT NOT NULL,
		from_currency VARCHAR(3) NOT NULL, 
		form_quantity REAL NOT NULL,
		to_currency VARCHAR(3) NOT NULL,  
		to_quantity REAL NOT NULL
			)
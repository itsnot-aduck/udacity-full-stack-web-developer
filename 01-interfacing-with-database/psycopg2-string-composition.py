import psycopg2 

connection = psycopg2.connect(dbname = "example", user = "postgres", host = "localhost", password = "1234")

cursor = connection.cursor()

# DROP if existed 
cursor.execute('DROP TABLE IF EXISTS table3;')

cursor.execute('''
               CREATE TABLE table3(
                    id INTEGER PRIMARY KEY,
                    completed BOOLEAN NOT NULL DEFAULT False
               );
               ''')

# Pass by string
cursor.execute('INSERT INTO table3 (id, completed) VALUES (%s, %s);', (1, True))

# Pass by tuple
cursor.execute('INSERT INTO table3 (id, completed) ' + 'VALUES (%(id)s, %(completed)s);', {
    'id': 2,
    'completed': False
})

data = {
    'id': 3,
    'completed': False
}
# Pass by object 
cursor.execute('INSERT INTO table3 (id, completed) ' + 'VALUES (%(id)s, %(completed)s);', data)
# Commit the work to database
connection.commit()

# Close the connection
cursor.close()
connection.close()
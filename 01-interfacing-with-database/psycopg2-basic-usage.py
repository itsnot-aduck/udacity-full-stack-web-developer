import psycopg2

connection = psycopg2.connect(dbname = "example", user="postgres", host="localhost", password = "1234")

# The cursor is offered by the connection object as a result of connecting to psycopg2
cursor = connection.cursor()

# Cursor is a interface to start queuing up work and transaction
cursor.execute('''
               CREATE TABLE table3(
                    id INTEGER PRIMARY KEY,
                    completed BOOLEAN NOT NULL DEFAULT False
               );
               ''')

cursor.execute('INSERT INTO table3 (id, completed) VALUES (1, true);')

# Commit the work to database
connection.commit()

# Close the connection
cursor.close()
connection.close()
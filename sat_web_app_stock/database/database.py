import mysql.connector

# Replace these with your MySQL server details
host = 'localhost'
user = 'root'
password = '12memoreX-!'
database = 'cmada'

# Establish a connection to the MySQL server
connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

cursor = connection.cursor()

table_name = 'products_db'
create_table_query = """
CREATE TABLE IF NOT EXISTS {} (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    age INT
)
""".format(table_name)

cursor.execute(create_table_query)

print('OK')
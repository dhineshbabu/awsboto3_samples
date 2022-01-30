import psycopg2
import boto3
import json
import time
from datetime import date
import random



def get_secret_values(secret_id = None):
    # RDS will create a secret value for the connection string and configuration information

    if secret_id is not None:
        client = boto3.client('secretsmanager', region_name='us-east-1')
        response = client.get_secret_values(
            SecretId=secret_id
        )

        return response


def get_connection(hostname, port, databasename, username, password):
    # Establish connection to the database

    conn = psycopg2.connect(
        host = hostname,
        database = databasename,
        user = username,
        password = password,
        port = port
    )

    return conn


def create_table(conn):
    # Query to create the table

    create_query = '''
        CREATE TABLE userdetails(
            username VARCHAR ( 50 ) PRIMARY KEY,
            email VARCHAR ( 50 ) NOT NULL,
        );
    '''

    cursor = conn.cursor()
    cursor.execute(create_query)
    conn.commit()
    print('Table created successfully...')


def insert_read_data(conn):

    # Query to insert and read data

    seq_time = str(int(time.time()))
    insert_query = f'''INSERT INTO public.userdetails (username, email) VALUES ('test{seq_time}' 'test{seq_time}@test.com');'''
    cursor = conn.cursor()
    cursor.execute(insert_query)
    conn.commit()
    print('1 Record inserted successfully')
    time.sleep(1)
    # Extacting data
    cursor.execute(f"SELECT * FROM userdetails WHERE username='test{seq_time}'")
    record = cursor.fetchall()
    print('Result from RDS read ', record)


def lambda_handler(event, context):
    # Read the secret for database connection information. Do not print this

    secret_list = get_secret_values('RDS_SECRET_NAME') # RDS secret name
    database_secrets = json.loads(secret_list['SecretString'])
    db_host = database_secrets['host']
    db_port = database_secrets['port']
    db_name = database_secrets['dbname']
    db_username = database_secrets['username']
    db_password = database_secrets['password']

    try:
        # Establish connection to the database
        connection = get_connection(db_host, db_port, db_name, db_username, db_password)
        # Table name "userdetails" already created call the create_table() function to create more tables
        # Insert records into the table and will fetch all the results from the table based on the filter 
        insert_read_data(connection)
    except (psycopg2.DatabaseError) as error:
        print('Something went wrong ', error)
    finally:
        if connection is not None:
            connection.close()
            print('Connection to the database closed')

    return {
        'statusCode': 200,
        'body': 'Secrets Retrieved'
    }

if __name__ == '__main__':
    lambda_handler(None, None)
from awsdemo import DYNAMODB_TABLE, ECS_API_URL, LAMBDA_API_URL, RDS_SECRET_NAME, S3_BUCKET_NAME, SNS_TOPIC_ARN
from logging import debug
from awsdemo.awscomponents import dynamodb,S3, rdsaurora, sns
from flask import Flask,request, Response,jsonify
import json
import time
from datetime import date
import psycopg2
import requests

#Initiate app
app = Flask(__name__)

#Any configuration goes here

''' Routes for the API calls''' 

#### Routes for sns #### 

#  API for publishing the message
@app.route('/snspublish',methods = ['GET'])
def sns_publish() :
    # read the total count of messages from the http get parameter
    total_messages = int (request.args.get('messagecount'))

    # SNS_TOPIC_ARN initialized in __init__.py
    for i in range(total_messages):
        time.sleep(1)
        sns_response =sns.publish_message(SNS_TOPIC_ARN)
        print(sns_response)

    return Response(f"{total_messages} messages published to SNS topic", status=200)

# API for listing the subscriptions
@app.route('/snslist', methods = ['GET'])
def sns_list():

    # SNS_TOPIC_ARN initialized in__init__.py
    sns_response = sns.subscription_list(SNS_TOPIC_ARN)
    print(sns_response)
    return Response(json.dumps(f'Response is: {sns_response}'), status = 200)


#### Route for S3 actions ####

# API for uploading the files
@app.route('/s3upload', methods = ['GET'])
def s3_upload():

    # S3 Bucket Name initialized in __init__.py
    s3_response = S3.upload_files(S3_BUCKET_NAME)
    print(s3_response)
    return Response(json.dumps(f'Response is: {s3_response}'), status = 200) 

# API for listing the contents and file count
@app.route('/s3listobjects', methods = ['GET'])
def s3_listobjects():

    # S3 bucket name initialized in __init__.py
    s3_response = S3.list_files(S3_BUCKET_NAME)
    print(s3_response)
    return Response(json.dumps(f'Response is: {s3_response}'), status = 200)


# API for get a file contents. This will make get object call to the bucket
@app.route('/s3getobject', methods = ['GET'])
def s3_getobject():

    # S3 Bucket Name initialized in __init__.py
    s3_response = S3.get_s3_object(S3_BUCKET_NAME)
    print(s3_response)
    return Response(json.dumps(f'Response is: {s3_response}'), status = 200)


#### Route for DynamoDB actions #### 

# API for DynamoDB operations
@app.route('/dynamocrudoperations', methods = ['GET'])
def dynamo_crudoperations():

    # Step 01: Create 2 items in the DynamoDB table 
    for i in range(2):
        time.sleep(1)
        order_id_input = str(date.today())
        test_id_input = int(time.time())
        create_item_response = dynamodb.create_item(order_id_input, test_id_input, f'Dynatrace Test {order_id_input}{test_id_input}', DYNAMODB_TABLE)
        print('Items added successfully to DynamoDB table')

    time.sleep(1)
    
    # Step 02: Read any of the added item from the table
    read_item_response = dynamodb.read_item(order_id_input, test_id_input, DYNAMODB_TABLE)
    print('Item Read Successfully from DynamoDB table')

    time.sleep(1)

    # Step 03: Delete an entry from DynamoDB table
    delete_item_response = dynamodb.remove_item(order_id_input, test_id_input, DYNAMODB_TABLE)
    print('Item Deleted Successfully from DynamoDB')

    return Response(json.dumps('Opereations completed successfully on DynamoDB table'), status=200)


#### Route for RDS Aurora (PostgreSQL) actions ####

# API for RDS operations
@app.route('/rdscrudoperations', methods = ['GET'])
def rds_crudoperations():

    # Read the dataabse details from the secret manager. Important: Do not print these values
    secret_list = rdsaurora.get_secret_values(RDS_SECRET_NAME)
    database_secrets = json.loads(secret_list['SecretString'])
    db_host = database_secrets['host']
    db_port = database_secrets['port']
    db_name = database_secrets['dbname']
    db_username = database_secrets['username']
    db_password = database_secrets['password']

    try:
        # Establish connection to the database
        connection = rdsaurora.get_connection(db_host, db_port, db_name, db_username, db_password)
        # Table name "user details" already created call the create_table() function to create more tables
        # Insert records into the table and will fetch all the results from the table based on the filter
        rdsaurora.insert_read_data(connection)

    except (Exception, psycopg2.DatabaseError) as error:
        print('Something went wrong ', error)

    finally:
        if connection is not None:
            connection.close()
            print('Connection to the database closed')

    return Response(json.dumps('Opereations completed successfully on RDS table'), status=200)


#### Route for ECS Operations #### 

# This will have simple URL to call and this will have entry for the load balancer and container insights for ECS

@app.route('/ecsoperations', methods = ['GET'])
def ecs_apioperations():
    payload = {'message': 'sample message for the ECS payload'}
    headers = {'content-type': 'application/json', 'Accept': 'application/json'}
    ecs_response = requests.post(ECS_API_URL, json=payload, headers=headers)
    return Response(f'{ecs_response}, {ecs_response.status_code}', status = 200)
    # return r.text


#### Route for Lambda and APIGW ####

# This will have a simple lambda function attached with APIGW
@app.route('/lambdaoperations', methods = ['GET'])
def lambda_operations():
    LAMBDA_API_URL = "target API URL will go here"
    headers = {'content-type': 'application/json', 'Accept': 'application/json'}
    lambda_response = requests.get(LAMBDA_API_URL, headers=headers)
    return Response(f'{lambda_response.content}, {lambda_response.status_code}', status = 200)


if __name__ == '__main__':
    app.run(debug = True)
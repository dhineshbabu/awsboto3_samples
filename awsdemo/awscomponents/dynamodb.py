from pprint import pprint
import boto3
from botocore.exceptions import ClientError
import time
from datetime import date

# Function for creating new item
def create_item(order_id, test_id, description, tablename):

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table(tablename)
    response = table.put_item(
        Item = {
            'OrderID': str(order_id),
            'TestID': str(test_id),
            'Desc': str(description)
        }
    )

    return response

# Function to retrieve an item from DynamoDB table

def read_item(order_id, test_id, tablename):

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table(tablename)

    try:
        response = table.get_item(Key={'OrderID': str(order_id), 'TestID': str(test_id)})
    except ClientError as e:
        print(f'Something went wrong ' + e.response['Error']['Message'])
    else:
        return response['Item']


# Function to delete an item from DynamoDB table 

def remove_item(order_id, test_id, tablename):

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table(tablename)

    try:
        response = table.delete_item(Key={'OrderID': str(order_id), 'TestID': str(test_id)})
    except ClientError as e:
        print(f'Something went wrong ' + e.response['Error']['Message'])
    else:
        return response['Item']
    

if __name__ == '__main__':

    order_id_input = str(date.today())
    test_id_input = str(time.time())

    # Create a new item with
    create_item_response = create_item(order_id_input, test_id_input, f'Dynatrace Test {order_id_input} {test_id_input}')
    print('Item added successfully')
    pprint(create_item_response, sort_dicts=False)

    # Read an item
    read_item_response = read_item(order_id_input, test_id_input)
    print('Item Read Successfully')
    pprint(read_item_response, sort_dicts=False)

    # Delete an item
    delete_item_response = remove_item(order_id_input, test_id_input)
    print('Item Deleted successfully')
    pprint(delete_item_response, sort_dicts=False)
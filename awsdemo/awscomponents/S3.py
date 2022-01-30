import os
import sys
import time
from datetime import date
import boto3
from botocore.exceptions import ClientError
import string
import random

# Generating random / unique file names
def generate_file_names(total_file_count, file_directory):
    ''' This funcion will generate files, write some random text and will store it in the same location'''

    file_names = []
    for _ in range(total_file_count):
        time.sleep(1)
        current_time = str(int(time.time()))
        current_date = str(date.today())
        # file_name = os.path.join(file_directory, 'dynatrace'+current_date.replace('-', '') + current_time + '.txt')
        file_name = 'dynatrace' + current_date.replace('-', '') + current_time + '.txt'
        file_names.append(file_name)
        if len(file_names) == total_file_count:
            return file_names
        
    return None

# Creating files in local directory for upload

def generate_files(file_names):
    for name in file_names:
        try:
            with open(name, 'w') as file:
                file.write('some random text' + ''.join(random.choices(
                    string.ascii_uppercase + string.digits,
                    k = 10
                )))
        except IOError as e:
            print(f'I/O Error {e.errno}: {e.strerror} during the file operation')
        except: # handle other exceptions such as attribute errors
            print('Unexpected error: ', sys.exc_info()[0])


# Uploading the files to S3 bucket
def upload_files(bucket):
    s3_client = boto3.client('s3')
    
    # Generate random file names and get the list
    current_directory = os.getcwd()
    random_file_names = generate_file_names(total_file_count = 1, file_directory = current_directory)

    # Create required random txt files in the current working directory
    if random_file_names:
        generate_files(file_names = random_file_names)

        for file in random_file_names:
            try:
                s3_client.upload_file(file, bucket, file)
                print(f'File uploaded {file} ')
            except ClientError as e:
                print('Client error ', e)
                return False
    return f'Uploaded file(s) {random_file_names}'


# Listing the objects in the bucket
def list_files(bucket):
    s3_client = boto3.client('s3')
    try:
        response = s3_client.list_files(Bucket = bucket)
        if response:
            print('Total files in the bucket:')
            print(len(response['Contents']))
            for i in response['Contents']:
                print(f'{i["Key"]}')
        return {'total_files': len(response['Contents'])}
    except ClientError as e:
        print('Client error ', e)


# Code for creating a get request for S3 bucket and this will read the existing file from the bucket
def get_s3_object(bucket):
    s3_client = boto3.client('s3')
    
    try:
        file_to_get = None
        file_list = s3_client.list_objects_v2(Bucket = bucket)
        if file_list and len(file_list['Contents']) > 0:
            random.shuffle(file_list['Contents'])
            for i in file_list['Contents']:
                if '.txt' in i["Key"]:
                    file_to_get = f'i["Key"]'
                    break

        if file_to_get:
            # print(file_to_get)
            response = s3_client.get_object(Bucket = bucket, Key = file_to_get)
            print(response)
            return f'Get file call made for {file_to_get}'
            

    except ClientError as e:
        print('Client error ', e)
    except Exception as e:
        print('Something went wrong, ', e)


if __name__ == '__main__':

    # Upload files to S3 bucket
    upload_files(bucket = 'any bucket name')

    # List the objects 
    list_files(bucket = 'any bucket name')

    # Get the object
    get_s3_object(bucket = 'any bucket name')

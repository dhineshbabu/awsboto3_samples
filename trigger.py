import json
import requests
import time

def trigger_test(input_dict):

    # All the API routes will be available as a Flask application and will be running in port 5000 in localhost

    for service, data in input_dict.items():
        print('--------------------------------------------')
        print(f'##### Calling API for {service} #####')
        print('--------------------------------------------')

        api_url = data[0]
        count = data[1]

        for _ in range(count):
            try:
                response = requests.get(api_url)
                print(response.content)
                time.sleep(3)
            except Exception as e:
                print(f'Something went wrong {e}')
                break
            else:
                print(f'API for {service} completed')



if __name__ == '__main__':

    # This dictionary will have a list for each AWS service that will expose API url from flask application and the total iterations to be executed

    url_dict = {
        'snspublish': ['http://127.0.0.1:5000/snspublish?messagecount=1', 2],
        'snslist': ['http://127.0.0.1:5000/snslist', 2],
        's3upload': ['http://127.0.0.1:5000/s3upload', 2],
        's3listobjects': ['http://127.0.0.1:5000/s3listobjects', 2],
        's3getobject': ['http://127.0.0.1:5000/s3getobject', 2],
        'dynamocrudoperations': ['http://127.0.0.1:5000/dynamocrudoperations', 2],
        'rdscrudoperations': ['http://127.0.0.1:5000/rdscrudoperations', 2],
        'ecsoperations': ['http://127.0.0.1:5000/ecsoperations', 2],
        'lambdaoperations': ['http://127.0.0.1:5000/lambdaoperations', 2],
    }

    trigger_test(url_dict)
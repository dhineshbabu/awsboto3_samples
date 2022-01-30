import json
import boto3
from botocore.exceptions import ClientError
import time
from datetime import date 


def publish_message(sns_topic_arn):
    ''' This function will publish a simple json message to the sns topic '''

    # Input json 
    input_json = {
        'name': 'test message',
        'date': str(int(time.time())),
        'time': str(date.today())
    }

    try:

        # Initiate client and publish message
        sns_client = boto3.client('sns', region_name='us-east-1')

        sns_response = sns_client.publish(
            TargetArn = sns_topic_arn,
            Message = json.dumps(input_json)
        )
        # print(f'Message published: {sns_response}')
        return sns_response

    except ClientError as e:
        print(f'Client error while publishing the message to the sns topic: {e}')



def subscription_list(sns_topic_arn):
    ''' This function will list the available subscriptions for the SNS topic '''

    try:
        # Initiate client and publish message
        sns_client = boto3.client('sns', region_name='us-east-1')

        sns_subscriptions = sns_client.list_subscriptions_by_topic(
            TopicArn = sns_topic_arn
        )

        if sns_subscriptions:
            for subscription in sns_subscriptions['Subscriptions']:
                print(f'Subscription : {subscription["SubscriptionArn"]}')
                return sns_subscriptions['Subscriptions']

    except ClientError as e:
        print(f'CLient error while listing subscriptions of the sns topic: {e}')


    
if __name__ == '__main__':

    topic_arn = "Any topic ARN will come here"

    # Publish message to the SNS topic 
    publish_message(topic_arn)

    # List the ARNs of the available subscriptions to the SNS topic
    subscription_list(topic_arn)
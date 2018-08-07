import boto3
import json

sqs_queue_name = 'queue_name'
aws_credential_profile = 'profile_name'
aws_region = 'region_name'

session = boto3.Session(
    profile_name=aws_credential_profile,
    region_name=aws_region
)

sqs = session.resource('sqs')
queue = sqs.get_queue_by_name(QueueName=sqs_queue_name)

sqsclient = session.client('sqs')

# send sqs messages
for i in range(0, 10):
    msg = {'id': i}
    print(msg)
    result = sqsclient.send_message(
        QueueUrl=queue.url,
        MessageBody=json.dumps(msg),
        DelaySeconds=0,
        MessageGroupId='z'
    )
    print(result)

# receive single message
message = sqsclient.receive_message(
    QueueUrl=queue.url,
    AttributeNames=['All'],
    MaxNumberOfMessages=1,
    WaitTimeSeconds=10,
    VisibilityTimeout=60
)

#print(message['Messages'][0]['Body'])

# Get handle for delete
message_handle = (message['Messages'][0]['ReceiptHandle'])

# Delete message while in flight
delete = sqsclient.delete_message(
    QueueUrl=queue.url,
    ReceiptHandle=message_handle
)

import boto3
import uuid

# Setting up boto session
session = boto3.Session()
s3_resource = boto3.resource('s3')

# Create a random bucket name
def create_bucket_name(bucket_prefix):
  return ''.join([bucket_prefix, str(uuid.uuid4())])

# Create a bucket function and push to S3 in AWS
def create_bucket(bucket_prefix, s3_connection):
    current_region = session.region_name
    bucket_name = create_bucket_name(bucket_prefix)
    bucket_response = s3_connection.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={
            'LocationConstraint': current_region})
    # print(bucket_name, current_region)
    return bucket_name, bucket_response

def enable_bucket_versioning(bucket_name):
    bkt_versioning = s3_resource.BucketVersioning(bucket_name)
    bkt_versioning.enable()
    print(bkt_versioning.status)

def run_creation_script():
    first_bucket_name, first_response = create_bucket(
        bucket_prefix='firstpythonbucket', 
        s3_connection=s3_resource.meta.client)
        
    second_bucket_name, second_response = create_bucket(
        bucket_prefix='secondpythonbucket', 
        s3_connection=s3_resource)
        
    print('First Bucket Name:', first_bucket_name, '\nFirst Response Name:', first_response, sep='\n')
    print('\nSecond Bucket Name:', second_bucket_name, '\nSecond Response Name:', second_response, sep='\n')
    
    return first_bucket_name, second_bucket_name

def delete_all_objects(bucket_name):
    res = []
    bucket=s3_resource.Bucket(bucket_name)
    for obj_version in bucket.object_versions.all():
        res.append({'Key': obj_version.object_key,
                    'VersionId': obj_version.id})
        print(res)
        bucket.delete_objects(Delete={'Objects': res})
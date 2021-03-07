import boto3
import uuid

session = boto3.Session()
s3_resource = boto3.resource('s3')

def create_public_file(first_bucket):
    second_file_name = create_temp_file(400, 'secondfile.txt', 's')
    second_object = s3_resource.Object(first_bucket, second_file_name)
    second_object.upload_file(second_file_name, ExtraArgs={'ACL': 'public-read'})
    second_object_acl = second_object.Acl()
    
    verify_permission = input("Are you sure you want to keep this public (y/n)?")
    verify_input = False
    
    while verify_input == False:
        if verify_permission.lower() == 'n':
            response = second_object_acl.put(ACL='private')
            print(second_object_acl.grants, response)
            verify_input = True    
        else:
            if verify_permission.lower() == 'y':
                print(second_object_acl.grants)  
                verify_input = True
            else:
                verify_permission = input(
                    "Bad input. Are you sure you want to keep this public (y/n)?")
    return second_file_name

def create_encrypted_file(first_bucket_name):
    third_file_name = create_temp_file(300, 'thirdfile.txt', 't')
    third_object = s3_resource.Object(first_bucket_name, third_file_name)
    third_object.upload_file(third_file_name, ExtraArgs={
        'ServerSideEncryption': 'AES256'})
    
    print (third_object.server_side_encryption)
    
    change_s3 = input("The storage of the file is standard. Change to Standard_IA (y/n)?")
    verify_input = False
    
    while verify_input == False:
        if change_s3.lower() == 'n':
            print(third_object.storage_class)
            verify_input = True    
        else:
            if change_s3.lower() == 'y':
                third_object.upload_file(third_file_name, ExtraArgs={
                    'ServerSideEncryption': 'AES256',
                    'StorageClass': 'STANDARD_IA'})
                third_object.reload()
                print(third_object.storage_class)
                verify_input = True
            else:
                change_s3 = input(
                    "Bad Input. The storage of the file is standard. Change to Standard_IA (y/n)?")
    return third_file_name

def upload_new_version(bucket_name, file_name):
    s3_resource.Object(bucket_name, file_name).upload_file(
            file_name)
    print(s3_resource.Object(bucket_name, file_name).version_id)
    
def create_temp_file(size, file_name, file_content):
    random_file_name = ''.join([str(uuid.uuid4().hex[:6]), file_name])
    with open(random_file_name, 'w') as f:
        f.write(str(file_content) * size)
        return random_file_name
    
def download_file(first_bucket_name, first_file_name):
    s3_resource.Object(first_bucket_name, first_file_name).download_file(
            'C:\\Users\\Omriz-PC\\Documents\\DevOps\\Python\\Project\\Downloads\\' + first_file_name)

def copy_to_bucket(bucket_from_name, bucket_to_name, copied_file_name):
    copy_source = {
        'Bucket': bucket_from_name,
        'Key': copied_file_name
        }
    s3_resource.Object(bucket_to_name, copied_file_name).copy(copy_source)
    print ("Copied {copied_file_name} from {bucket_from_name} to {bucket_to_name}".format(
        copied_file_name=copied_file_name,
        bucket_from_name=bucket_from_name,
        bucket_to_name=bucket_to_name))

def delete_file(from_bucket, file_name):
    s3_resource.Object(from_bucket, file_name).delete()
    
def run_files_script(first_bucket_name):
    first_file_name = create_temp_file(300, 'firstfile.txt', 'f')       
    print(first_file_name)
    
    upload_option = int(input("Choose how to upload file:" + 
                          "\n1 - From an object instance:" + 
                          "\n2 - From a bucket instance:" + 
                          "\n3 - From a client:" + 
                          "\nAny other option to exit:"))   
    
    if upload_option == 1:
        s3_resource.Object(first_bucket_name, first_file_name).upload_file(
            Filename=first_file_name)
        print (first_file_name, "Uploaded using the Object instance.")        
    else:
        if upload_option == 2:
            s3_resource.Bucket(first_bucket_name).upload_file(
                Filename=first_file_name, Key=first_file_name)
            print (first_file_name, "Uploaded using the Bucket instance.")
            
        else:
            if upload_option == 3:
                s3_resource.meta.client.upload_file(
                    Filename=first_file_name, Bucket=first_bucket_name,
                    Key=first_file_name)
                print (first_file_name, "Uploaded from the Client.")
    return first_file_name
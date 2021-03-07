import boto3
import bucket_management
import files_handling
import time

s3_resource = boto3.resource('s3')

already_created = False
instructions ="What would you like to do?" + \
                      "\n1.  Create 2 buckets." + \
                      "\n2.  Create a private file." + \
                      "\n3.  Download a file from bucket." + \
                      "\n4.  Copy from the first bucket to the second." + \
                      "\n5.  Delete the copied file from the second bucket." + \
                      "\n6.  Create a public file." + \
                      "\n7.  Create an encrypted file." + \
                      "\n8.  Enable versioning to the first bucket." + \
                      "\n9.  Show a list of the objects in a bucket." + \
                      "\n10. Delete objects from the first bucket." + \
                      "\n11. Delete the first bucket.\n"
                      
func_selector = int(input(instructions))

while func_selector > 0 and func_selector < 12:    
    # Create 2 buckets. If already created, throw an error.
    if func_selector == 1 and already_created == False:
        first_bucket_name, second_bucket_name = bucket_management.run_creation_script()
        already_created = True
        
    # Error if 2 buckets are already created.
    else:
        if func_selector == 1 and already_created == True:
            print("\nAlready created 2 first buckets. Select other option.")
            time.sleep(3)
    
    # Create a temp file and add it to a bucket
    if func_selector == 2:
        first_file_name = files_handling.run_files_script(first_bucket_name)
        
    if func_selector == 3:
        files_handling.download_file(first_bucket_name, first_file_name)
    
    if func_selector == 4:
        files_handling.copy_to_bucket(first_bucket_name, second_bucket_name, first_file_name)
    
    if func_selector == 5:
        files_handling.delete_file(second_bucket_name, first_file_name)
    
    if func_selector == 6:
        second_file_name = files_handling.create_public_file(first_bucket_name)       
    
    if func_selector == 7:
        third_file_name = files_handling.create_encrypted_file(first_bucket_name)
        
    if func_selector == 8:
        bucket_management.enable_bucket_versioning(first_bucket_name)
        files_handling.upload_new_version(first_bucket_name, first_file_name)
        files_handling.upload_new_version(first_bucket_name, third_file_name)
        files_handling.upload_new_version(first_bucket_name, second_file_name)
        
    if func_selector == 9:
        for bucket in s3_resource.buckets.all():
            print(bucket.name)
            for obj in bucket.objects.all():
                subsrc = obj.Object()
                print("  " + obj.key, obj.storage_class, obj.last_modified,
                      subsrc.version_id, subsrc.metadata)
    
    if func_selector == 10:
        bucket_management.delete_all_objects(first_bucket_name)    
    
    if func_selector == 11:
        print(s3_resource.Bucket(first_bucket_name).delete())
                    
    func_selector = int(input(instructions))
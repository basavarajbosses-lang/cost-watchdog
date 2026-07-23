import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    
    # Step 1: Get all running EC2 instances
    running_instances = []
    try:
        instances = ec2.describe_instances(
            Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
        )
        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                running_instances.append(instance['InstanceId'])
        print(f"Found {len(running_instances)} running instances")
    except ClientError as e:
        print(f"Error getting instances: {e}")
        return {'statusCode': 500, 'body': 'Failed to describe instances'}
    
    # Step 2: Get all snapshots owned by this account
    try:
        snapshots = ec2.describe_snapshots(OwnerIds=['self'])['Snapshots']
        print(f"Found {len(snapshots)} total snapshots")
    except ClientError as e:
        print(f"Error getting snapshots: {e}")
        return {'statusCode': 500, 'body': 'Failed to describe snapshots'}
    
    # Step 3: Check each snapshot
    deleted_count = 0
    for snapshot in snapshots:
        snapshot_id = snapshot['SnapshotId']
        volume_id = snapshot.get('VolumeId')
        
        # Case A: No volume attached - safe to delete
        if not volume_id:
            delete_snapshot(ec2, snapshot_id, "No associated volume")
            deleted_count += 1
            continue
        
        # Case B: Check if volume still exists
        try:
            volume_response = ec2.describe_volumes(VolumeIds=[volume_id])
            if not volume_response['Volumes']:
                delete_snapshot(ec2, snapshot_id, "Volume not found")
                deleted_count += 1
                continue
            
            volume = volume_response['Volumes'][0]
            
            # Case C: Volume exists but not attached to any instance
            if not volume['Attachments']:
                delete_snapshot(ec2, snapshot_id, "Volume not attached to any instance")
                deleted_count += 1
                continue
            
            # Case D: Attached to a non-running instance
            instance_id = volume['Attachments'][0]['InstanceId']
            if instance_id not in running_instances:
                delete_snapshot(ec2, snapshot_id, f"Instance {instance_id} is not running")
                deleted_count += 1
                
        except ClientError as e:
            if e.response['Error']['Code'] == 'InvalidVolume.NotFound':
                delete_snapshot(ec2, snapshot_id, "Volume not found (API error)")
                deleted_count += 1
            else:
                print(f"Unexpected error for {snapshot_id}: {e}")
    
    print(f"Successfully deleted {deleted_count} snapshots")
    return {
        'statusCode': 200,
        'body': f'Deleted {deleted_count} snapshots'
    }

def delete_snapshot(ec2, snapshot_id, reason):
    """Helper function to delete a snapshot and log the reason."""
    print(f"DELETING: {snapshot_id} - Reason: {reason}")
    try:
        ec2.delete_snapshot(SnapshotId=snapshot_id)
    except ClientError as e:
        print(f"ERROR deleting {snapshot_id}: {e}")
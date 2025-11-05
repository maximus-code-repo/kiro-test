#!/usr/bin/env python3
"""
AWS Setup Helper for Bedrock Joke Generator
Helps verify AWS configuration and Bedrock access.
"""

import boto3
import json
from botocore.exceptions import ClientError, NoCredentialsError

def check_aws_credentials():
    """Check if AWS credentials are configured."""
    try:
        session = boto3.Session()
        credentials = session.get_credentials()
        if credentials is None:
            return False, "No AWS credentials found"
        
        # Test credentials with STS
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        return True, f"Credentials valid for: {identity.get('Arn', 'Unknown')}"
    
    except NoCredentialsError:
        return False, "AWS credentials not configured"
    except Exception as e:
        return False, f"Error checking credentials: {str(e)}"

def check_bedrock_access(region='us-east-1'):
    """Check if Bedrock service is accessible."""
    try:
        bedrock = boto3.client('bedrock', region_name=region)
        # Try to list foundation models
        response = bedrock.list_foundation_models()
        models = response.get('modelSummaries', [])
        return True, f"Bedrock accessible. Found {len(models)} models in {region}"
    
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'AccessDeniedException':
            return False, f"Access denied to Bedrock in {region}. Check IAM permissions."
        else:
            return False, f"Bedrock error in {region}: {error_code}"
    except Exception as e:
        return False, f"Error accessing Bedrock: {str(e)}"

def check_model_access(region='us-east-1'):
    """Check access to specific models."""
    models_to_check = [
        'anthropic.claude-3-haiku-20240307-v1:0',
        'anthropic.claude-3-sonnet-20240229-v1:0',
        'amazon.titan-text-express-v1'
    ]
    
    try:
        bedrock = boto3.client('bedrock-runtime', region_name=region)
        accessible_models = []
        
        for model_id in models_to_check:
            try:
                # Try a minimal test request
                test_body = {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 10,
                    "messages": [{"role": "user", "content": "Hi"}]
                } if 'claude' in model_id else {
                    "inputText": "Hi",
                    "textGenerationConfig": {"maxTokenCount": 10}
                }
                
                bedrock.invoke_model(
                    modelId=model_id,
                    body=json.dumps(test_body)
                )
                accessible_models.append(model_id)
            except ClientError as e:
                if e.response['Error']['Code'] != 'AccessDeniedException':
                    accessible_models.append(f"{model_id} (limited access)")
        
        return accessible_models
    
    except Exception as e:
        return [f"Error testing models: {str(e)}"]

def main():
    """Run AWS setup checks."""
    print("🔧 AWS Bedrock Setup Checker")
    print("=" * 40)
    
    # Check credentials
    print("\n1. Checking AWS Credentials...")
    creds_ok, creds_msg = check_aws_credentials()
    print(f"   {'✅' if creds_ok else '❌'} {creds_msg}")
    
    if not creds_ok:
        print("\n📋 To configure AWS credentials:")
        print("   Option 1: Run 'aws configure'")
        print("   Option 2: Set environment variables:")
        print("     export AWS_ACCESS_KEY_ID=your_key")
        print("     export AWS_SECRET_ACCESS_KEY=your_secret")
        print("     export AWS_DEFAULT_REGION=us-east-1")
        return
    
    # Check Bedrock access
    regions_to_check = ['us-east-1', 'us-west-2', 'eu-west-1']
    print(f"\n2. Checking Bedrock Access...")
    
    accessible_regions = []
    for region in regions_to_check:
        bedrock_ok, bedrock_msg = check_bedrock_access(region)
        print(f"   {'✅' if bedrock_ok else '❌'} {region}: {bedrock_msg}")
        if bedrock_ok:
            accessible_regions.append(region)
    
    if not accessible_regions:
        print("\n📋 To enable Bedrock access:")
        print("   1. Go to AWS Console → Bedrock")
        print("   2. Navigate to 'Model access' in the left sidebar")
        print("   3. Request access to Claude and Titan models")
        print("   4. Wait for approval (usually instant for Claude Haiku)")
        return
    
    # Check model access for the first accessible region
    if accessible_regions:
        region = accessible_regions[0]
        print(f"\n3. Checking Model Access in {region}...")
        accessible_models = check_model_access(region)
        
        for model in accessible_models:
            print(f"   ✅ {model}")
        
        if accessible_models:
            print(f"\n🎉 Setup Complete! You can use the joke generator.")
            print(f"   Recommended region: {region}")
            print(f"   Available models: {len(accessible_models)}")
        else:
            print(f"\n❌ No models accessible in {region}")

if __name__ == "__main__":
    main()
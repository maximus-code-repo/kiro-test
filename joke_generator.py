#!/usr/bin/env python3
"""
AWS Bedrock Joke Generator
A Python app that creates unique jokes using AWS Bedrock AI models.
"""

import boto3
import json
import random
from typing import Dict, List, Optional
from botocore.exceptions import ClientError, NoCredentialsError

class BedrockJokeGenerator:
    def __init__(self, region_name: str = 'us-east-1'):
        """Initialize the Bedrock joke generator."""
        self.region_name = region_name
        self.bedrock_client = None
        self.available_models = [
            'anthropic.claude-3-haiku-20240307-v1:0',
            'anthropic.claude-3-sonnet-20240229-v1:0',
            'amazon.titan-text-express-v1'
        ]
        self.current_model = self.available_models[0]  # Default to Claude Haiku
        
        # Joke style options
        self.joke_styles = {
            'pun': 'Create a clever pun-based joke',
            'dad': 'Create a classic dad joke',
            'witty': 'Create a witty, clever joke',
            'silly': 'Create a silly, lighthearted joke',
            'observational': 'Create an observational comedy joke',
            'wordplay': 'Create a joke using wordplay'
        }
        
        self._initialize_bedrock()
    
    def _initialize_bedrock(self):
        """Initialize the Bedrock client."""
        try:
            self.bedrock_client = boto3.client(
                service_name='bedrock-runtime',
                region_name=self.region_name
            )
            print("✅ AWS Bedrock client initialized successfully!")
        except NoCredentialsError:
            print("❌ AWS credentials not found. Please configure your AWS credentials.")
            print("   Run: aws configure")
        except Exception as e:
            print(f"❌ Error initializing Bedrock client: {str(e)}")
    
    def generate_joke(self, topic: str, style: str = 'witty', model: Optional[str] = None) -> str:
        """Generate a joke using AWS Bedrock."""
        if not self.bedrock_client:
            return "❌ Bedrock client not available. Please check your AWS configuration."
        
        model_id = model or self.current_model
        style_prompt = self.joke_styles.get(style, self.joke_styles['witty'])
        
        # Create the prompt
        prompt = self._create_prompt(topic, style_prompt)
        
        try:
            if 'claude' in model_id:
                return self._generate_with_claude(prompt, model_id)
            elif 'titan' in model_id:
                return self._generate_with_titan(prompt, model_id)
            else:
                return "❌ Unsupported model selected."
        
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'AccessDeniedException':
                return "❌ Access denied. Please check your AWS permissions for Bedrock."
            elif error_code == 'ValidationException':
                return "❌ Invalid request. Please check the model availability in your region."
            else:
                return f"❌ AWS Error: {error_code}"
        except Exception as e:
            return f"❌ Unexpected error: {str(e)}"
    
    def _create_prompt(self, topic: str, style_prompt: str) -> str:
        """Create a well-structured prompt for joke generation."""
        return f"""You are a professional comedian. {style_prompt} about the topic: "{topic}".

Requirements:
- Keep it clean and family-friendly
- Make it genuinely funny and original
- Keep it concise (1-3 sentences max)
- Focus specifically on the topic: {topic}

Topic: {topic}
Joke:"""
    
    def _generate_with_claude(self, prompt: str, model_id: str) -> str:
        """Generate joke using Claude models."""
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 200,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.8,
            "top_p": 0.9
        }
        
        response = self.bedrock_client.invoke_model(
            modelId=model_id,
            body=json.dumps(body)
        )
        
        response_body = json.loads(response['body'].read())
        return response_body['content'][0]['text'].strip()
    
    def _generate_with_titan(self, prompt: str, model_id: str) -> str:
        """Generate joke using Titan models."""
        body = {
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": 200,
                "temperature": 0.8,
                "topP": 0.9,
                "stopSequences": ["\n\n"]
            }
        }
        
        response = self.bedrock_client.invoke_model(
            modelId=model_id,
            body=json.dumps(body)
        )
        
        response_body = json.loads(response['body'].read())
        return response_body['results'][0]['outputText'].strip()
    
    def get_available_styles(self) -> List[str]:
        """Get list of available joke styles."""
        return list(self.joke_styles.keys())
    
    def set_model(self, model_name: str) -> bool:
        """Set the AI model to use."""
        if model_name in self.available_models:
            self.current_model = model_name
            return True
        return False
    
    def get_model_info(self) -> Dict[str, str]:
        """Get information about available models."""
        return {
            'current': self.current_model,
            'available': self.available_models
        }

def main():
    """Main function to run the joke generator."""
    print("🎭 AWS Bedrock Joke Generator 🎭")
    print("=" * 50)
    
    generator = BedrockJokeGenerator()
    
    if not generator.bedrock_client:
        print("\n❌ Cannot proceed without AWS Bedrock access.")
        print("Please ensure:")
        print("1. AWS CLI is configured: aws configure")
        print("2. You have Bedrock permissions")
        print("3. Models are enabled in your AWS region")
        return
    
    print(f"\n🤖 Current AI Model: {generator.current_model}")
    print(f"🎨 Available Styles: {', '.join(generator.get_available_styles())}")
    
    while True:
        print("\n" + "─" * 50)
        
        # Get topic
        topic = input("🎯 Enter a topic for your joke (or 'quit' to exit): ").strip()
        
        if topic.lower() in ['quit', 'exit', 'q']:
            print("\n🎉 Thanks for the laughs! Keep smiling! 👋")
            break
        
        if not topic:
            print("❌ Please enter a valid topic!")
            continue
        
        # Get style (optional)
        print(f"\n🎨 Choose a style ({', '.join(generator.get_available_styles())}) or press Enter for 'witty':")
        style = input("Style: ").strip().lower()
        if not style or style not in generator.get_available_styles():
            style = 'witty'
        
        print(f"\n🎭 Generating a {style} joke about '{topic}'...")
        print("⏳ Please wait...")
        
        # Generate joke
        joke = generator.generate_joke(topic, style)
        
        print(f"\n📜 Your {style} joke about '{topic}':")
        print("┌" + "─" * 48 + "┐")
        
        # Handle multi-line jokes
        joke_lines = joke.split('\n')
        for line in joke_lines:
            if line.strip():
                print(f"│ {line:<46} │")
        
        print("└" + "─" * 48 + "┘")
        
        # Ask for another
        print("\n🤔 What would you like to do next?")
        choice = input("   Press Enter for another joke, 'settings' for options, or 'quit' to exit: ").strip().lower()
        
        if choice in ['quit', 'exit', 'q']:
            print("\n🎉 Thanks for the laughs! Keep smiling! 👋")
            break
        elif choice == 'settings':
            show_settings_menu(generator)

def show_settings_menu(generator: BedrockJokeGenerator):
    """Show settings menu for model selection."""
    while True:
        print("\n⚙️  Settings Menu")
        print("─" * 20)
        model_info = generator.get_model_info()
        print(f"Current Model: {model_info['current']}")
        print("\nAvailable Models:")
        for i, model in enumerate(model_info['available'], 1):
            marker = "→" if model == model_info['current'] else " "
            print(f"{marker} {i}. {model}")
        
        print("\nOptions:")
        print("1-3: Select model")
        print("b: Back to joke generation")
        
        choice = input("\nChoice: ").strip().lower()
        
        if choice == 'b':
            break
        elif choice in ['1', '2', '3']:
            try:
                model_index = int(choice) - 1
                new_model = model_info['available'][model_index]
                if generator.set_model(new_model):
                    print(f"✅ Model changed to: {new_model}")
                else:
                    print("❌ Failed to change model")
            except (ValueError, IndexError):
                print("❌ Invalid selection")

if __name__ == "__main__":
    main()
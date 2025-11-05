# Joke & Limerick Generators

This repository contains two fun Python applications:

## 🎭 AWS Bedrock Joke Generator
Generates unique jokes using AWS Bedrock AI models based on topics you choose.

## 📜 Enhanced Limerick Generator  
Creates witty limericks locally without requiring any external services.

---

## Quick Start

### Limerick Generator (No Setup Required)
```bash
python enhanced_limerick_generator.py
```

### AWS Bedrock Joke Generator

1. **Install dependencies:**
```bash
pip install -r requirements_aws.txt
```

2. **Configure AWS credentials:**
```bash
aws configure
```

3. **Check your setup:**
```bash
python setup_aws.py
```

4. **Run the joke generator:**
```bash
python joke_generator.py
```

---

## AWS Bedrock Setup

### Prerequisites
- AWS Account with Bedrock access
- AWS CLI configured
- Bedrock model access enabled

### Enable Model Access
1. Go to AWS Console → Amazon Bedrock
2. Click "Model access" in the left sidebar  
3. Request access to:
   - Claude 3 Haiku (recommended - usually instant approval)
   - Claude 3 Sonnet (optional)
   - Titan Text Express (optional)

### Supported Regions
- us-east-1 (recommended)
- us-west-2  
- eu-west-1

---

## Features

### Joke Generator
- 🤖 Multiple AI models (Claude 3, Titan)
- 🎨 Various joke styles (pun, dad jokes, witty, etc.)
- 🔄 Unique jokes every time
- ⚙️ Model switching in runtime

### Limerick Generator  
- 📝 6 different limerick templates
- 🎯 Topic-specific word banks
- 🔄 Anti-repetition system
- 🎪 No external dependencies

---

## Usage Examples

### Joke Generator
```
🎯 Enter a topic: programming
🎨 Style: dad
📜 Result: "Why do programmers prefer dark mode? Because light attracts bugs!"
```

### Limerick Generator
```
🎯 Enter a topic: cat
📜 Result:
There once was a fluffy cat from Maine,
Who purred with incredible brain,
They'd dance and they'd play,
In their own special way,
What a sight to behold in Spain!
```

---

## Troubleshooting

### AWS Issues
- Run `python setup_aws.py` to diagnose problems
- Ensure your AWS region supports Bedrock
- Check IAM permissions for Bedrock access

### Common Errors
- **AccessDeniedException**: Request model access in Bedrock console
- **NoCredentialsError**: Run `aws configure`
- **ValidationException**: Check model availability in your region

---

## Cost Information

AWS Bedrock charges per token:
- Claude 3 Haiku: ~$0.00025 per 1K tokens (very affordable)
- Jokes typically use 50-100 tokens (~$0.000025 per joke)

The limerick generator is completely free as it runs locally.
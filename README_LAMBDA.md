# 🚀 Moses AI Assistant - AWS Lambda Deployment Guide

## Overview

Your AI Assistant is now configured for **serverless deployment** on AWS Lambda with API Gateway. This setup provides:

- **💰 Cost-Effective**: Pay only for requests (not idle time)
- **⚡ Auto-Scaling**: Handles traffic spikes automatically  
- **🔒 Secure**: AWS IAM and VPC integration
- **🌍 Global**: Deploy in multiple AWS regions

---

## 🏗️ Architecture

```
Frontend → API Gateway → Lambda Function → Your AI Assistant
```

**Components:**
- **Lambda Function**: Runs your FastAPI backend
- **API Gateway**: Provides public HTTPS endpoints
- **CloudFormation**: Infrastructure as Code
- **GitHub Actions**: Automated CI/CD pipeline

---

## 📋 Prerequisites

### 1. AWS Account Setup
- [ ] AWS Account (free tier eligible)
- [ ] AWS CLI installed: `aws --version`
- [ ] AWS SAM CLI installed: `sam --version`

### 2. GitHub Secrets Configuration
Add these secrets to your GitHub repository:

```bash
# Required AWS credentials
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here

# Your OpenAI API key
OPENAI_API_KEY=your_openai_key_here
```

### 3. Install AWS Tools
```bash
# Install AWS CLI
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /

# Install SAM CLI
brew tap aws/tap
brew install aws-sam-cli

# Configure AWS credentials
aws configure
```

---

## 🚀 Deployment Options

### Option 1: Automated GitHub Deployment ✨ (Recommended)

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Configure AWS Lambda deployment"
   git push origin develop  # Deploys to staging
   git push origin main     # Deploys to production
   ```

2. **Monitor Deployment:**
   - Visit GitHub Actions tab
   - Watch the deployment pipeline
   - Get your API URL from the logs

### Option 2: Manual Local Deployment

```bash
# Build the Lambda package
sam build --use-container

# Deploy to AWS
sam deploy --guided \
  --stack-name moses-ai-assistant \
  --parameter-overrides Stage=prod OpenAIApiKey=your_openai_key

# Get your API URL
aws cloudformation describe-stacks \
  --stack-name moses-ai-assistant \
  --query 'Stacks[0].Outputs[?OutputKey==`MosesAIAssistantApi`].OutputValue' \
  --output text
```

---

## 🔗 API Endpoints

Once deployed, your API will be available at:
```
https://{api-id}.execute-api.us-east-1.amazonaws.com/{stage}/
```

### Available Endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/health` | GET | Health check |
| `/stats` | GET | Usage statistics |
| `/expertise` | GET | Moses's expertise summary |
| `/query` | POST | General questions |
| `/query/technical` | POST | Technical questions |
| `/query/career` | POST | Career questions |
| `/query/projects` | POST | Project questions |

### Example API Call:
```bash
curl -X POST "https://your-api-url/query" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Tell me about Moses Omondi",
    "context_count": 5,
    "include_sources": true
  }'
```

---

## 💰 Cost Estimation

### AWS Lambda Pricing (us-east-1):
- **Free Tier**: 1M requests/month + 400K GB-seconds
- **After Free Tier**: $0.20 per 1M requests + compute time

### Example Monthly Costs:

| Usage Level | Requests/Month | Estimated Cost |
|------------|----------------|----------------|
| **Personal** | 1,000 | **FREE** |
| **Small Business** | 10,000 | ~$0.50 |
| **Medium Business** | 100,000 | ~$5.00 |
| **Enterprise** | 1,000,000 | ~$50.00 |

*Much cheaper than always-on servers!*

---

## 🔧 Configuration

### Environment Variables:
- `STAGE`: Deployment stage (dev/staging/prod)
- `OPENAI_API_KEY`: Your OpenAI API key
- `AWS_REGION`: AWS deployment region

### Memory & Timeout Settings:
- **Memory**: 2048 MB (adjustable in `template.yaml`)
- **Timeout**: 300 seconds (5 minutes max)
- **Runtime**: Python 3.11

---

## 📊 Monitoring & Logs

### CloudWatch Integration:
```bash
# View logs
aws logs describe-log-groups --log-group-name-prefix /aws/lambda/moses

# Monitor metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Duration \
  --dimensions Name=FunctionName,Value=moses-ai-assistant-prod-MosesAIAssistantFunction
```

### Key Metrics to Monitor:
- **Invocations**: Request count
- **Duration**: Response time
- **Errors**: Failed requests
- **Throttles**: Rate limiting events

---

## 🔒 Security Features

- ✅ **HTTPS Only**: API Gateway enforces SSL
- ✅ **CORS Configured**: Cross-origin requests allowed
- ✅ **IAM Roles**: Principle of least privilege
- ✅ **VPC Support**: Network isolation (optional)
- ✅ **Environment Variables**: Encrypted secrets
- ✅ **Security Scanning**: Automated in CI/CD

---

## 🚦 Environments

### Staging Environment:
- **Trigger**: Push to `develop` branch
- **Stack**: `moses-ai-assistant-staging`
- **Purpose**: Testing before production

### Production Environment:
- **Trigger**: Push to `main` branch  
- **Stack**: `moses-ai-assistant-prod`
- **Purpose**: Live API for users

---

## 🛠️ Troubleshooting

### Common Issues:

#### Cold Start Delays
```bash
# Warm up the function
curl https://your-api-url/health
```

#### Memory Errors
Update `MemorySize` in `template.yaml`:
```yaml
MemorySize: 3008  # Increase if needed
```

#### Timeout Issues
Update `Timeout` in `template.yaml`:
```yaml
Timeout: 300  # Max 15 minutes
```

#### Permission Errors
Check IAM roles and policies in AWS Console.

### Debug Commands:
```bash
# Check stack status
aws cloudformation describe-stacks --stack-name moses-ai-assistant-prod

# View function logs
sam logs -n MosesAIAssistantFunction --stack-name moses-ai-assistant-prod --tail

# Test locally
sam local start-api
curl http://localhost:3000/health
```

---

## 🔄 Updates & Maintenance

### Update Deployment:
```bash
# Make changes to your code
git add .
git commit -m "Update AI assistant"
git push origin main  # Triggers automatic deployment
```

### Delete Stack:
```bash
aws cloudformation delete-stack --stack-name moses-ai-assistant-prod
```

---

## 📈 Scaling Considerations

### Concurrent Executions:
- **Default Limit**: 1,000 concurrent executions
- **Increase Limit**: Contact AWS support

### Performance Optimization:
- Use **Provisioned Concurrency** for consistent performance
- Optimize **memory allocation** based on usage
- Implement **connection pooling** for databases

---

## 🎯 Next Steps

1. **✅ Deploy**: Use GitHub Actions or manual deployment
2. **📱 Frontend Integration**: Connect your frontend to the API
3. **📊 Monitoring**: Set up CloudWatch alarms
4. **🔐 API Keys**: Implement authentication (optional)
5. **🌍 Custom Domain**: Configure Route53 domain (optional)

---

## 📞 Support

- **AWS Documentation**: [Lambda Developer Guide](https://docs.aws.amazon.com/lambda/)
- **SAM Documentation**: [SAM Developer Guide](https://docs.aws.amazon.com/serverless-application-model/)
- **FastAPI + Lambda**: [Mangum Documentation](https://mangum.io/)

---

**🎉 Your AI Assistant is now ready for serverless deployment!** 

The Lambda architecture provides enterprise-grade scalability at a fraction of traditional hosting costs.

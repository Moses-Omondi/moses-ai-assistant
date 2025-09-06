#!/bin/bash

echo "🔑 AWS Credentials Helper for GitHub Secrets"
echo "============================================="
echo ""

# Check if AWS CLI is configured
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI not found. Please install it first:"
    echo "   brew install awscli"
    exit 1
fi

# Check if AWS is configured
if ! aws configure list &> /dev/null; then
    echo "❌ AWS CLI not configured. Run: aws configure"
    exit 1
fi

echo "📋 Current AWS Configuration:"
echo ""

# Get AWS configuration
AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id)
AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key)
AWS_REGION=$(aws configure get region)
AWS_OUTPUT=$(aws configure get output)

if [ -z "$AWS_ACCESS_KEY_ID" ] || [ -z "$AWS_SECRET_ACCESS_KEY" ]; then
    echo "❌ AWS credentials not found in default profile."
    echo ""
    echo "Available profiles:"
    aws configure list-profiles 2>/dev/null || echo "No profiles found"
    echo ""
    read -p "📝 Enter AWS profile name to use [default]: " PROFILE
    PROFILE=${PROFILE:-default}
    
    if [ "$PROFILE" != "default" ]; then
        AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id --profile $PROFILE)
        AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key --profile $PROFILE)
        AWS_REGION=$(aws configure get region --profile $PROFILE)
    fi
fi

if [ -z "$AWS_ACCESS_KEY_ID" ] || [ -z "$AWS_SECRET_ACCESS_KEY" ]; then
    echo "❌ Still can't find AWS credentials. Please run:"
    echo "   aws configure"
    echo ""
    echo "Or manually enter them:"
    echo ""
    read -p "📝 Enter AWS_ACCESS_KEY_ID: " AWS_ACCESS_KEY_ID
    read -p "📝 Enter AWS_SECRET_ACCESS_KEY: " AWS_SECRET_ACCESS_KEY
    read -p "📝 Enter AWS_REGION [us-east-1]: " AWS_REGION
    AWS_REGION=${AWS_REGION:-us-east-1}
fi

# Display credentials
echo ""
echo "✅ Found AWS Credentials:"
echo "   Profile: ${PROFILE:-default}"
echo "   Region:  ${AWS_REGION:-us-east-1}"
echo ""

# Show GitHub Secrets instructions
echo "📋 GitHub Secrets to Add:"
echo "=========================="
echo ""
echo "Go to your repository → Settings → Secrets and variables → Actions"
echo "Add these secrets:"
echo ""
echo "🔑 Secret Name: AWS_ACCESS_KEY_ID"
echo "📄 Secret Value:"
echo "$AWS_ACCESS_KEY_ID"
echo ""
echo "🔑 Secret Name: AWS_SECRET_ACCESS_KEY" 
echo "📄 Secret Value:"
echo "$AWS_SECRET_ACCESS_KEY"
echo ""
echo "🔑 Secret Name: AWS_DEFAULT_REGION (Optional)"
echo "📄 Secret Value:"
echo "${AWS_REGION:-us-east-1}"
echo ""

# Option to test credentials
echo "🧪 Test AWS Credentials? (y/n): "
read -r TEST_CREDS

if [[ $TEST_CREDS =~ ^[Yy]$ ]]; then
    echo ""
    echo "🧪 Testing AWS credentials..."
    
    export AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY_ID"
    export AWS_SECRET_ACCESS_KEY="$AWS_SECRET_ACCESS_KEY"
    export AWS_DEFAULT_REGION="${AWS_REGION:-us-east-1}"
    
    if aws sts get-caller-identity 2>/dev/null; then
        echo "✅ AWS credentials work!"
    else
        echo "❌ AWS credentials test failed!"
    fi
fi

echo ""
echo "📋 Quick Copy Commands:"
echo "======================="
echo ""
echo "# Copy these one by one:"
echo "echo '$AWS_ACCESS_KEY_ID' | pbcopy"
echo "echo '$AWS_SECRET_ACCESS_KEY' | pbcopy"
echo ""

# Save to temporary file for easy access
cat > /tmp/aws-github-secrets.txt << EOF
GitHub Secrets for moses-ai-assistant repository:

AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
AWS_DEFAULT_REGION=${AWS_REGION:-us-east-1}

Repository URL: https://github.com/Moses-Omondi/moses-ai-assistant
Settings URL: https://github.com/Moses-Omondi/moses-ai-assistant/settings/secrets/actions
EOF

echo "💾 Credentials saved to: /tmp/aws-github-secrets.txt"
echo ""
echo "🎯 Next Steps:"
echo "   1. Create GitHub repository: https://github.com/new"
echo "   2. Add the secrets above to your repository"
echo "   3. Run: ./setup-github.sh"
echo "   4. Watch your Lambda deployment! 🚀"

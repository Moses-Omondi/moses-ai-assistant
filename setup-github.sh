#!/bin/bash

echo "🚀 Moses AI Assistant - GitHub Setup & Deploy"
echo "============================================="
echo ""

# Get GitHub username
read -p "📝 Enter your GitHub username: " GITHUB_USERNAME

# Validate username
if [ -z "$GITHUB_USERNAME" ]; then
    echo "❌ GitHub username cannot be empty!"
    exit 1
fi

# Get repository name (with default)
echo ""
read -p "📝 Enter repository name [moses-ai-assistant]: " REPO_NAME
REPO_NAME=${REPO_NAME:-moses-ai-assistant}

# Show what we'll do
echo ""
echo "📋 Configuration Summary:"
echo "   GitHub User: $GITHUB_USERNAME"
echo "   Repository:  $REPO_NAME"
echo "   Remote URL:  https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
echo ""

# Confirm
read -p "✅ Is this correct? (y/n): " CONFIRM
if [[ $CONFIRM != [yY] ]]; then
    echo "❌ Setup cancelled."
    exit 1
fi

echo ""
echo "🔧 Setting up GitHub remote..."

# Remove existing remote if it exists
git remote remove origin 2>/dev/null || true

# Add new remote
git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"

echo "✅ Remote added successfully!"
echo ""

# Check if repo exists
echo "🔍 Checking if repository exists..."
if git ls-remote origin HEAD &>/dev/null; then
    echo "✅ Repository found!"
else
    echo "⚠️  Repository not found. Please create it first:"
    echo "   1. Go to: https://github.com/new"
    echo "   2. Repository name: $REPO_NAME"
    echo "   3. Don't initialize with README/gitignore"
    echo "   4. Click 'Create repository'"
    echo ""
    read -p "📝 Press Enter after creating the repository..."
fi

echo ""
echo "🚀 Pushing code to GitHub..."

# Push to GitHub
git branch -M main
if git push -u origin main; then
    echo ""
    echo "🎉 SUCCESS! Code pushed to GitHub!"
    echo ""
    echo "🔗 Repository URL: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
    echo "🔗 Actions URL:    https://github.com/$GITHUB_USERNAME/$REPO_NAME/actions"
    echo ""
    echo "📋 Next Steps:"
    echo "   1. Add GitHub Secrets in repository settings:"
    echo "      • AWS_ACCESS_KEY_ID"
    echo "      • AWS_SECRET_ACCESS_KEY"
    echo "   2. Watch your CI/CD pipeline run automatically!"
    echo "   3. Get your Lambda API URL from the deployment logs"
    echo ""
else
    echo ""
    echo "❌ Push failed! This might happen if:"
    echo "   • Repository doesn't exist yet"
    echo "   • You don't have push permissions"
    echo "   • Network connectivity issues"
    echo ""
    echo "💡 To fix:"
    echo "   1. Create the repository: https://github.com/new"
    echo "   2. Run this script again"
fi

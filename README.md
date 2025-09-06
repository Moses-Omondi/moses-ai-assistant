# Moses AI Assistant - AWS Lambda Backend

## Quick Deploy

### GitHub Actions (Recommended)
```bash
git add .
git commit -m "Deploy Lambda backend"
git push origin main
```

### Manual Deploy
```bash
sam build --use-container
sam deploy --guided
```

## Required GitHub Secrets
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY` 
- `OPENAI_API_KEY`

## API Endpoints
- `GET /` - API info
- `GET /health` - Health check  
- `POST /query` - Ask questions

## Frontend Integration
```javascript
const response = await fetch('https://your-api-url/query', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({question: "Tell me about Moses"})
});
```

See `README_LAMBDA.md` for detailed setup guide.

#!/bin/bash

# Quick Test Script for Honeypot Agent
# Usage: ./quick_test.sh

echo "🔍 Starting Quick Honeypot Agent Test..."
echo ""

# Configuration
API_URL="http://136.116.51.121:8080/api/honey-pot"
API_KEY="your-secret-api-key-here"

# Quick connectivity test
echo "Testing API connectivity..."
response=$(curl -s -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $API_KEY" \
  -d '{
    "sessionId": "quick-test-'$(date +%s)'",
    "message": {
      "sender": "scammer",
      "text": "You won 50000 rupees! Send your UPI ID to claim.",
      "timestamp": '$(date +%s000)'
    },
    "conversationHistory": []
  }')

# Check if response is valid
if echo "$response" | grep -q "success"; then
    echo "✅ API is responding correctly!"
    echo ""
    echo "Response:"
    echo "$response" | python3 -m json.tool
    echo ""
    echo "✨ Your honeypot agent is working!"
else
    echo "❌ API test failed"
    echo "Response: $response"
    exit 1
fi

echo ""
echo "To run full test suite:"
echo "  python honeypot_tester.py"

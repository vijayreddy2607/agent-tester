# Honeypot Agent Tester

Comprehensive testing suite for the **Agentic Honey-Pot for Scam Detection & Intelligence Extraction** system (Problem Statement 2).

## 🎯 What This Tester Does

This testing suite validates your deployed honeypot agent against all requirements from Problem Statement 2:

### Core Tests

1. **API Connectivity** - Verifies the API is reachable and responding
2. **Response Format Validation** - Ensures responses match the required format: `{"status": "success", "reply": "..."}`
3. **API Performance** - Checks response times are under 5 seconds
4. **Scam Detection Accuracy** - Tests with 5 different scam scenarios (UPI, bank, KYC, prize, work-from-home)
5. **False Positive Rate** - Validates the agent doesn't wrongly engage with legitimate messages
6. **Persona Consistency** - Tests if the agent maintains a believable human persona across multiple turns
7. **Human-Like Responses** - Analyzes response quality for natural language characteristics
8. **Intelligence Extraction** - Simulates multi-turn conversations to test data extraction capability
9. **UPI Scam Scenario** - End-to-end test of a complete UPI scam interaction
10. **Phishing Link Scenario** - Tests handling of phishing attempts

## 📋 Requirements

```bash
pip install requests
```

## 🚀 Usage

### Quick Start

```bash
python honeypot_tester.py
```

The tester is pre-configured with your deployment details:
- **URL**: `http://136.116.51.121:8080/api/honey-pot`
- **API Key**: `your-secret-api-key-here`

### Custom Configuration

Edit the configuration section in `honeypot_tester.py`:

```python
# Configuration
BASE_URL = "http://your-deployment-url/api/honey-pot"
API_KEY = "your-api-key"
```

## 📊 Test Output

The tester provides detailed output for each test:

```
================================================================================
  TEST 1: API Connectivity
================================================================================

✅ PASSED - API Connectivity
   Message: Successfully connected to the API
   Response Time: 0.234s
   Details: {
     "endpoint": "http://136.116.51.121:8080/api/honey-pot"
   }
```

### Status Indicators

- ✅ **PASSED** - Test succeeded
- ⚠️  **WARNING** - Test passed but with concerns
- ❌ **FAILED** - Test failed
- ℹ️  **INFO** - Informational message

## 🎯 Evaluation Criteria Covered

### 1. Detection Accuracy (20 points)
- ✅ Tests scam message detection with 5 diverse scenarios
- ✅ Tests false positive rate with legitimate messages
- ✅ Validates the agent doesn't wrongly classify normal messages

### 2. Persona & Believability (25 points)
- ✅ Multi-turn conversation consistency testing
- ✅ Human-like response quality analysis
- ✅ Validates agent doesn't reveal it's automated
- ✅ Checks for natural language patterns

### 3. Intelligence Yield (30 points)
- ✅ Tests extraction of UPI IDs
- ✅ Tests extraction of bank account numbers
- ✅ Tests extraction of phone numbers
- ✅ Tests extraction of phishing links
- ✅ Tests extraction of IFSC codes

### 4. Technical Performance (15 points)
- ✅ Response time measurement
- ✅ API reliability testing
- ✅ Correct response format validation

### 5. Ethics & Constraints (10 points)
- ✅ Validates agent doesn't initiate scams
- ✅ Checks agent doesn't share sensitive information
- ✅ Ensures agent doesn't reveal honeypot identity

## 📈 Understanding Test Results

### Scam Detection Test
- **Target**: ≥80% success rate
- **Warning**: 60-80% success rate
- **Failure**: <60% success rate

### False Positive Test
- **Target**: 0% false positives
- **Warning**: ≤25% false positives
- **Failure**: >25% false positives

### Persona Consistency
- **Target**: ≥80% consistency across conversation
- **Warning**: 60-80% consistency
- **Failure**: <60% consistency

### Response Time
- **Target**: <5 seconds
- **Warning**: 5-10 seconds
- **Failure**: >10 seconds

## 🔍 Test Scenarios Included

### Scam Messages Tested
1. **Prize/Lottery Scam**: "Congratulations! You've won Rs 50,000!"
2. **Bank Verification Scam**: "Your bank account has been locked"
3. **KYC Update Scam**: "Your KYC needs update. Share Aadhar and PAN"
4. **Nigerian Prince Scam**: "I am Nigerian prince..."
5. **Work-from-home Scam**: "Earn 50,000 per month. Send registration fee"

### Legitimate Messages Tested
1. Personal family message
2. Work meeting reminder
3. Birthday wish
4. Casual conversation

## 🎨 Features

- **Comprehensive Coverage**: Tests all aspects from Problem Statement 2
- **Detailed Reporting**: Clear pass/fail/warning indicators with explanations
- **Performance Metrics**: Response time tracking for each test
- **Realistic Scenarios**: Uses authentic Indian scam patterns
- **Multi-turn Testing**: Simulates actual scammer conversations
- **Intelligence Tracking**: Monitors what data the agent extracts

## 📝 Sample Test Output

```
================================================================================
  TEST SUMMARY
================================================================================

Total Tests: 10
✅ Passed: 8
⚠️  Warnings: 2
❌ Failed: 0

Success Rate: 80.0%

✨ Great! All tests passed with some warnings. Review warnings for optimization.
```

## 🐛 Troubleshooting

### Connection Errors
- Verify the deployment URL is correct and accessible
- Check if the API key matches your deployment
- Ensure the server is running

### Timeout Errors
- Increase timeout in `send_message()` method
- Check if your deployment has sufficient resources
- Verify network connectivity

### Format Errors
- Ensure your API returns `{"status": "success", "reply": "..."}`
- Check for any additional fields that might break parsing
- Validate JSON format is correct

## 🔄 Next Steps

After running the tests:

1. **Review Failed Tests**: Focus on any ❌ failed tests first
2. **Optimize Warnings**: Address ⚠️ warnings to improve performance
3. **Analyze Intelligence Extraction**: Check if the agent is successfully extracting scammer data
4. **Improve Persona**: If consistency tests fail, enhance the persona system
5. **Reduce Response Time**: If performance warnings appear, optimize your LLM calls

## 📞 Support

For issues or questions about the tester, review:
- Test output details
- Your agent's logs at the deployment
- Problem Statement 2 requirements in the Google Doc

---

**Built for**: GUVI Hackathon - Problem Statement 2  
**Target**: Agentic Honey-Pot for Scam Detection & Intelligence Extraction

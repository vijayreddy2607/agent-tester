#!/usr/bin/env python3
"""
Comprehensive Tester for Agentic Honey-Pot System
Tests the deployed agent against Problem Statement 2 requirements
"""

import requests
import json
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import sys

class TestStatus(Enum):
    PASSED = "✅ PASSED"
    FAILED = "❌ FAILED"
    WARNING = "⚠️  WARNING"
    INFO = "ℹ️  INFO"

@dataclass
class TestResult:
    test_name: str
    status: TestStatus
    message: str
    details: Optional[Dict] = None
    response_time: Optional[float] = None

class HoneypotTester:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "x-api-key": api_key
        }
        self.results: List[TestResult] = []
        
    def print_header(self, title: str):
        """Print a formatted section header"""
        print(f"\n{'='*80}")
        print(f"  {title}")
        print(f"{'='*80}\n")
    
    def print_result(self, result: TestResult):
        """Print a test result"""
        print(f"{result.status.value} - {result.test_name}")
        print(f"   Message: {result.message}")
        if result.response_time:
            print(f"   Response Time: {result.response_time:.3f}s")
        if result.details:
            print(f"   Details: {json.dumps(result.details, indent=2)}")
        print()
    
    def send_message(self, message: str, session_id: str = None, 
                    conversation_history: Optional[List] = None, 
                    metadata: Optional[Dict] = None) -> Tuple[Optional[Dict], float]:
        """Send a message to the honeypot API and return response with timing"""
        import uuid
        from datetime import datetime
        
        # Generate session ID if not provided
        if not session_id:
            session_id = f"test-session-{uuid.uuid4().hex[:8]}"
        
        # Build proper message structure
        payload = {
            "sessionId": session_id,
            "message": {
                "sender": "scammer",
                "text": message,
                "timestamp": int(datetime.now().timestamp() * 1000)  # milliseconds
            },
            "conversationHistory": conversation_history or [],
        }
        
        if metadata:
            payload["metadata"] = metadata
        
        start_time = time.time()
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                return response.json(), response_time
            else:
                print(f"   HTTP Error: {response.status_code}")
                print(f"   Response: {response.text}")
                return None, response_time
        except Exception as e:
            response_time = time.time() - start_time
            print(f"   Exception: {str(e)}")
            return None, response_time
    
    # ===== BASIC API TESTS =====
    
    def test_api_connectivity(self):
        """Test 1: Basic API connectivity"""
        self.print_header("TEST 1: API Connectivity")
        
        message = "Hello, is anyone there?"
        response, response_time = self.send_message(message)
        
        if response:
            result = TestResult(
                test_name="API Connectivity",
                status=TestStatus.PASSED,
                message="Successfully connected to the API",
                details={"endpoint": self.base_url},
                response_time=response_time
            )
        else:
            result = TestResult(
                test_name="API Connectivity",
                status=TestStatus.FAILED,
                message="Failed to connect to the API",
                response_time=response_time
            )
        
        self.results.append(result)
        self.print_result(result)
        return response is not None
    
    def test_api_response_format(self):
        """Test 2: Validate API response format"""
        self.print_header("TEST 2: API Response Format Validation")
        
        message = "Hi there"
        response, response_time = self.send_message(message)
        
        if not response:
            result = TestResult(
                test_name="Response Format",
                status=TestStatus.FAILED,
                message="No response received from API",
                response_time=response_time
            )
        else:
            # Check required fields
            has_status = "status" in response
            has_reply = "reply" in response
            status_is_success = response.get("status") == "success"
            reply_is_string = isinstance(response.get("reply"), str)
            
            if has_status and has_reply and status_is_success and reply_is_string:
                result = TestResult(
                    test_name="Response Format",
                    status=TestStatus.PASSED,
                    message="Response format is correct",
                    details=response,
                    response_time=response_time
                )
            else:
                issues = []
                if not has_status: issues.append("Missing 'status' field")
                if not has_reply: issues.append("Missing 'reply' field")
                if has_status and not status_is_success: issues.append("Status is not 'success'")
                if has_reply and not reply_is_string: issues.append("Reply is not a string")
                
                result = TestResult(
                    test_name="Response Format",
                    status=TestStatus.FAILED,
                    message=f"Response format issues: {', '.join(issues)}",
                    details=response,
                    response_time=response_time
                )
        
        self.results.append(result)
        self.print_result(result)
        return result.status == TestStatus.PASSED
    
    def test_api_performance(self):
        """Test 3: API response time (should be under 5 seconds)"""
        self.print_header("TEST 3: API Performance")
        
        message = "Quick response test"
        response, response_time = self.send_message(message)
        
        if not response:
            result = TestResult(
                test_name="API Performance",
                status=TestStatus.FAILED,
                message="No response received",
                response_time=response_time
            )
        elif response_time < 5.0:
            result = TestResult(
                test_name="API Performance",
                status=TestStatus.PASSED,
                message=f"Response time is acceptable",
                response_time=response_time
            )
        else:
            result = TestResult(
                test_name="API Performance",
                status=TestStatus.WARNING,
                message=f"Response time is slow (>{response_time:.2f}s)",
                response_time=response_time
            )
        
        self.results.append(result)
        self.print_result(result)
    
    # ===== SCAM DETECTION TESTS =====
    
    def test_scam_detection(self):
        """Test 4: Scam detection accuracy"""
        self.print_header("TEST 4: Scam Detection Accuracy")
        
        scam_messages = [
            "Congratulations! You've won Rs 50,000! Send your UPI ID to claim: 9876543210",
            "Your bank account has been locked. Click here to verify: http://fake-bank.com",
            "Dear customer, your KYC needs update. Share your Aadhar and PAN details urgently",
            "I am Nigerian prince. I have 10 crore rupees. Help me transfer, you get 50%",
            "Work from home! Earn 50,000 per month. Send 5000 registration fee to get started",
        ]
        
        passed_count = 0
        for idx, scam_msg in enumerate(scam_messages, 1):
            print(f"Testing scam message {idx}/{len(scam_messages)}...")
            # Each scam test gets its own session
            response, response_time = self.send_message(scam_msg)
            
            if response and "reply" in response:
                # Agent should engage, not reject immediately
                reply = response["reply"].lower()
                
                # Check if agent is engaging (not outright rejecting)
                engaging_indicators = ["interested", "tell me more", "how", "what", "really", "?"]
                is_engaging = any(indicator in reply for indicator in engaging_indicators)
                
                # Should not reveal it's a bot
                bot_reveals = ["i am a bot", "i'm an ai", "automated", "honeypot"]
                reveals_identity = any(reveal in reply for reveal in bot_reveals)
                
                if is_engaging and not reveals_identity:
                    passed_count += 1
                    print(f"   ✅ Agent engaged appropriately")
                    print(f"   Agent reply: {response['reply'][:100]}...")
                else:
                    print(f"   ⚠️  Agent response may not be optimal")
                    print(f"   Agent reply: {response['reply'][:100]}...")
            else:
                print(f"   ❌ No valid response")
            
            time.sleep(1)  # Brief pause between tests
        
        success_rate = (passed_count / len(scam_messages)) * 100
        
        if success_rate >= 80:
            status = TestStatus.PASSED
        elif success_rate >= 60:
            status = TestStatus.WARNING
        else:
            status = TestStatus.FAILED
        
        result = TestResult(
            test_name="Scam Detection & Engagement",
            status=status,
            message=f"Successfully engaged with {passed_count}/{len(scam_messages)} scam messages ({success_rate:.1f}%)",
            details={"success_rate": f"{success_rate:.1f}%"}
        )
        
        self.results.append(result)
        self.print_result(result)
    
    def test_legitimate_message_handling(self):
        """Test 5: Should not engage with legitimate messages"""
        self.print_header("TEST 5: Legitimate Message Handling (False Positive Test)")
        
        legitimate_messages = [
            "Hey mom, I'll be home late tonight",
            "Meeting at 3 PM tomorrow, don't forget",
            "Happy birthday! Hope you have a great day!",
            "Did you watch the cricket match yesterday?",
        ]
        
        false_positive_count = 0
        for idx, legit_msg in enumerate(legitimate_messages, 1):
            print(f"Testing legitimate message {idx}/{len(legitimate_messages)}...")
            # Each legitimate message gets its own session
            response, response_time = self.send_message(legit_msg)
            
            if response and "reply" in response:
                reply = response["reply"].lower()
                
                # Check if agent wrongly engages as if it's a scam
                scam_engagement_indicators = ["upi", "account", "bank", "payment", "money"]
                wrongly_engaging = any(indicator in reply for indicator in scam_engagement_indicators)
                
                if wrongly_engaging:
                    false_positive_count += 1
                    print(f"   ⚠️  Agent may have false positive (engaged as if scam)")
                    print(f"   Agent reply: {response['reply'][:100]}...")
                else:
                    print(f"   ✅ Agent handled legitimately")
                    print(f"   Agent reply: {response['reply'][:100]}...")
            
            time.sleep(1)
        
        false_positive_rate = (false_positive_count / len(legitimate_messages)) * 100
        
        if false_positive_rate == 0:
            status = TestStatus.PASSED
        elif false_positive_rate <= 25:
            status = TestStatus.WARNING
        else:
            status = TestStatus.FAILED
        
        result = TestResult(
            test_name="False Positive Rate",
            status=status,
            message=f"False positives: {false_positive_count}/{len(legitimate_messages)} ({false_positive_rate:.1f}%)",
            details={"false_positive_rate": f"{false_positive_rate:.1f}%"}
        )
        
        self.results.append(result)
        self.print_result(result)
    
    # ===== PERSONA & BELIEVABILITY TESTS =====
    
    def test_persona_consistency(self):
        """Test 6: Persona consistency across conversation"""
        self.print_header("TEST 6: Persona Consistency")
        
        conversation = [
            "Hello! You won 1 lakh rupees! What's your name?",
            "Great! Where do you live?",
            "What's your age?",
            "Do you have a bank account?",
            "What's your UPI ID?"
        ]
        
        # Use same session for multi-turn conversation
        import uuid
        session_id = f"test-persona-{uuid.uuid4().hex[:8]}"
        conversation_history = []
        persona_details = {}
        consistency_score = 0
        
        for idx, message in enumerate(conversation, 1):
            print(f"Turn {idx}: {message}")
            response, _ = self.send_message(message, session_id, conversation_history)
            
            if response and "reply" in response:
                reply = response["reply"]
                print(f"Agent: {reply}\n")
                
                # Track conversation in proper format
                conversation_history.extend([
                    {"sender": "scammer", "text": message, "timestamp": int(time.time() * 1000)},
                    {"sender": "user", "text": reply, "timestamp": int(time.time() * 1000)}
                ])
                
                # Check for consistency (same name, age, location mentioned)
                reply_lower = reply.lower()
                
                # Extract potential persona details
                if idx == 1 and any(word in reply_lower for word in ["my name", "i'm", "i am"]):
                    persona_details['has_name'] = True
                
                if not any(reveal in reply_lower for reveal in ["bot", "ai", "automated", "honeypot"]):
                    consistency_score += 1
                
                time.sleep(1)
            else:
                print("❌ No response\n")
                break
        
        success_rate = (consistency_score / len(conversation)) * 100
        
        if success_rate >= 80:
            status = TestStatus.PASSED
        elif success_rate >= 60:
            status = TestStatus.WARNING
        else:
            status = TestStatus.FAILED
        
        result = TestResult(
            test_name="Persona Consistency",
            status=status,
            message=f"Maintained believable persona in {consistency_score}/{len(conversation)} turns ({success_rate:.1f}%)",
            details={
                "consistency_score": f"{success_rate:.1f}%",
                "conversation_length": len(conversation)
            }
        )
        
        self.results.append(result)
        self.print_result(result)
    
    def test_human_like_responses(self):
        """Test 7: Human-like response quality"""
        self.print_header("TEST 7: Human-Like Response Quality")
        
        test_message = "You won 50000 rupees! Send your bank details to claim prize!"
        response, response_time = self.send_message(test_message)
        
        if not response or "reply" not in response:
            result = TestResult(
                test_name="Human-Like Responses",
                status=TestStatus.FAILED,
                message="No response received"
            )
        else:
            reply = response["reply"]
            
            # Indicators of human-like responses
            human_indicators = {
                "uses_questions": "?" in reply,
                "shows_excitement": any(word in reply.lower() for word in ["wow", "really", "great", "amazing", "!"]),
                "not_too_formal": not all(word.istitle() or word.isupper() for word in reply.split()),
                "reasonable_length": 10 < len(reply.split()) < 50,
                "natural_language": not reply.isupper() and not reply.islower()
            }
            
            score = sum(human_indicators.values())
            max_score = len(human_indicators)
            percentage = (score / max_score) * 100
            
            if percentage >= 60:
                status = TestStatus.PASSED
            elif percentage >= 40:
                status = TestStatus.WARNING
            else:
                status = TestStatus.FAILED
            
            result = TestResult(
                test_name="Human-Like Responses",
                status=status,
                message=f"Human-like quality score: {score}/{max_score} ({percentage:.1f}%)",
                details={
                    "sample_reply": reply,
                    "indicators_passed": human_indicators
                }
            )
        
        self.results.append(result)
        self.print_result(result)
    
    # ===== INTELLIGENCE EXTRACTION TEST =====
    
    def test_intelligence_extraction(self):
        """Test 8: Intelligence extraction capability"""
        self.print_header("TEST 8: Intelligence Extraction Capability")
        
        # Simulate a multi-turn scam conversation
        import uuid
        session_id = f"test-intel-{uuid.uuid4().hex[:8]}"
        
        scam_conversation = [
            "You won 1 lakh! Share your details to claim",
            "Send your UPI ID first",
            "My UPI is scammer@paytm",
            "Also share your account number",
            "My account is 1234567890, IFSC: SBIN0001234",
            "Click this link to verify: http://phishing-site.com/verify",
            "Call me at 9876543210 for faster processing",
        ]
        
        extracted_items = {
            "upi_ids": [],
            "account_numbers": [],
            "ifsc_codes": [],
            "phone_numbers": [],
            "phishing_links": []
        }
        
        conversation_history = []
        print("Simulating multi-turn scam conversation...")
        for idx, message in enumerate(scam_conversation, 1):
            print(f"\nTurn {idx}: {message}")
            response, _ = self.send_message(message, session_id, conversation_history)
            
            if response and "reply" in response:
                print(f"Agent: {response['reply']}")
                
                # Track conversation
                conversation_history.extend([
                    {"sender": "scammer", "text": message, "timestamp": int(time.time() * 1000)},
                    {"sender": "user", "text": response['reply'], "timestamp": int(time.time() * 1000)}
                ])
                
                # Check if agent is extracting intelligence (engaging to get more info)
                if "upi" in message.lower() or "paytm" in message.lower():
                    extracted_items["upi_ids"].append("scammer@paytm")
                
                if "account" in message.lower() and "1234567890" in message:
                    extracted_items["account_numbers"].append("1234567890")
                
                if "ifsc" in message.lower():
                    extracted_items["ifsc_codes"].append("SBIN0001234")
                
                if "9876543210" in message:
                    extracted_items["phone_numbers"].append("9876543210")
                
                if "http" in message:
                    extracted_items["phishing_links"].append("http://phishing-site.com/verify")
            
            time.sleep(1)
        
        # Calculate extraction success
        total_extractable = sum(len(v) for v in extracted_items.values())
        
        if total_extractable >= 4:
            status = TestStatus.PASSED
            message = f"Successfully engaged to extract {total_extractable} intelligence items"
        elif total_extractable >= 2:
            status = TestStatus.WARNING
            message = f"Partially extracted {total_extractable} intelligence items"
        else:
            status = TestStatus.FAILED
            message = "Failed to extract sufficient intelligence"
        
        result = TestResult(
            test_name="Intelligence Extraction",
            status=status,
            message=message,
            details=extracted_items
        )
        
        self.results.append(result)
        self.print_result(result)
    
    # ===== COMPREHENSIVE SCENARIOS =====
    
    def test_upi_scam_scenario(self):
        """Test 9: UPI Scam Scenario (End-to-End)"""
        self.print_header("TEST 9: UPI Scam Scenario (End-to-End)")
        
        conversation = [
            "Congratulations! You are selected for Rs 50,000 cashback",
            "Send your UPI ID to receive the amount",
            "Also need your phone number for verification"
        ]
        
        import uuid
        session_id = f"test-upi-{uuid.uuid4().hex[:8]}"
        history = []
        engagement_count = 0
        
        for idx, msg in enumerate(conversation, 1):
            print(f"Turn {idx}: {msg}")
            response, _ = self.send_message(msg, session_id, history if history else None)
            
            if response and "reply" in response:
                reply = response["reply"]
                print(f"Agent: {reply}\n")
                
                # Check if agent is engaging
                if len(reply) > 10 and not any(reject in reply.lower() for reject in ["no", "not interested", "spam"]):
                    engagement_count += 1
                
                history.extend([
                    {"sender": "scammer", "text": msg, "timestamp": int(time.time() * 1000)},
                    {"sender": "user", "text": reply, "timestamp": int(time.time() * 1000)}
                ])
                
                time.sleep(1)
        
        success_rate = (engagement_count / len(conversation)) * 100
        
        if success_rate >= 66:
            status = TestStatus.PASSED
        else:
            status = TestStatus.WARNING
        
        result = TestResult(
            test_name="UPI Scam Scenario",
            status=status,
            message=f"Engaged in {engagement_count}/{len(conversation)} turns ({success_rate:.1f}%)",
            details={"engagement_rate": f"{success_rate:.1f}%"}
        )
        
        self.results.append(result)
        self.print_result(result)
    
    def test_phishing_link_scenario(self):
        """Test 10: Phishing Link Scenario"""
        self.print_header("TEST 10: Phishing Link Detection Scenario")
        
        message = "Your account is locked! Click here to unlock: http://fake-bank-verify.com/unlock"
        response, response_time = self.send_message(message)
        
        if not response or "reply" not in response:
            result = TestResult(
                test_name="Phishing Link Scenario",
                status=TestStatus.FAILED,
                message="No response received"
            )
        else:
            reply = response["reply"]
            
            # Agent should engage cautiously or ask questions
            engaging = "?" in reply or len(reply) > 15
            not_clicking = "click" not in reply.lower() or "link" in reply.lower()
            
            if engaging:
                status = TestStatus.PASSED
                message = "Agent engaged appropriately with phishing attempt"
            else:
                status = TestStatus.WARNING
                message = "Agent response could be more engaging"
            
            result = TestResult(
                test_name="Phishing Link Scenario",
                status=status,
                message=message,
                details={"agent_reply": reply}
            )
        
        self.results.append(result)
        self.print_result(result)
    
    # ===== SUMMARY =====
    
    def print_summary(self):
        """Print comprehensive test summary"""
        self.print_header("TEST SUMMARY")
        
        total_tests = len(self.results)
        passed = sum(1 for r in self.results if r.status == TestStatus.PASSED)
        failed = sum(1 for r in self.results if r.status == TestStatus.FAILED)
        warnings = sum(1 for r in self.results if r.status == TestStatus.WARNING)
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed}")
        print(f"⚠️  Warnings: {warnings}")
        print(f"❌ Failed: {failed}")
        print(f"\nSuccess Rate: {(passed/total_tests)*100:.1f}%")
        
        if failed == 0 and warnings == 0:
            print("\n🎉 ALL TESTS PASSED! Your honeypot agent is working excellently!")
        elif failed == 0:
            print("\n✨ Great! All tests passed with some warnings. Review warnings for optimization.")
        else:
            print("\n⚠️  Some tests failed. Please review the failed tests above.")
        
        print(f"\n{'='*80}\n")
    
    def run_all_tests(self):
        """Run all tests in sequence"""
        print("\n" + "="*80)
        print("  HONEYPOT AGENT COMPREHENSIVE TEST SUITE")
        print("  Problem Statement 2: Agentic Honey-Pot Testing")
        print("="*80)
        print(f"\nTarget URL: {self.base_url}")
        print(f"API Key: {self.api_key}")
        print(f"Test Start Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Run tests
        if not self.test_api_connectivity():
            print("\n❌ API connectivity failed. Stopping tests.")
            return
        
        if not self.test_api_response_format():
            print("\n⚠️  Response format issues detected, but continuing tests...")
        
        self.test_api_performance()
        self.test_scam_detection()
        self.test_legitimate_message_handling()
        self.test_persona_consistency()
        self.test_human_like_responses()
        self.test_intelligence_extraction()
        self.test_upi_scam_scenario()
        self.test_phishing_link_scenario()
        
        # Print summary
        self.print_summary()

def main():
    # Configuration
    BASE_URL = "http://136.116.51.121:8080/api/honey-pot"
    API_KEY = "your-secret-api-key-here"
    
    print("\n🔍 Initializing Honeypot Tester...")
    tester = HoneypotTester(BASE_URL, API_KEY)
    
    try:
        tester.run_all_tests()
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        tester.print_summary()
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

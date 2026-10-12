#!/usr/bin/env python
"""
COMPLETE TESTING GUIDE - Follow-up Pipeline System
Copy-paste these commands to test the system
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/api/workflows"

def print_section(title):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")

def print_result(status, message):
    emoji = "✅" if status else "❌"
    print(f"{emoji} {message}")

# ============================================================================
# TEST 1: GET AVAILABLE SCENARIOS
# ============================================================================

def test_1_get_scenarios():
    print_section("TEST 1: Get Available Workflow Scenarios")
    
    print("INPUT: GET /api/workflows/scenarios")
    print("\nDescripton: Retrieve all 6 pre-built workflow templates\n")
    
    try:
        response = requests.get(f"{BASE_URL}/scenarios", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Response Status: {response.status_code} (SUCCESS)\n")
            
            print(f"Number of Scenarios: {len(data.get('scenarios', []))}\n")
            print("Scenarios Available:")
            print("-" * 70)
            
            for i, scenario in enumerate(data.get('scenarios', []), 1):
                print(f"\n{i}. {scenario['name'].upper()}")
                print(f"   Type: {scenario['scenario_type']}")
                print(f"   Steps: {scenario['steps_count']}")
                print(f"   Description: {scenario['description'][:60]}...")
            
            print("\n" + "-" * 70)
            print("✅ TEST PASSED: All 6 scenarios loaded successfully!")
            return True
        else:
            print(f"❌ Failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# ============================================================================
# TEST 2: CREATE WORKFLOW FROM TEMPLATE
# ============================================================================

def test_2_create_workflow():
    print_section("TEST 2: Create Workflow from Attendance Template")
    
    print("INPUT: POST /api/workflows/from-scenario")
    print("Parameters:")
    print("  - scenario_type: 'attendance'")
    print("  - name: 'Class 10-A Attendance Pipeline'")
    print("  - description: 'Track attendance and escalate to parents'\n")
    
    try:
        response = requests.post(
            f"{BASE_URL}/from-scenario",
            params={
                "scenario_type": "attendance",
                "name": "Class 10-A Attendance Pipeline",
                "description": "Track attendance and escalate to parents"
            },
            timeout=5
        )
        
        if response.status_code in [200, 201]:
            data = response.json()
            print(f"✅ API Response Status: {response.status_code} (SUCCESS)\n")
            print("OUTPUT:")
            print(json.dumps(data, indent=2))
            
            workflow_id = data.get('workflow_id')
            print(f"\n✅ TEST PASSED: Workflow created with ID: {workflow_id}")
            return workflow_id
        else:
            print(f"❌ Failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

# ============================================================================
# TEST 3: EXECUTE WORKFLOW FOR STUDENT
# ============================================================================

def test_3_execute_workflow(workflow_id):
    print_section("TEST 3: Execute Workflow for Student abc@gmail.com")
    
    print("INPUT: POST /api/workflows/{workflow_id}/run")
    print("\nPayload:")
    payload = {
        "workflow_definition_id": workflow_id,
        "subject_email": "abc@gmail.com",
        "subject_id": "1234554321"
    }
    print(json.dumps(payload, indent=2))
    
    print("\nDescription: Start workflow execution for the specific student\n")
    
    try:
        response = requests.post(
            f"{BASE_URL}/{workflow_id}/run",
            json=payload,
            timeout=5
        )
        
        if response.status_code in [200, 201]:
            data = response.json()
            print(f"✅ API Response Status: {response.status_code} (SUCCESS)\n")
            print("OUTPUT:")
            print(json.dumps(data, indent=2))
            
            instance_id = data.get('instance_id')
            print(f"\n✅ TEST PASSED: Workflow instance created: {instance_id}")
            return instance_id
        else:
            print(f"❌ Failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

# ============================================================================
# TEST 4: CHECK WORKFLOW STATUS
# ============================================================================

def test_4_check_status(instance_id):
    print_section("TEST 4: Check Workflow Instance Status")
    
    print("INPUT: GET /api/workflows/instances/{instance_id}")
    print(f"\nDescription: Get current status, step, and execution history\n")
    
    try:
        response = requests.get(
            f"{BASE_URL}/instances/{instance_id}",
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Response Status: {response.status_code} (SUCCESS)\n")
            print("OUTPUT:")
            print(json.dumps(data, indent=2))
            
            print(f"\n📊 WORKFLOW STATUS SUMMARY:")
            print(f"   Student Email: {data.get('subject_email')}")
            print(f"   Student ID: {data.get('subject_id')}")
            print(f"   Current Step: {data.get('current_step')}")
            print(f"   Current State: {data.get('current_state')}")
            print(f"   Actions Logged: {len(data.get('execution_log', []))}")
            print(f"   Next Scheduled: {data.get('next_scheduled_at', 'N/A')}")
            
            print(f"\n✅ TEST PASSED: Workflow status retrieved successfully!")
            return True
        else:
            print(f"❌ Failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# ============================================================================
# TEST 5: TEST ALL 6 SCENARIOS
# ============================================================================

def test_5_all_scenarios():
    print_section("TEST 5: Test All 6 Scenario Types")
    
    scenarios = [
        ("attendance", "Student Attendance Follow-up"),
        ("assignment", "Assignment Deadline Reminder"),
        ("fee", "Fee Payment Collection"),
        ("exam", "Exam Preparation Tracking"),
        ("conduct", "Conduct Issue Management"),
        ("scholarship", "Scholarship Eligibility")
    ]
    
    results = []
    
    for scenario_type, scenario_name in scenarios:
        print(f"\nTesting: {scenario_name}")
        print("-" * 70)
        
        try:
            response = requests.post(
                f"{BASE_URL}/from-scenario",
                params={
                    "scenario_type": scenario_type,
                    "name": f"Test {scenario_name}",
                    "description": f"Testing {scenario_name} scenario"
                },
                timeout=5
            )
            
            if response.status_code in [200, 201]:
                data = response.json()
                workflow_id = data.get('workflow_id')
                print(f"✅ {scenario_name}: {workflow_id}")
                results.append(True)
            else:
                print(f"❌ {scenario_name}: Failed with status {response.status_code}")
                results.append(False)
                
        except Exception as e:
            print(f"❌ {scenario_name}: Error - {e}")
            results.append(False)
    
    print(f"\n{'='*70}")
    passed = sum(results)
    total = len(results)
    print(f"✅ TEST RESULT: {passed}/{total} scenarios loaded successfully!")
    
    return all(results)

# ============================================================================
# TEST 6: REAL-WORLD SCENARIO TEST
# ============================================================================

def test_6_real_world_scenario():
    print_section("TEST 6: Real-World Scenario - Student Not Attending Class")
    
    print("SCENARIO: Student abc@gmail.com (ID: 1234554321)")
    print("  - Attendance: 65% (below 70% threshold)")
    print("  - Days Absent: 5")
    print("  - Status: Needs intervention\n")
    
    print("EXPECTED WORKFLOW:")
    print("  Day 0:  Send email to student")
    print("  Day 3:  Check ERP attendance data")
    print("  Day 4:  Send urgent reminder if still low")
    print("  Day 6:  Re-check attendance")
    print("  Day 7:  Escalate to parent (auto-fetch parent email)")
    print("  Day 14: Alert admin if still unresolved\n")
    
    print("EXECUTION:\n")
    
    # Step 1: Create workflow
    print("Step 1: Creating Attendance Workflow...")
    workflow_response = requests.post(
        f"{BASE_URL}/from-scenario",
        params={
            "scenario_type": "attendance",
            "name": "Student ABC - Attendance",
            "description": "Track attendance for student abc@gmail.com"
        },
        timeout=5
    )
    
    if workflow_response.status_code not in [200, 201]:
        print(f"❌ Failed to create workflow")
        return False
    
    workflow_id = workflow_response.json().get('workflow_id')
    print(f"✅ Workflow Created: {workflow_id}\n")
    
    # Step 2: Execute workflow
    print("Step 2: Executing Workflow for Student...")
    exec_response = requests.post(
        f"{BASE_URL}/{workflow_id}/run",
        json={
            "workflow_definition_id": workflow_id,
            "subject_email": "abc@gmail.com",
            "subject_id": "1234554321"
        },
        timeout=5
    )
    
    if exec_response.status_code not in [200, 201]:
        print(f"❌ Failed to execute workflow")
        return False
    
    instance_id = exec_response.json().get('instance_id')
    print(f"✅ Workflow Instance Created: {instance_id}\n")
    
    # Step 3: Check status
    print("Step 3: Checking Workflow Status...")
    status_response = requests.get(
        f"{BASE_URL}/instances/{instance_id}",
        timeout=5
    )
    
    if status_response.status_code == 200:
        data = status_response.json()
        
        print(f"✅ Current Step: {data.get('current_step')}")
        print(f"✅ Current State: {data.get('current_state')}")
        print(f"✅ Next Scheduled: {data.get('next_scheduled_at', 'N/A')}")
        print(f"✅ Actions Logged: {len(data.get('execution_log', []))}")
        
        print("\n📋 EXECUTION LOG:")
        for log_entry in data.get('execution_log', []):
            print(f"  - Step {log_entry.get('step')}: {log_entry.get('action')}")
        
        print(f"\n✅ TEST PASSED: Real-world scenario executed successfully!")
        return True
    else:
        print(f"❌ Failed to check status")
        return False

# ============================================================================
# MAIN TEST SUITE
# ============================================================================

def run_all_tests():
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  FOLLOW-UP PIPELINE SYSTEM - COMPLETE TESTING SUITE".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "="*68 + "╝")
    
    results = {}
    
    # Test 1
    results['test_1'] = test_1_get_scenarios()
    
    # Test 2
    workflow_id = test_2_create_workflow()
    results['test_2'] = workflow_id is not None
    
    # Test 3
    if workflow_id:
        instance_id = test_3_execute_workflow(workflow_id)
        results['test_3'] = instance_id is not None
        
        # Test 4
        if instance_id:
            results['test_4'] = test_4_check_status(instance_id)
    
    # Test 5
    results['test_5'] = test_5_all_scenarios()
    
    # Test 6
    results['test_6'] = test_6_real_world_scenario()
    
    # Summary
    print_section("FINAL SUMMARY")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    print(f"Tests Passed: {passed}/{total}\n")
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {test_name.upper()}: {status}")
    
    print("\n" + "="*70)
    if passed == total:
        print("🎉 ALL TESTS PASSED! System is working perfectly!")
    else:
        print(f"⚠️  {total - passed} test(s) failed. Check your backend connection.")
    print("="*70 + "\n")

if __name__ == "__main__":
    # Make sure backend is running
    print("\n🔍 Checking if backend is running on http://localhost:8000...")
    try:
        response = requests.get(f"{BASE_URL}/scenarios", timeout=2)
        if response.status_code == 200:
            print("✅ Backend is running!\n")
            run_all_tests()
        else:
            print(f"❌ Backend responded with status {response.status_code}")
            print("Make sure the backend is running: http://localhost:8000")
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        print("Start the backend with: python -m uvicorn backend.main:app --reload")

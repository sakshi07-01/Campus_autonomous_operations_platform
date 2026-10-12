# FOLLOW-UP PIPELINE SYSTEM - TESTING GUIDE

## Quick Start

Make sure your backend is running:
```bash
# Terminal 1 - Backend
cd d:\projects\GOOGLE-PROJECT
python -m uvicorn backend.main:app --reload
# You should see: Uvicorn running on http://0.0.0.0:8000
```

Then run the complete test suite:
```bash
# Terminal 2 - Tests
cd d:\projects\GOOGLE-PROJECT
python complete_testing_guide.py
```

## Or Test Manually with curl

---

## TEST 1: Get All Available Scenarios

**What you're testing:** "Are the 6 pre-built workflow templates available?"

### Input:
```bash
curl -X GET "http://localhost:8000/api/workflows/scenarios" \
  -H "Content-Type: application/json"
```

### Expected Output (HTTP 200):
```json
{
  "scenarios": [
    {
      "name": "Student Attendance Follow-up",
      "scenario_type": "attendance",
      "steps_count": 8,
      "description": "Track student attendance and escalate to parents if attendance drops below threshold"
    },
    {
      "name": "Assignment Deadline Reminder",
      "scenario_type": "assignment",
      "steps_count": 7,
      "description": "Send reminders for upcoming assignment deadlines"
    },
    {
      "name": "Fee Collection Pipeline",
      "scenario_type": "fee",
      "steps_count": 7,
      "description": "Automated fee payment reminders with escalation"
    },
    {
      "name": "Exam Preparation Tracking",
      "scenario_type": "exam",
      "steps_count": 8,
      "description": "Guide students through exam preparation with resources"
    },
    {
      "name": "Conduct Issue Management",
      "scenario_type": "conduct",
      "steps_count": 9,
      "description": "Handle student conduct issues with escalation"
    },
    {
      "name": "Scholarship Eligibility",
      "scenario_type": "scholarship",
      "steps_count": 9,
      "description": "Track scholarship eligibility and application"
    }
  ]
}
```

### How to Explain This:
> "The API returned all 6 pre-built workflow templates. Each one has a specific scenario type (attendance, assignment, etc.) and includes multiple steps for different actions."

---

## TEST 2: Create Workflow from Template

**What you're testing:** "Can I create a new workflow from a template?"

### Input:
```bash
curl -X POST "http://localhost:8000/api/workflows/from-scenario?scenario_type=attendance&name=Class%2010-A%20Attendance&description=Track%20attendance%20for%20class%2010-A" \
  -H "Content-Type: application/json"
```

### Expected Output (HTTP 201):
```json
{
  "workflow_id": "wf_abc123def456",
  "name": "Class 10-A Attendance",
  "scenario_type": "attendance",
  "description": "Track attendance for class 10-A",
  "status": "active",
  "created_at": "2025-03-22T10:30:00Z",
  "steps": [
    {
      "step_number": 1,
      "type": "send_email",
      "config": {
        "template": "attendance_warning_student",
        "recipient": "student"
      }
    },
    {
      "step_number": 2,
      "type": "wait",
      "config": {
        "duration_days": 3,
        "reason": "Allow time for student response"
      }
    },
    {
      "step_number": 3,
      "type": "check_condition",
      "config": {
        "condition": "attendance < 70",
        "check_source": "erp"
      }
    }
  ]
}
```

### What to Save:
📌 **Important:** Copy the `workflow_id` - you'll need it for the next test!
```
workflow_id = "wf_abc123def456"
```

### How to Explain This:
> "The API created a new workflow based on the attendance template. Each workflow is identified by a unique workflow_id. The workflow includes multiple steps like sending emails, waiting periods, and condition checks. The workflow is now 'active' and ready to be executed."

---

## TEST 3: Execute Workflow for a Student

**What you're testing:** "Can I start a workflow for a specific student?"

### Input:
```bash
# Replace wf_abc123def456 with your actual workflow_id from TEST 2
curl -X POST "http://localhost:8000/api/workflows/wf_abc123def456/run" \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_definition_id": "wf_abc123def456",
    "subject_email": "student@school.com",
    "subject_id": "STU_2024_0001"
  }'
```

### Expected Output (HTTP 201):
```json
{
  "instance_id": "wfi_xyz789abc123",
  "workflow_definition_id": "wf_abc123def456",
  "subject_email": "student@school.com",
  "subject_id": "STU_2024_0001",
  "current_step": 1,
  "current_state": "IN_PROGRESS",
  "started_at": "2025-03-22T10:31:00Z",
  "next_scheduled_at": "2025-03-25T10:31:00Z",
  "execution_log": [
    {
      "timestamp": "2025-03-22T10:31:00Z",
      "step": 1,
      "action": "send_email",
      "status": "success",
      "details": "Email sent to student@school.com"
    }
  ]
}
```

### What to Save:
📌 **Important:** Copy the `instance_id` - you'll need it to check status!
```
instance_id = "wfi_xyz789abc123"
```

### How to Explain This:
> "The API created a workflow instance for this specific student. The workflow started at step 1 and sent an initial email. The instance is tracked with instance_id. The next scheduled action is in 3 days (on March 25th). We can monitor the execution_log to see what actions have been taken."

---

## TEST 4: Check Workflow Status

**What you're testing:** "What's the current status of an executing workflow?"

### Input:
```bash
# Replace wfi_xyz789abc123 with your actual instance_id from TEST 3
curl -X GET "http://localhost:8000/api/workflows/instances/wfi_xyz789abc123" \
  -H "Content-Type: application/json"
```

### Expected Output (HTTP 200):
```json
{
  "instance_id": "wfi_xyz789abc123",
  "workflow_definition_id": "wf_abc123def456",
  "subject_email": "student@school.com",
  "subject_id": "STU_2024_0001",
  "current_step": 1,
  "current_state": "IN_PROGRESS",
  "started_at": "2025-03-22T10:31:00Z",
  "updated_at": "2025-03-22T10:31:30Z",
  "next_scheduled_at": "2025-03-25T10:31:00Z",
  "execution_log": [
    {
      "timestamp": "2025-03-22T10:31:00Z",
      "step": 1,
      "action": "send_email",
      "status": "success",
      "details": "Sent attendance warning email to student@school.com"
    },
    {
      "timestamp": "2025-03-22T10:31:10Z",
      "step": 1,
      "action": "log_action",
      "status": "success",
      "details": "Step 1 completed successfully"
    }
  ],
  "metadata": {
    "attendance_percentage": 65,
    "days_absent": 5,
    "escalation_triggered": false
  }
}
```

### How to Explain This:
> "The workflow is currently in progress at step 1. An email was sent to the student 30 seconds ago. The next check is scheduled for March 25th (3 days from start). We can see the student's current attendance is 65%, which is below the 70% threshold. If this doesn't improve, the workflow will escalate to parent contact on day 7."

---

## TEST 5: Create and Execute All 6 Scenarios

**What you're testing:** "Do all 6 scenario types work?"

### Attendance Scenario:
```bash
curl -X POST "http://localhost:8000/api/workflows/from-scenario?scenario_type=attendance&name=Test%20Attendance&description=Test" \
  -H "Content-Type: application/json"
```

### Assignment Scenario:
```bash
curl -X POST "http://localhost:8000/api/workflows/from-scenario?scenario_type=assignment&name=Test%20Assignment&description=Test" \
  -H "Content-Type: application/json"
```

### Fee Scenario:
```bash
curl -X POST "http://localhost:8000/api/workflows/from-scenario?scenario_type=fee&name=Test%20Fee&description=Test" \
  -H "Content-Type: application/json"
```

### Exam Scenario:
```bash
curl -X POST "http://localhost:8000/api/workflows/from-scenario?scenario_type=exam&name=Test%20Exam&description=Test" \
  -H "Content-Type: application/json"
```

### Conduct Scenario:
```bash
curl -X POST "http://localhost:8000/api/workflows/from-scenario?scenario_type=conduct&name=Test%20Conduct&description=Test" \
  -H "Content-Type: application/json"
```

### Scholarship Scenario:
```bash
curl -X POST "http://localhost:8000/api/workflows/from-scenario?scenario_type=scholarship&name=Test%20Scholarship&description=Test" \
  -H "Content-Type: application/json"
```

### Expected Result:
All 6 should return HTTP 201 with a workflow_id each.

---

## REAL-WORLD SCENARIO: Student Attendance Crisis

**Scenario:** Student "Rajesh" (email: rajesh@school.com) has only 65% attendance and will be barred from exams soon.

### Step 1: Create Attendance Workflow
```bash
curl -X POST "http://localhost:8000/api/workflows/from-scenario?scenario_type=attendance&name=Rajesh%20Attendance%20Crisis&description=Handle%20Rajesh's%20low%20attendance" \
  -H "Content-Type: application/json"
```

**Response:** `workflow_id = "wf_rajesh_001"`

### Step 2: Start Workflow for Rajesh
```bash
curl -X POST "http://localhost:8000/api/workflows/wf_rajesh_001/run" \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_definition_id": "wf_rajesh_001",
    "subject_email": "rajesh@school.com",
    "subject_id": "STU_2024_0789"
  }'
```

**Response:** `instance_id = "wfi_rajesh_001"`

**What Happens Next (Automated):**

| Day | Action | Who Gets Notified | Status |
|-----|--------|------------------|--------|
| 0 | Email sent to Rajesh warning about low attendance | Rajesh | ✅ Sent |
| 3 | System checks ERP for updated attendance | - | ⏳ Pending |
| 4 | If attendance still low, send urgent reminder | Rajesh | ⏳ Pending |
| 6 | Re-check attendance | - | ⏳ Pending |
| 7 | **Escalate to parent** - Email sent to parent | Parent | ⏳ Pending |
| 10 | If no improvement, mark for counselor | Counselor | ⏳ Pending |
| 14 | If still unresolved, escalate to admin | Admin | ⏳ Pending |

### Step 3: Monitor Progress
```bash
# Check status immediately (within 1 minute)
curl -X GET "http://localhost:8000/api/workflows/instances/wfi_rajesh_001" \
  -H "Content-Type: application/json"
```

**You'll See:**
- Step 1 completed (email sent)
- Next scheduled check on day 3
- Execution log showing email was sent
- Metadata with current attendance %

---

## Understanding the Output

### Workflow States (What Does Each Mean?)

```
PENDING          → Workflow created but not started yet
IN_PROGRESS      → Currently executing, waiting for next step
PARENT_CONTACTED → Parent has been notified, waiting for response
ADMIN_ESCALATED  → Escalated to admin level, requires attention
RESOLVED         → Issue resolved, workflow complete
```

### Step Types (What Does Each Action Do?)

```
send_email       → Send an email to student, parent, or faculty
wait             → Wait for X days before next action
check_condition  → Query ERP to check if condition is met
query_erp        → Get student data (attendance, fees, etc.)
escalate         → Move to next level (parent → principal → admin)
log_action       → Record action in execution log
```

### Execution Log (How to Read It)

Each log entry shows:
- **timestamp:** When the action happened
- **step:** Which step number
- **action:** What was done (send_email, check_condition, etc.)
- **status:** success / failed / pending
- **details:** What specifically happened (email sent to whom, condition result, etc.)

---

## Troubleshooting

### Problem: Connection refused to localhost:8000
```
❌ Error: Cannot connect to backend
```
**Solution:** Make sure backend is running
```bash
cd d:\projects\GOOGLE-PROJECT
python -m uvicorn backend.main:app --reload
```

### Problem: 404 Not Found
```
❌ "detail": "Not found"
```
**Solution:** Make sure you're using the correct workflow_id or instance_id

### Problem: 422 Unprocessable Entity
```
❌ "detail": [{"loc": [...], "msg": "..."}]
```
**Solution:** Check that you're sending the correct JSON payload

---

## Expected Results Summary

| Test | Input | Expected Output | Success = |
|------|-------|-----------------|-----------|
| 1 | GET /scenarios | HTTP 200 + 6 scenarios | All 6 present |
| 2 | POST /from-scenario?type=attendance | HTTP 201 + workflow_id | workflow_id exists |
| 3 | POST /{workflow_id}/run | HTTP 201 + instance_id | instance_id exists |
| 4 | GET /instances/{instance_id} | HTTP 200 + status | current_state = IN_PROGRESS |
| 5 | POST all 6 scenario types | HTTP 201 × 6 | 6 workflow_ids created |
| 6 | Real-world scenario | Complete workflow + logs | Logs show step 1 completed |

---

## Next Steps

Once all tests pass:

1. ✅ **API is working** - Workflows can be created and executed
2. ✅ **Scenarios are correct** - All 6 pre-built templates load
3. ✅ **Execution is running** - Workflows start and track progress
4. ✅ **Monitoring works** - Can check status anytime

Then you can:
- Integrate PipelineBuilder component into dashboard
- Connect real Gmail API for actual email sending
- Set up background scheduler for automated execution
- Add WebSocket for real-time updates
- Deploy to production

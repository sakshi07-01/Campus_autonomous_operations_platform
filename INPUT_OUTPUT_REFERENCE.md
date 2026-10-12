# INPUT/OUTPUT REFERENCE - Complete Cheat Sheet

## All API Endpoints at a Glance

```
GET  /api/workflows/scenarios
POST /api/workflows/from-scenario?scenario_type=X&name=Y&description=Z
GET  /api/workflows
POST /api/workflows/{workflow_id}/run
GET  /api/workflows/{workflow_id}/instances
GET  /api/workflows/instances/{instance_id}
POST /api/workflows/{workflow_id}/instances/{instance_id}/resume
DELETE /api/workflows/{workflow_id}
GET  /api/workflows/health/check
```

---

## ENDPOINT 1: Get All Scenarios

| Property | Value |
|----------|-------|
| **Method** | GET |
| **URL** | http://localhost:8000/api/workflows/scenarios |
| **Headers** | Content-Type: application/json |
| **Body** | (empty) |
| **Status** | 200 |

### INPUT (What You Send):
```
GET /api/workflows/scenarios
```

### OUTPUT (What You Get):
```json
{
  "scenarios": [
    {
      "name": "Student Attendance Follow-up",
      "scenario_type": "attendance",
      "steps_count": 8,
      "description": "Track student attendance and escalate to parents"
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

---

## ENDPOINT 2: Create Workflow from Scenario

| Property | Value |
|----------|-------|
| **Method** | POST |
| **URL** | http://localhost:8000/api/workflows/from-scenario |
| **Query Parameters** | scenario_type, name, description |
| **Body** | (empty) |
| **Status** | 201 |

### INPUT (What You Send):
```
POST /api/workflows/from-scenario?scenario_type=attendance&name=Test%20Workflow&description=Testing
```

### OUTPUT (What You Get):
```json
{
  "workflow_id": "wf_abc123def456",
  "name": "Test Workflow",
  "scenario_type": "attendance",
  "description": "Testing",
  "status": "active",
  "created_at": "2025-03-22T10:30:00Z",
  "total_steps": 8,
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

---

## ENDPOINT 3: Execute Workflow for Student

| Property | Value |
|----------|-------|
| **Method** | POST |
| **URL** | http://localhost:8000/api/workflows/{workflow_id}/run |
| **Headers** | Content-Type: application/json |
| **Body** | JSON with workflow_definition_id, subject_email, subject_id |
| **Status** | 201 |

### INPUT (What You Send):
```json
POST /api/workflows/wf_abc123def456/run
Content-Type: application/json

{
  "workflow_definition_id": "wf_abc123def456",
  "subject_email": "student@school.com",
  "subject_id": "STU_2024_0001"
}
```

### OUTPUT (What You Get):
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

---

## ENDPOINT 4: Get Workflow Instance Status

| Property | Value |
|----------|-------|
| **Method** | GET |
| **URL** | http://localhost:8000/api/workflows/instances/{instance_id} |
| **Headers** | Content-Type: application/json |
| **Body** | (empty) |
| **Status** | 200 |

### INPUT (What You Send):
```
GET /api/workflows/instances/wfi_xyz789abc123
```

### OUTPUT (What You Get):
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
      "details": "Step 1 completed"
    }
  ],
  "metadata": {
    "attendance_percentage": 65,
    "days_absent": 5,
    "escalation_triggered": false,
    "parent_email": "parent@school.com"
  }
}
```

---

## DATA TYPES REFERENCE

### Workflow States (current_state)
```
PENDING           → Created but not started
IN_PROGRESS       → Currently executing
PARENT_CONTACTED  → Parent notification sent, waiting
ADMIN_ESCALATED   → Escalated to administration
RESOLVED          → Workflow completed
```

### Step Types (action in execution_log)
```
send_email        → Email sent to recipient
wait              → Waiting period in progress
check_condition   → Condition evaluated
query_erp         → Data retrieved from ERP
escalate          → Escalated to next level
log_action        → Action logged
```

### Scenario Types (scenario_type parameter)
```
attendance        → Track student attendance
assignment        → Assignment deadline reminders
fee              → Fee payment collection
exam             → Exam preparation tracking
conduct          → Conduct issue management
scholarship      → Scholarship eligibility
```

---

## Complete Real-World Example Walkthrough

### Scenario: Student "Priya" (priya@abc.com, ID: 2024_0234) has low attendance (58%)

### Step 1: Create Attendance Workflow
```bash
INPUT:
POST /api/workflows/from-scenario?scenario_type=attendance&name=Priya%20Attendance&description=Low%20attendance%20follow-up

OUTPUT:
{
  "workflow_id": "wf_priya_001",
  "scenario_type": "attendance",
  "status": "active",
  "total_steps": 8
}
```

**What this means:** "We've created an attendance workflow template. Now we need to execute it for Priya."

---

### Step 2: Execute for Priya
```bash
INPUT:
POST /api/workflows/wf_priya_001/run
{
  "workflow_definition_id": "wf_priya_001",
  "subject_email": "priya@abc.com",
  "subject_id": "2024_0234"
}

OUTPUT:
{
  "instance_id": "wfi_priya_001",
  "current_step": 1,
  "current_state": "IN_PROGRESS",
  "started_at": "2025-03-22T09:00:00Z",
  "next_scheduled_at": "2025-03-25T09:00:00Z",
  "execution_log": [
    {
      "step": 1,
      "action": "send_email",
      "status": "success",
      "details": "Email sent to priya@abc.com"
    }
  ]
}
```

**What this means:** "Workflow started! Step 1 completed (email sent to Priya). Next check is in 3 days."

---

### Step 3: Check Status After 1 Day
```bash
INPUT:
GET /api/workflows/instances/wfi_priya_001

OUTPUT:
{
  "instance_id": "wfi_priya_001",
  "current_step": 1,
  "current_state": "IN_PROGRESS",
  "started_at": "2025-03-22T09:00:00Z",
  "next_scheduled_at": "2025-03-25T09:00:00Z",
  "execution_log": [
    {
      "step": 1,
      "action": "send_email",
      "status": "success",
      "details": "Email sent to priya@abc.com"
    }
  ],
  "metadata": {
    "attendance_percentage": 58,
    "days_absent": 8,
    "escalation_triggered": false
  }
}
```

**What this means:** "Status: still waiting. Email was sent yesterday. Next action in 2 more days (March 25)."

---

### Step 4: Check Status After 3 Days (Day 3)
```bash
INPUT:
GET /api/workflows/instances/wfi_priya_001

OUTPUT:
{
  "instance_id": "wfi_priya_001",
  "current_step": 3,
  "current_state": "IN_PROGRESS",
  "started_at": "2025-03-22T09:00:00Z",
  "next_scheduled_at": "2025-03-29T09:00:00Z",
  "execution_log": [
    {
      "step": 1,
      "action": "send_email",
      "status": "success",
      "details": "Email sent to priya@abc.com"
    },
    {
      "step": 2,
      "action": "wait",
      "status": "success",
      "details": "Waited 3 days"
    },
    {
      "step": 3,
      "action": "check_condition",
      "status": "success",
      "details": "Condition check: attendance is 58% (still < 70%)"
    }
  ],
  "metadata": {
    "attendance_percentage": 58,
    "condition_met": true,
    "escalation_needed": true
  }
}
```

**What this means:** "Condition still true (attendance < 70%). System will now escalate to parent."

---

### Step 5: Check Status After 7 Days (Day 7)
```bash
INPUT:
GET /api/workflows/instances/wfi_priya_001

OUTPUT:
{
  "instance_id": "wfi_priya_001",
  "current_step": 5,
  "current_state": "PARENT_CONTACTED",
  "started_at": "2025-03-22T09:00:00Z",
  "next_scheduled_at": "2025-04-05T09:00:00Z",
  "execution_log": [
    ... (steps 1-4 as before) ...,
    {
      "step": 5,
      "action": "escalate",
      "status": "success",
      "details": "Escalated to parent"
    },
    {
      "step": 6,
      "action": "send_email",
      "status": "success",
      "details": "Email sent to parent@abc.com with attendance report"
    }
  ],
  "metadata": {
    "attendance_percentage": 58,
    "parent_email": "parent@abc.com",
    "parent_contacted_at": "2025-03-29T09:00:00Z",
    "escalation_triggered": true
  }
}
```

**What this means:** "Workflow escalated to parent! Parent email sent with attendance report. Now waiting for parent response."

---

### Step 6: Check Status After 14 Days (Day 14)
```bash
INPUT:
GET /api/workflows/instances/wfi_priya_001

OUTPUT:
{
  "instance_id": "wfi_priya_001",
  "current_step": 8,
  "current_state": "ADMIN_ESCALATED",
  "execution_log": [
    ... (all previous steps) ...,
    {
      "step": 8,
      "action": "escalate",
      "status": "success",
      "details": "Escalated to admin - attendance still 58% despite parent contact"
    },
    {
      "step": 9,
      "action": "send_email",
      "status": "success",
      "details": "Alert sent to principal@abc.com"
    }
  ],
  "metadata": {
    "attendance_percentage": 58,
    "admin_escalated_at": "2025-04-05T09:00:00Z",
    "action_taken_by_admin": "pending"
  }
}
```

**What this means:** "Issue escalated to principal. Workflow waiting for admin action."

---

## Key Fields to Watch

| Field | Meaning | When to Check |
|-------|---------|--------------|
| `current_state` | What level is issue at? | Always, to know escalation status |
| `current_step` | Which step is executing? | To track progress through workflow |
| `next_scheduled_at` | When will next action happen? | To know when to check back |
| `execution_log` | What actions have been taken? | To debug or audit |
| `metadata.attendance_percentage` | Current attendance %, fee status, etc. | To verify data accuracy |
| `metadata.escalation_triggered` | Has this escalated yet? | To know if email sent to parent/admin |

---

## Common Queries by Use Case

### "Is the workflow working?"
Check: `current_state != "PENDING"` and execution_log has entries

### "Has parent been contacted?"
Check: `current_state = "PARENT_CONTACTED"` or `metadata.parent_contacted_at` exists

### "Has this been escalated to admin?"
Check: `current_state = "ADMIN_ESCALATED"` or check execution_log for "escalate to admin"

### "What was the last action taken?"
Look at: Last entry in `execution_log` array

### "When is the next action scheduled?"
Check: `next_scheduled_at` field

### "Is the condition still being met?"
Check: `metadata` fields (attendance_percentage, fees_pending, etc.)

---

## Error Response Examples

### 404 - Workflow Not Found
```json
{
  "detail": "Workflow not found",
  "workflow_id": "wf_nonexistent"
}
```
**Fix:** Use correct workflow_id from CREATE response

### 422 - Invalid Data
```json
{
  "detail": [
    {
      "loc": ["body", "subject_email"],
      "msg": "invalid email format",
      "type": "value_error"
    }
  ]
}
```
**Fix:** Check JSON format, email must be valid

### 500 - Server Error
```json
{
  "detail": "Internal server error",
  "error": "Database connection failed"
}
```
**Fix:** Check if backend is running, database is accessible

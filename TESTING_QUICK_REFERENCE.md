# TESTING QUICK REFERENCE - Copy & Paste Commands

## ⚡ FASTEST WAY TO TEST (30 seconds)

Open PowerShell and run this:

```powershell
cd d:\projects\GOOGLE-PROJECT
python complete_testing_guide.py
```

Wait for results. You'll see:
- ✅ TEST 1: Get Scenarios
- ✅ TEST 2: Create Workflow
- ✅ TEST 3: Execute Workflow
- ✅ TEST 4: Check Status
- ✅ TEST 5: Test All 6 Scenarios
- ✅ TEST 6: Real-World Scenario

If all show ✅, your system works!

---

## 🔧 MANUAL TESTING (Use curl)

### Prerequisite: Make sure backend is running
```bash
cd d:\projects\GOOGLE-PROJECT
python -m uvicorn backend.main:app --reload
```
You should see: `Uvicorn running on http://0.0.0.0:8000`

---

### TEST 1: Get Scenarios (30 seconds)

What: "Do the 6 templates exist?"

```bash
curl -X GET "http://localhost:8000/api/workflows/scenarios" -H "Content-Type: application/json"
```

Expected: HTTP 200, shows 6 scenarios (attendance, assignment, fee, exam, conduct, scholarship)

**How to explain:** "The API returned all 6 pre-built workflow templates available in the system."

---

### TEST 2: Create Workflow (30 seconds)

What: "Can I create a workflow from a template?"

```bash
curl -X POST "http://localhost:8000/api/workflows/from-scenario?scenario_type=attendance&name=Test%20Attendance&description=Testing%20attendance%20scenario" -H "Content-Type: application/json"
```

Expected: HTTP 201, returns workflow_id like `"workflow_id": "wf_12345abc"`

**⭐ SAVE THIS:** Copy the workflow_id for next test

**How to explain:** "The API created a new workflow instance from the attendance template. Each workflow gets a unique ID for tracking."

---

### TEST 3: Execute Workflow (30 seconds)

What: "Can I run a workflow for a specific student?"

IMPORTANT: Replace `wf_12345abc` with your workflow_id from TEST 2

```bash
curl -X POST "http://localhost:8000/api/workflows/wf_12345abc/run" -H "Content-Type: application/json" -d "{\"workflow_definition_id\": \"wf_12345abc\", \"subject_email\": \"student@example.com\", \"subject_id\": \"STU_001\"}"
```

Expected: HTTP 201, returns instance_id like `"instance_id": "wfi_xyz789"`

**⭐ SAVE THIS:** Copy the instance_id for next test

**How to explain:** "The workflow started executing for the specified student. The system created an instance to track this specific execution. Step 1 was completed (email sent)."

---

### TEST 4: Check Status (30 seconds)

What: "What's happening with the workflow right now?"

IMPORTANT: Replace `wfi_xyz789` with your instance_id from TEST 3

```bash
curl -X GET "http://localhost:8000/api/workflows/instances/wfi_xyz789" -H "Content-Type: application/json"
```

Expected: HTTP 200, shows:
- current_step: 1
- current_state: "IN_PROGRESS"
- execution_log: [ { shows what actions were taken } ]

**How to explain:** "The workflow is in progress. Step 1 has completed (email sent). The next step is scheduled for 3 days from now. The execution_log shows exactly what actions have been taken so far."

---

### TEST 5: Quick Test All 6 Scenarios (2 minutes)

```bash
# Attendance
curl -X POST "http://localhost:8000/api/workflows/from-scenario?scenario_type=attendance&name=Test1&description=Test" -H "Content-Type: application/json"

# Assignment
curl -X POST "http://localhost:8000/api/workflows/from-scenario?scenario_type=assignment&name=Test2&description=Test" -H "Content-Type: application/json"

# Fee
curl -X POST "http://localhost:8000/api/workflows/from-scenario?scenario_type=fee&name=Test3&description=Test" -H "Content-Type: application/json"

# Exam
curl -X POST "http://localhost:8000/api/workflows/from-scenario?scenario_type=exam&name=Test4&description=Test" -H "Content-Type: application/json"

# Conduct
curl -X POST "http://localhost:8000/api/workflows/from-scenario?scenario_type=conduct&name=Test5&description=Test" -H "Content-Type: application/json"

# Scholarship
curl -X POST "http://localhost:8000/api/workflows/from-scenario?scenario_type=scholarship&name=Test6&description=Test" -H "Content-Type: application/json"
```

Expected: All 6 should return HTTP 201 with a workflow_id

---

## 📊 REAL-WORLD EXAMPLE: Student Not Attending Class

**Story:** Student Rajesh (rajesh@school.com) has 65% attendance (needs 70%).

### Step 1: Create workflow
```bash
curl -X POST "http://localhost:8000/api/workflows/from-scenario?scenario_type=attendance&name=Rajesh%20Follow-up&description=Handle%20Rajesh's%20low%20attendance" -H "Content-Type: application/json"
```
Save the workflow_id (let's say: `wf_rajesh_001`)

### Step 2: Start workflow for Rajesh
```bash
curl -X POST "http://localhost:8000/api/workflows/wf_rajesh_001/run" -H "Content-Type: application/json" -d "{\"workflow_definition_id\": \"wf_rajesh_001\", \"subject_email\": \"rajesh@school.com\", \"subject_id\": \"2024_0789\"}"
```
Save the instance_id (let's say: `wfi_rajesh_001`)

### Step 3: Check what happened
```bash
curl -X GET "http://localhost:8000/api/workflows/instances/wfi_rajesh_001" -H "Content-Type: application/json"
```

**What You'll See:**
```
current_state: "IN_PROGRESS"
current_step: 1
next_scheduled_at: 3 days from now (March 25 if today is March 22)

execution_log: [
  {
    "step": 1,
    "action": "send_email",
    "details": "Email sent to rajesh@school.com",
    "timestamp": "2025-03-22T10:31:00Z"
  },
  {
    "step": 1,
    "action": "log_action",
    "details": "Step 1 completed"
  }
]

metadata: {
  "attendance_percentage": 65,
  "days_absent": 5
}
```

**Timeline of What Will Happen (Automated):**
- Day 0 ✅ DONE: Email sent to Rajesh
- Day 3 ⏳ PENDING: Check attendance again
- Day 4 ⏳ PENDING: If still low, send urgent reminder
- Day 7 ⏳ PENDING: Email parent (auto-fetch parent email)
- Day 14 ⏳ PENDING: Alert principal if unresolved

---

## ✅ SUCCESS CHECKLIST

After running tests, check for:

- [ ] Test 1: Shows 6 scenarios
- [ ] Test 2: Returns workflow_id
- [ ] Test 3: Returns instance_id
- [ ] Test 4: Shows current_state = IN_PROGRESS
- [ ] Test 5: All 6 scenarios work
- [ ] Test 6: Execution log shows actions taken

If ALL boxes are checked ✅, your system is working!

---

## 🚨 TROUBLESHOOTING

| Problem | Solution |
|---------|----------|
| `curl: command not found` | Use PowerShell instead of CMD, or use `python complete_testing_guide.py` |
| `Connection refused` | Backend not running. Run: `python -m uvicorn backend.main:app --reload` |
| `HTTP 404` | Wrong workflow_id or instance_id. Copy from previous response |
| `HTTP 422` | Wrong JSON format. Make sure you copy the entire curl command |

---

## 📝 HOW TO EXPLAIN RESULTS TO OTHERS

### If Everything Works (All Tests Pass):
> "The system successfully created and executed automated follow-up workflows. The API endpoints are responding correctly, all 6 pre-built scenarios are available, and the workflow engine properly tracks execution steps. The system is ready for integration into the production dashboard."

### If Only Some Tests Pass:
> "Tests 1-4 passed, confirming the core API and workflow engine are functioning. Test 5 and 6 had issues with [specific scenario type], which suggests [specific problem area]."

### Explaining to Non-Technical People:
> "This is an automated system that sends reminders to students about important things (like attendance, assignments, fees, exams, etc.). When we create a 'follow-up pipeline' for a student, the system automatically sends them emails on specific dates. If they don't respond, it can escalate to parents and administrators. We just tested that the system correctly creates these pipelines, starts them for students, and tracks what's happening."

---

## 🎯 What Each Test Proves

| Test | Proves | Business Value |
|------|--------|-----------------|
| 1 | API is responding | System is reachable |
| 2 | Templates exist | 6 scenarios available |
| 3 | Workflows execute | System can start follow-ups |
| 4 | Status tracking works | We can monitor progress |
| 5 | All scenarios work | Full feature set operational |
| 6 | Real workflow runs | Real students can be tracked |

---

## 🚀 NEXT STEPS

Once testing confirms everything works:

1. **Integrate into Dashboard** → Add PipelineBuilder tab to FacultyEmailDashboard
2. **Connect Real Gmail** → Replace mock emails with actual sending
3. **Database Integration** → Connect to live Supabase instead of memory
4. **Scheduled Execution** → Set up background job to run workflows on schedule
5. **Real-Time Updates** → Add WebSocket for live monitoring

Each takes 15-30 minutes with proper documentation.

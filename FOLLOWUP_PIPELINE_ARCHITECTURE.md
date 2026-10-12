# Follow-up Pipeline System Architecture

## 1. STUDENT ATTENDANCE SCENARIO (Your Example)

### Workflow Definition
```
Student X: abc@gmail.com (ID: 1234554321)
Problem: Not attending classes, not submitting assignments
Goal: Get student to attend classes and submit assignments
```

### Pipeline States & Flow
```
START
  ↓
[STEP 1] Initial Contact (Day 0)
  └─ Send email to student: "You've missed 3 classes. Please attend."
  └─ Record: email_sent_to_student = True, attempts = 1
  ↓
[STEP 2] Wait 3 Days
  └─ Scheduled check at Day 3
  ↓
[STEP 3] Automated Check
  └─ Query ERP: Student attendance as of Day 3
  └─ Decision: attendance >= 70% ?
     ├─ YES → Go to [SUCCESS] - Mark as "resolved"
     └─ NO → Continue to [STEP 4]
  ↓
[STEP 4] Second Reminder (Day 4)
  └─ Send email to student: "Reminder: You must attend classes to pass"
  └─ Record: attempts = 2, escalation_pending = True
  ↓
[STEP 5] Wait 2 Days + Check
  └─ Scheduled check at Day 6
  └─ Query ERP: Updated attendance
  └─ Decision: attendance >= 70% ?
     ├─ YES → Go to [SUCCESS]
     └─ NO → Continue to [STEP 6]
  ↓
[STEP 6] Escalation to Parent (Day 7)
  └─ Query ERP: Get parent email for student
  └─ Send email to parent: "Your child has missed too many classes. Please intervene."
  └─ Record: escalation_level = "parent", parent_contacted = True
  ↓
[STEP 7] Parent Follow-up (Day 14)
  └─ If no improvement: Send admin alert
  └─ Record: escalation_level = "admin"
  ↓
[END]
```

### State Persistence in Supabase
```json
{
  "workflow_instance": {
    "id": "uuid",
    "student_email": "abc@gmail.com",
    "student_id": "1234554321",
    "workflow_name": "student_attendance_followup",
    "current_step": 6,
    "current_state": "parent_contacted",
    "created_at": "2026-04-30T10:00:00Z",
    "last_action_at": "2026-05-07T10:00:00Z",
    "next_scheduled_step": "2026-05-14T10:00:00Z",
    "metadata": {
      "attempts": 2,
      "escalation_level": "parent",
      "parent_email": "parent@example.com",
      "last_attendance_check": 65,
      "emails_sent": ["student_reminder_1", "student_reminder_2", "parent_escalation"]
    }
  }
}
```

---

## 2. FIVE ADDITIONAL SCENARIOS

### Scenario 2: Assignment Deadline Follow-up
**Problem:** Students not submitting assignments
**Pipeline:**
- Day 0: Send reminder "Assignment XYZ due in 3 days"
- Day 2: Check if submitted
- If No → Send urgent reminder
- Day 4 (after deadline): Check submissions
- If still No → Auto-reduce marks, notify parents

**Where it's used:** Any assignment-heavy course (Engineering, Maths, Projects)

---

### Scenario 3: Fee Payment Collection
**Problem:** Parents not paying school fees on time
**Pipeline:**
- Day 1: Send fee payment reminder to parent
- Day 15: Send second reminder + partial payment option
- Day 30: Escalate to principal, restrict student access
- Day 45: Send final notice + payment plan offer

**Where it's used:** School fee collection, hostel charges, activity fees

---

### Scenario 4: Exam Preparation Tracking
**Problem:** Students not prepared for exams, failing
**Pipeline:**
- Day 60 (before exam): Send study materials + tips
- Day 30: Send mock test link, track if attempted
- Day 7: If not practiced → Send remedial guidance
- Day 1: Final tips, exam timing reminders

**Where it's used:** Board exams, competitive exams (JEE, NEET), internal exams

---

### Scenario 5: Conduct & Behavior Issues
**Problem:** Student has behavior/discipline issues
**Pipeline:**
- Day 0: Send first warning to student
- Day 7: If no improvement → Schedule counselor meeting
- Day 14: If still issues → Notify parents (meeting invitation)
- Day 21: If unresolved → Suspension notice

**Where it's used:** Bullying cases, classroom disruption, attendance abuse

---

### Scenario 6: Scholarship Eligibility Reminders
**Problem:** Eligible students missing scholarship application deadlines
**Pipeline:**
- Day 30 (before deadline): Send eligibility confirmation + application form
- Day 15: Send reminder + deadline alert
- Day 5: URGENT - Last chance notification
- Day 1 (after deadline): Send rejection/acceptance status

**Where it's used:** Merit scholarships, financial aid, government schemes

---

## 3. WHERE IN UI WILL IT BE CREATED?

### Current TaskAdaptiveWorkspace Modal Structure
```
TaskAdaptiveWorkspace
├── existing_modal (FacultyEmailDashboard - already there)
├── NEW: pipeline_builder_modal (Create/Edit Pipelines)
├── NEW: pipeline_monitor_modal (View Running Pipelines)
└── NEW: scenario_templates_modal (Quick-start templates)
```

### New Tab in Faculty Dashboard
```
FacultyEmailDashboard
├── Tab 1: Digest (existing)
├── Tab 2: Priorities (existing)
├── Tab 3: Threads (existing)
└── NEW Tab 4: Follow-up Pipelines
   ├── Active Pipelines (list with status)
   ├── Pipeline Templates (quick-start)
   ├── Create New Pipeline (button → opens PipelineBuilder)
   └── Pipeline History (completed/archived)
```

### Pipeline Builder UI
```
LEFT PANEL (Step Library)
├── Step Type: Send Email
├── Step Type: Check Condition (ERP Query)
├── Step Type: Wait (Delay)
├── Step Type: Log Action
├── Step Type: Escalate

MIDDLE PANEL (Canvas)
├── Drag-drop steps to create flow
├── Visual connections between steps
├── Decision diamonds for conditions
└── Preview execution path

RIGHT PANEL (Configuration)
├── Step name & description
├── Email template selection
├── ERP query type
├── Delay duration
└── Condition logic (if/then)
```

### How to Edit?
**Option 1: Visual Editor (Recommended)**
- Click pipeline → Opens PipelineBuilder in visual mode
- Drag steps, reconnect conditions
- Save changes → Automatically updates all future instances

**Option 2: Code/JSON Editor**
- Advanced users can edit JSON workflow definition
- Schema validation on save
- Version history tracked

**Option 3: Template Modification**
- Clone from template
- Modify conditions, email templates, delays
- Test before deploying

---

## 4. TECHNICAL ARCHITECTURE

### Backend Components
```
backend/
├── core/
│   ├── workflow_engine.py (NEW)
│   │   ├── WorkflowDefinition (class)
│   │   ├── WorkflowInstance (class)
│   │   ├── WorkflowExecutor (class)
│   │   └── WorkflowScheduler (class)
│   ├── workflow_scenarios.py (NEW)
│   │   ├── StudentAttendanceScenario
│   │   ├── AssignmentReminderScenario
│   │   ├── FeeCollectionScenario
│   │   ├── ExamPrepScenario
│   │   ├── ConductIssueScenario
│   │   └── ScholarshipScenario
│   └── erp_integration.py (NEW)
│       ├── get_student_attendance()
│       ├── get_parent_email()
│       ├── check_assignment_status()
│       └── get_fee_status()
│
├── routes/
│   └── workflows.py (NEW)
│       ├── POST /api/workflows (create)
│       ├── GET /api/workflows (list)
│       ├── GET /api/workflows/{id} (detail)
│       ├── PUT /api/workflows/{id} (edit)
│       ├── POST /api/workflows/{id}/run (execute)
│       ├── GET /api/workflows/{id}/instances (see running)
│       └── DELETE /api/workflows/{id} (delete)
│
└── tests/
    └── test_workflow_engine.py (NEW)
```

### Frontend Components
```
frontend/src/components/
├── PipelineBuilder.jsx (NEW)
│   ├── Canvas for visual editing
│   ├── Step palette
│   └── Configuration panel
├── PipelineMonitor.jsx (NEW)
│   ├── Active pipelines list
│   ├── Execution timeline
│   └── Manual override options
├── ScenarioTemplates.jsx (NEW)
│   └── Quick-start templates (copy & modify)
└── FacultyEmailDashboard.jsx (MODIFIED)
    └── Add "Pipelines" tab
```

### Database Schema (Supabase)
```sql
-- Workflow Definitions
CREATE TABLE workflow_definitions (
  id UUID PRIMARY KEY,
  name VARCHAR(255) UNIQUE,
  description TEXT,
  scenario_type VARCHAR(100), -- 'attendance', 'assignment', 'fee', etc.
  steps JSONB, -- Workflow step definitions
  conditions JSONB, -- Branching logic
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  created_by UUID
);

-- Workflow Instances (running workflows)
CREATE TABLE workflow_instances (
  id UUID PRIMARY KEY,
  workflow_definition_id UUID REFERENCES workflow_definitions(id),
  subject_email VARCHAR(255),
  subject_id VARCHAR(255),
  current_step INT,
  current_state VARCHAR(50), -- 'in_progress', 'parent_contacted', 'completed'
  metadata JSONB, -- Custom data per instance
  next_scheduled_at TIMESTAMP,
  created_at TIMESTAMP,
  completed_at TIMESTAMP
);

-- Workflow Execution Log
CREATE TABLE workflow_execution_log (
  id UUID PRIMARY KEY,
  workflow_instance_id UUID REFERENCES workflow_instances(id),
  step_number INT,
  action_type VARCHAR(100), -- 'email_sent', 'check_performed', 'escalation'
  status VARCHAR(50), -- 'success', 'failed', 'skipped'
  details JSONB,
  executed_at TIMESTAMP
);
```

---

## 5. IMPLEMENTATION SEQUENCE

### Phase 1: Core Engine
1. ✅ Create WorkflowDefinition, WorkflowInstance classes
2. ✅ Create WorkflowExecutor (handle step execution)
3. ✅ Create Supabase schema
4. ✅ REST endpoints CRUD

### Phase 2: Student Attendance Scenario
1. ✅ Create StudentAttendanceScenario template
2. ✅ Implement ERP integration (mock for now)
3. ✅ Test full pipeline execution

### Phase 3: Frontend Pipeline Builder
1. ✅ Create visual canvas (React)
2. ✅ Add to FacultyEmailDashboard as tab
3. ✅ Drag-drop step building

### Phase 4: 4 More Scenarios
1. ✅ AssignmentReminderScenario
2. ✅ FeeCollectionScenario
3. ✅ ExamPrepScenario
4. ✅ ConductIssueScenario

### Phase 5: Advanced Features
1. ✅ Scheduler service (background job execution)
2. ✅ Webhook support (ERP callbacks)
3. ✅ Manual override UI
4. ✅ Execution history & analytics

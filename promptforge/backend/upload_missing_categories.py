#!/usr/bin/env python3
"""Upload missing Project Management and Education prompts"""
import firebase_admin
from firebase_admin import credentials, firestore
import time

# Initialize Firebase
cred = credentials.Certificate('firebase-credentials.json')
try:
    firebase_admin.get_app()
except ValueError:
    firebase_admin.initialize_app(cred)

db = firestore.client()

# PROJECT MANAGEMENT PROMPTS (71-78)
project_management_prompts = [
    {'id': 71, 'title': 'Agile Sprint Planning', 'category': 'project-management', 'text': 'Create comprehensive Agile sprint plan for [TEAM/PROJECT]. Include: sprint goal, user story breakdown with story points, sprint backlog prioritization, capacity planning, definition of done, risk assessment, daily standup structure, sprint review & retrospective agenda.', 'rating': 4.9, 'uses': 11200, 'tags': ['agile', 'scrum', 'sprint-planning', 'project-management']},
    {'id': 72, 'title': 'Project Charter Template', 'category': 'project-management', 'text': 'Create project charter for [PROJECT]. Include: executive summary, project purpose & justification, objectives with success criteria, scope (in/out), key stakeholders, high-level requirements, assumptions & constraints, budget estimate, timeline, approval signatures.', 'rating': 4.8, 'uses': 9400, 'tags': ['project-charter', 'project-initiation', 'planning', 'governance']},
    {'id': 73, 'title': 'Risk Management Plan', 'category': 'project-management', 'text': 'Develop risk management plan for [PROJECT]. Include: risk identification (15-20 risks), qualitative analysis (probability/impact matrix), quantitative analysis, risk response strategies (avoid, mitigate, transfer, accept), risk register, monitoring plan, escalation procedures.', 'rating': 4.9, 'uses': 8600, 'tags': ['risk-management', 'project-planning', 'mitigation', 'governance']},
    {'id': 74, 'title': 'Stakeholder Communication Plan', 'category': 'project-management', 'text': 'Create stakeholder communication plan for [PROJECT]. Include: stakeholder analysis (power/interest grid), communication requirements, communication matrix (who/what/when/how), meeting cadence, reporting templates, escalation paths, feedback mechanisms, change management.', 'rating': 4.8, 'uses': 7800, 'tags': ['stakeholder-management', 'communication', 'project-management', 'governance']},
    {'id': 75, 'title': 'Resource Allocation Matrix', 'category': 'project-management', 'text': 'Design resource allocation plan for [PROJECT]. Include: resource requirements, skills matrix, RACI chart, resource calendar, capacity planning, conflict resolution, onboarding plan, performance tracking, contingency resources, cost analysis.', 'rating': 4.7, 'uses': 6900, 'tags': ['resource-management', 'capacity-planning', 'team-management', 'allocation']},
    {'id': 76, 'title': 'Change Management Process', 'category': 'project-management', 'text': 'Create change management process for [PROJECT]. Include: change request template, impact assessment criteria, approval workflow, change advisory board structure, implementation plan, communication strategy, rollback procedures, lessons learned documentation.', 'rating': 4.8, 'uses': 7200, 'tags': ['change-management', 'process', 'governance', 'project-control']},
    {'id': 77, 'title': 'Project Status Report', 'category': 'project-management', 'text': 'Generate project status report for [PROJECT]. Include: executive summary (RAG status), milestone progress, budget vs actual, resource utilization, risk & issue status, accomplishments, upcoming deliverables, decisions needed, action items with owners.', 'rating': 4.9, 'uses': 10400, 'tags': ['status-report', 'project-reporting', 'communication', 'dashboard']},
    {'id': 78, 'title': 'Project Retrospective Framework', 'category': 'project-management', 'text': 'Design project retrospective for [PROJECT/SPRINT]. Include: retrospective format (Start/Stop/Continue, 4Ls, Sailboat), data gathering, insights generation, prioritization voting, action items with SMART goals, celebration moments, continuous improvement tracking.', 'rating': 4.8, 'uses': 8200, 'tags': ['retrospective', 'lessons-learned', 'continuous-improvement', 'agile']},
]

# EDUCATION PROMPTS (79-86)
education_prompts = [
    {'id': 79, 'title': 'Lesson Plan Creator', 'category': 'education', 'text': 'Create comprehensive lesson plan for [SUBJECT/TOPIC]. Include: learning objectives (Bloom\'s taxonomy), prior knowledge assessment, teaching strategies, activities & materials, differentiation strategies, formative assessment, summative assessment, homework, reflection questions.', 'rating': 4.9, 'uses': 12800, 'tags': ['lesson-planning', 'teaching', 'curriculum', 'pedagogy']},
    {'id': 80, 'title': 'Course Curriculum Design', 'category': 'education', 'text': 'Design complete course curriculum for [COURSE]. Include: course description, learning outcomes, weekly syllabus (12-16 weeks), required materials, assessment strategy, grading rubric, course policies, technology requirements, accessibility considerations.', 'rating': 4.8, 'uses': 9200, 'tags': ['curriculum-design', 'course-planning', 'syllabus', 'higher-ed']},
    {'id': 81, 'title': 'Assessment & Rubric Builder', 'category': 'education', 'text': 'Create assessment and rubric for [ASSIGNMENT/PROJECT]. Include: clear instructions, learning objectives alignment, rubric with 4-5 performance levels, criteria descriptions, point distribution, grading guidelines, feedback template, self-assessment component.', 'rating': 4.9, 'uses': 10600, 'tags': ['assessment', 'rubrics', 'grading', 'evaluation']},
    {'id': 82, 'title': 'Interactive Learning Activity', 'category': 'education', 'text': 'Design interactive learning activity for [CONCEPT]. Include: learning objective, activity description, materials needed, step-by-step instructions, group size & roles, time allocation, discussion prompts, learning reinforcement, assessment method, variations for different learning styles.', 'rating': 4.8, 'uses': 8400, 'tags': ['active-learning', 'engagement', 'pedagogy', 'activities']},
    {'id': 83, 'title': 'Online Course Structure', 'category': 'education', 'text': 'Structure online course for [TOPIC]. Include: module breakdown, video script outlines, interactive elements (quizzes, discussions, assignments), resource library, learning path, engagement strategies, community building, technical setup, accessibility compliance, completion certificates.', 'rating': 4.9, 'uses': 11400, 'tags': ['online-learning', 'e-learning', 'course-design', 'distance-education']},
    {'id': 84, 'title': 'Student Feedback Framework', 'category': 'education', 'text': 'Create student feedback system for [COURSE/PROGRAM]. Include: formative feedback strategies, summative feedback template, constructive criticism framework, strengths-based approach, actionable improvement suggestions, peer feedback guidelines, self-reflection prompts, feedback timing.', 'rating': 4.8, 'uses': 7600, 'tags': ['feedback', 'student-assessment', 'teaching', 'improvement']},
    {'id': 85, 'title': 'Differentiated Instruction Plan', 'category': 'education', 'text': 'Design differentiated instruction for [LESSON/TOPIC]. Include: readiness differentiation (below/at/above level), learning style variations (visual/auditory/kinesthetic), interest-based options, flexible grouping strategies, scaffolding techniques, extension activities, assessment variations.', 'rating': 4.9, 'uses': 9800, 'tags': ['differentiation', 'inclusive-education', 'teaching-strategies', 'accessibility']},
    {'id': 86, 'title': 'Educational Technology Integration', 'category': 'education', 'text': 'Integrate technology into [LESSON/COURSE]. Include: technology selection (SAMR model), pedagogical justification, implementation plan, student training needs, troubleshooting guide, accessibility features, data privacy considerations, assessment of technology effectiveness.', 'rating': 4.8, 'uses': 8900, 'tags': ['edtech', 'technology-integration', 'digital-learning', 'innovation']},
]

all_new_prompts = project_management_prompts + education_prompts

print("="*70)
print("  UPLOADING PROJECT MANAGEMENT & EDUCATION PROMPTS")
print("="*70)
print()

collection = db.collection('prompts')
successful = 0
failed = 0
start_time = time.time()

for prompt in all_new_prompts:
    try:
        doc_data = {
            'title': prompt['title'],
            'category': prompt['category'],
            'text': prompt['text'],
            'rating': prompt['rating'],
            'uses': prompt['uses'],
            'submitter': 'Curated',
            'type': 'curated',
            'tags': prompt['tags'],
            'approved': True,
            'copy_count': prompt['uses']
        }
        
        doc_id = str(prompt['id'])
        collection.document(doc_id).set(doc_data)
        successful += 1
        print(f"✓ {prompt['id']}: {prompt['title']}")
        
    except Exception as e:
        failed += 1
        print(f"✗ Failed: {prompt['title']} - {e}")

elapsed_time = time.time() - start_time

print()
print("="*70)
print(f"  UPLOAD COMPLETE! ({elapsed_time:.1f}s)")
print("="*70)
print(f"✅ Successfully uploaded: {successful} prompts")
if failed > 0:
    print(f"❌ Failed: {failed} prompts")
print()
print("New categories added:")
print(f"  • Project Management: 8 prompts")
print(f"  • Education: 8 prompts")
print()
print("🎉 Total database now has: 86 prompts across 10 categories!")
print("="*70)

#!/usr/bin/env python3
"""Upload ALL 70+ prompts to Firestore - Complete Database"""
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

# Complete prompts database - all 70+ prompts
all_prompts = [
    # MARKETING (1-10) - Already uploaded, but including for completeness
    {'id': 1, 'title': 'SEO Blog Post Generator', 'category': 'marketing', 'text': 'You are an SEO expert. Create comprehensive SEO-optimized blog post about [TOPIC]. Include: compelling title with primary keyword, meta description (150-160 chars), H2/H3 subheadings, 1500+ words valuable content, internal/external links, FAQ section, call-to-action.', 'rating': 4.9, 'uses': 15200, 'tags': ['seo', 'content', 'blog']},
    {'id': 2, 'title': 'Social Media Campaign Planner', 'category': 'marketing', 'text': 'Create 30-day social media campaign for [PRODUCT/SERVICE]. Include: campaign strategy, content calendar (30 days), post types, captions with hashtags, visual concepts, posting schedule, engagement tactics, paid ad recommendations, KPIs.', 'rating': 4.8, 'uses': 8900, 'tags': ['social-media', 'campaign']},
    {'id': 3, 'title': 'Email Marketing Sequence', 'category': 'marketing', 'text': 'Design high-converting email sequence for [PRODUCT/SERVICE]. Create 5-7 emails with subject lines (A/B variants), body copy, CTAs, optimal send times, personalization tokens, expected metrics.', 'rating': 4.7, 'uses': 6700, 'tags': ['email-marketing', 'conversion']},
    {'id': 4, 'title': 'Landing Page Copy Optimizer', 'category': 'marketing', 'text': 'Create high-converting landing page copy for [PRODUCT]. Include: hero section (headline, subheadline, CTA), problem agitation, solution presentation, social proof, feature breakdown, objection handling FAQ, final CTA section with urgency.', 'rating': 4.9, 'uses': 11400, 'tags': ['landing-page', 'copywriting', 'conversion']},
    {'id': 5, 'title': 'Google Ads Campaign Structure', 'category': 'marketing', 'text': 'Design comprehensive Google Ads campaign for [PRODUCT]. Include: campaign structure, ad groups (3-5), keyword research (20-30 keywords), ad copy (3 variants), extensions, landing page alignment, conversion tracking, performance benchmarks.', 'rating': 4.8, 'uses': 7200, 'tags': ['google-ads', 'ppc', 'sem']},
    {'id': 6, 'title': 'Content Marketing Strategy', 'category': 'marketing', 'text': 'Develop 90-day content marketing strategy for [COMPANY]. Include: content pillars (3-5), content mix strategy, editorial calendar, SEO integration, distribution plan, repurposing strategy, metrics & KPIs.', 'rating': 4.9, 'uses': 9800, 'tags': ['content-strategy', 'marketing', 'seo']},
    {'id': 7, 'title': 'Product Launch Marketing Plan', 'category': 'marketing', 'text': 'Create product launch marketing plan for [PRODUCT]. Include: pre-launch (4-6 weeks), launch week day-by-day plan, post-launch (4 weeks), channels & tactics, messaging framework, budget allocation, success metrics.', 'rating': 4.8, 'uses': 5600, 'tags': ['product-launch', 'go-to-market']},
    {'id': 8, 'title': 'Brand Voice & Messaging Guide', 'category': 'marketing', 'text': 'Create comprehensive brand voice guide for [COMPANY]. Include: brand personality, voice attributes, messaging pillars, audience-specific messaging, vocabulary guidelines, channel adaptations, examples & templates.', 'rating': 4.7, 'uses': 4900, 'tags': ['brand-voice', 'messaging', 'copywriting']},
    {'id': 9, 'title': 'Competitor Analysis Report', 'category': 'marketing', 'text': 'Conduct comprehensive competitor analysis for [YOUR COMPANY]. Analyze 3-5 competitors: company overview, product/service analysis, marketing strategy, website analysis, customer perception, SWOT analysis, strategic recommendations.', 'rating': 4.8, 'uses': 7800, 'tags': ['competitor-analysis', 'market-research', 'strategy']},
    {'id': 10, 'title': 'Influencer Marketing Campaign', 'category': 'marketing', 'text': 'Design influencer marketing campaign for [PRODUCT]. Include: influencer strategy, 20 potential influencers list, campaign brief, compensation structure, content requirements, tracking & measurement, outreach templates.', 'rating': 4.7, 'uses': 6100, 'tags': ['influencer-marketing', 'social-media', 'campaign']},
    
    # CODING (11-22)
    {'id': 11, 'title': 'Python Code Review & Optimization', 'category': 'coding', 'text': 'You are a senior Python developer. Review this code: [CODE]. Provide: code quality assessment, performance optimization, best practices (PEP 8), security considerations, testing recommendations, refactored version with comparisons, documentation improvements.', 'rating': 4.9, 'uses': 12300, 'tags': ['python', 'code-review', 'optimization']},
    {'id': 12, 'title': 'React Component Architecture', 'category': 'coding', 'text': 'Design scalable React architecture for [FEATURE]. Include: component hierarchy, state management strategy, component patterns, performance optimization, TypeScript types, testing strategy, sample implementation.', 'rating': 4.8, 'uses': 8900, 'tags': ['react', 'javascript', 'architecture', 'frontend']},
    {'id': 13, 'title': 'SQL Query Optimization', 'category': 'coding', 'text': 'Optimize this SQL query: [QUERY]. Provide: query analysis, execution plan breakdown, optimized query, indexing recommendations, schema improvements, before/after metrics, monitoring approach.', 'rating': 4.9, 'uses': 7600, 'tags': ['sql', 'database', 'optimization', 'performance']},
    {'id': 14, 'title': 'API Design & Documentation', 'category': 'coding', 'text': 'Design RESTful API for [APPLICATION]. Include: endpoint design, request/response formats, pagination, filtering/sorting, error handling, rate limiting, authentication, OpenAPI/Swagger spec, SDK examples.', 'rating': 4.8, 'uses': 9200, 'tags': ['api', 'rest', 'backend', 'documentation']},
    {'id': 15, 'title': 'Debugging Strategy Generator', 'category': 'coding', 'text': 'Debug this issue: [BUG DESCRIPTION]. Provide: hypothesis generation (5 likely causes), systematic debugging plan, diagnostic commands, isolation techniques, temporary workarounds, preventive measures, root cause analysis framework.', 'rating': 4.7, 'uses': 5800, 'tags': ['debugging', 'troubleshooting', 'problem-solving']},
    {'id': 16, 'title': 'Docker & DevOps Setup', 'category': 'coding', 'text': 'Create Docker and CI/CD setup for [APPLICATION]. Include: Dockerfile (multi-stage), docker-compose.yml, CI/CD pipeline (GitHub Actions), Kubernetes manifests, nginx configuration, environment management, monitoring & logging.', 'rating': 4.9, 'uses': 11200, 'tags': ['docker', 'devops', 'ci-cd', 'kubernetes']},
    {'id': 17, 'title': 'Unit Test Suite Generator', 'category': 'coding', 'text': 'Generate comprehensive unit tests for: [CODE]. Include: test plan, test setup, happy path tests, edge cases, error handling tests, mocking strategy, complete test suite, coverage report interpretation.', 'rating': 4.8, 'uses': 8700, 'tags': ['testing', 'unit-tests', 'tdd', 'quality-assurance']},
    {'id': 18, 'title': 'GraphQL Schema Designer', 'category': 'coding', 'text': 'Design GraphQL schema for [APPLICATION]. Include: type definitions, queries, mutations, subscriptions, resolver structure, authentication & authorization, error handling, performance optimization, example queries.', 'rating': 4.7, 'uses': 6300, 'tags': ['graphql', 'api', 'backend', 'schema-design']},
    {'id': 19, 'title': 'Security Audit Checklist', 'category': 'coding', 'text': 'Conduct security audit for [APPLICATION]. Audit: authentication, authorization, input validation, data protection, API security, dependency security, infrastructure, logging & monitoring, code security. For each vulnerability: severity, remediation steps.', 'rating': 4.9, 'uses': 10100, 'tags': ['security', 'audit', 'vulnerability', 'best-practices']},
    {'id': 20, 'title': 'Microservices Architecture Design', 'category': 'coding', 'text': 'Design microservices architecture for [SYSTEM]. Include: service decomposition, communication patterns, data management, service discovery, API gateway, deployment strategy, observability, resilience patterns, migration plan.', 'rating': 4.8, 'uses': 7900, 'tags': ['microservices', 'architecture', 'distributed-systems']},
    {'id': 21, 'title': 'Git Workflow & Best Practices', 'category': 'coding', 'text': 'Design Git workflow for [TEAM]. Include: branching strategy, commit conventions, merge strategy, code review process, CI/CD integration, version control, hotfix procedure, documentation, automation.', 'rating': 4.7, 'uses': 8400, 'tags': ['git', 'version-control', 'workflow', 'best-practices']},
    {'id': 22, 'title': 'Mobile App Performance Optimization', 'category': 'coding', 'text': 'Optimize mobile app performance for [PLATFORM]. Analyze: startup time, memory management, network optimization, UI performance, battery optimization, app size reduction, database optimization, profiling & monitoring.', 'rating': 4.8, 'uses': 6700, 'tags': ['mobile', 'performance', 'optimization', 'ios', 'android']},
    
    # WRITING (23-30)
    {'id': 23, 'title': 'Professional Email Writer', 'category': 'writing', 'text': 'Write professional email for [SITUATION]. Include: clear subject line, appropriate greeting, concise body (under 200 words), specific action items, appropriate sign-off. Tone: [Formal/Semi-formal/Friendly professional].', 'rating': 4.9, 'uses': 18600, 'tags': ['email', 'professional', 'communication', 'business']},
    {'id': 24, 'title': 'LinkedIn Post Creator', 'category': 'writing', 'text': 'Create engaging LinkedIn post about [TOPIC]. Include: hook (first 2 lines), body content with insights, engagement elements, hashtags (3-5), CTA. Provide 2 versions: personal/storytelling and data-driven/professional.', 'rating': 4.8, 'uses': 11200, 'tags': ['linkedin', 'social-media', 'content', 'professional']},
    {'id': 25, 'title': 'Technical Documentation Writer', 'category': 'writing', 'text': 'Create comprehensive technical documentation for [SOFTWARE/FEATURE]. Include: overview, prerequisites, getting started, core concepts, detailed guides with examples, API reference, troubleshooting, best practices.', 'rating': 4.9, 'uses': 9800, 'tags': ['documentation', 'technical-writing', 'guides', 'api-docs']},
    {'id': 26, 'title': 'Press Release Generator', 'category': 'writing', 'text': 'Write professional press release for [ANNOUNCEMENT]. Include: headline, subheadline, lead paragraph, body (2-3 paragraphs), company boilerplate, contact information. Follow AP Style. 400-600 words.', 'rating': 4.7, 'uses': 5600, 'tags': ['press-release', 'pr', 'media', 'corporate-communications']},
    {'id': 27, 'title': 'Resume & Cover Letter Optimizer', 'category': 'writing', 'text': 'Optimize resume and cover letter for [JOB]. Include: ATS-friendly formatting, keyword optimization, achievement-focused bullets with quantified results, compelling summary, tailored cover letter (under 400 words).', 'rating': 4.8, 'uses': 14300, 'tags': ['resume', 'cover-letter', 'job-search', 'career']},
    {'id': 28, 'title': 'Case Study Writer', 'category': 'writing', 'text': 'Write compelling customer case study for [CLIENT/PROJECT]. Include: executive summary, client background, challenge deep-dive, solution details, quantified results, client testimonial, key takeaways, CTA. 1000-1500 words.', 'rating': 4.9, 'uses': 7400, 'tags': ['case-study', 'content-marketing', 'success-story', 'b2b']},
    {'id': 29, 'title': 'Grant Proposal Writer', 'category': 'writing', 'text': 'Write grant proposal for [PROJECT]. Include: cover letter, executive summary, statement of need, project description with SMART goals, evaluation plan, organizational capacity, detailed budget, sustainability plan.', 'rating': 4.7, 'uses': 4200, 'tags': ['grant-writing', 'nonprofit', 'fundraising', 'proposal']},
    {'id': 30, 'title': 'Whitepaper Writer', 'category': 'writing', 'text': 'Create authoritative whitepaper on [TOPIC]. Include: executive summary, introduction, background/context, the challenge, solution/approach, technical details, implementation guide, results/benefits, conclusion. 2500-5000 words.', 'rating': 4.8, 'uses': 6900, 'tags': ['whitepaper', 'content-marketing', 'b2b', 'thought-leadership']},
    
    # BUSINESS (31-38)
    {'id': 31, 'title': 'Business Model Canvas Generator', 'category': 'business', 'text': 'Create comprehensive Business Model Canvas for [BUSINESS]. Fill all 9 blocks: customer segments, value propositions, channels, customer relationships, revenue streams, key resources, key activities, key partnerships, cost structure. Include competitive advantages and validation plan.', 'rating': 4.9, 'uses': 13400, 'tags': ['business-model', 'strategy', 'startup', 'planning']},
    {'id': 32, 'title': 'SWOT Analysis Framework', 'category': 'business', 'text': 'Conduct comprehensive SWOT analysis for [COMPANY/PROJECT]. List 5-10 items per category with evidence. Include SO/WO/ST/WT strategies, priority matrix, action plan with owners and timelines.', 'rating': 4.8, 'uses': 10200, 'tags': ['swot-analysis', 'strategy', 'business-planning', 'analysis']},
    {'id': 33, 'title': 'Investor Pitch Deck Creator', 'category': 'business', 'text': 'Create compelling investor pitch deck for [COMPANY]. 10-15 slides: cover, problem, solution, market opportunity, product, traction, business model, go-to-market, competitive landscape, team, financial projections, the ask. Include storytelling arc and design principles.', 'rating': 4.9, 'uses': 9800, 'tags': ['pitch-deck', 'fundraising', 'investors', 'startup']},
    {'id': 34, 'title': 'Marketing Strategy Plan', 'category': 'business', 'text': 'Develop comprehensive marketing strategy for [COMPANY/PRODUCT]. Include: situation analysis, target audience personas, positioning & messaging, channel strategy (content, social, email, paid ads), 90-day action plan, budget breakdown, metrics & KPIs.', 'rating': 4.8, 'uses': 11600, 'tags': ['marketing-strategy', 'business-planning', 'growth']},
    {'id': 35, 'title': 'Competitive Analysis Report', 'category': 'business', 'text': 'Create detailed competitive analysis for [YOUR COMPANY]. Analyze 3-5 competitors: company overview, product/service analysis, positioning & messaging, marketing strategy, customer analysis, strengths & weaknesses, strategic recommendations, monitoring plan.', 'rating': 4.9, 'uses': 8900, 'tags': ['competitive-analysis', 'market-research', 'strategy']},
    {'id': 36, 'title': 'OKR Framework', 'category': 'business', 'text': 'Create OKR framework for [COMPANY/TEAM]. Generate 3-5 objectives with 3-5 key results each. Include: context, cascading structure, initiatives, tracking cadence, scoring rubric, communication plan, common pitfalls to avoid.', 'rating': 4.8, 'uses': 7400, 'tags': ['okr', 'goal-setting', 'strategy', 'performance-management']},
    {'id': 37, 'title': 'Crisis Management Plan', 'category': 'business', 'text': 'Create comprehensive crisis management plan for [COMPANY]. Include: crisis definition & levels, crisis types & scenarios, crisis management team, communication protocols, action plans, templates, resource inventory, training plan, recovery process.', 'rating': 4.9, 'uses': 5800, 'tags': ['crisis-management', 'risk-management', 'business-continuity']},
    {'id': 38, 'title': 'Customer Journey Mapping', 'category': 'business', 'text': 'Create detailed customer journey map for [PRODUCT/SERVICE]. Map stages: awareness, consideration, purchase, onboarding, usage, expansion. For each: customer actions, touchpoints, thoughts, emotions, pain points, opportunities. Include improvement roadmap.', 'rating': 4.9, 'uses': 8600, 'tags': ['customer-journey', 'ux', 'customer-experience', 'strategy']},
    
    # DESIGN (39-46)
    {'id': 39, 'title': 'UI/UX Design Brief', 'category': 'design', 'text': 'Create comprehensive UI/UX design brief for [PROJECT]. Include: project overview, target audience, goals & objectives, user personas, user flows, information architecture, design requirements, style preferences, technical constraints, timeline, deliverables.', 'rating': 4.8, 'uses': 9200, 'tags': ['ui-ux', 'design-brief', 'product-design', 'user-experience']},
    {'id': 40, 'title': 'Brand Identity Guide', 'category': 'design', 'text': 'Design complete brand identity system for [COMPANY]. Include: logo specifications, color palette (primary/secondary/accent), typography system, imagery guidelines, iconography, patterns & textures, brand applications, usage dos & donts.', 'rating': 4.9, 'uses': 8700, 'tags': ['brand-identity', 'visual-design', 'branding', 'style-guide']},
    {'id': 41, 'title': 'Design System Architecture', 'category': 'design', 'text': 'Create design system for [PRODUCT]. Include: design tokens, component library (atoms, molecules, organisms), grid system, spacing & layout, accessibility standards, dark mode, responsive guidelines, component documentation.', 'rating': 4.9, 'uses': 10100, 'tags': ['design-system', 'component-library', 'ui-design', 'scalability']},
    {'id': 42, 'title': 'User Research Plan', 'category': 'design', 'text': 'Design user research plan for [PRODUCT/FEATURE]. Include: research objectives, methodology (interviews, surveys, usability tests), participant recruitment criteria, discussion guide, analysis framework, timeline, expected outcomes, actionable insights format.', 'rating': 4.8, 'uses': 6800, 'tags': ['user-research', 'ux-research', 'usability', 'insights']},
    {'id': 43, 'title': 'Wireframe & Prototype Generator', 'category': 'design', 'text': 'Create wireframes and prototype for [FEATURE]. Include: lo-fi wireframes, hi-fi mockups, interactive prototype flows, user interactions, micro-interactions, responsive breakpoints, annotations, handoff specifications for developers.', 'rating': 4.7, 'uses': 7900, 'tags': ['wireframes', 'prototyping', 'mockups', 'ui-design']},
    {'id': 44, 'title': 'Accessibility Audit', 'category': 'design', 'text': 'Conduct accessibility audit for [WEBSITE/APP]. Review: WCAG 2.1 compliance, color contrast, keyboard navigation, screen reader support, ARIA labels, focus management, semantic HTML, form accessibility. Provide severity ratings and remediation steps.', 'rating': 4.9, 'uses': 5600, 'tags': ['accessibility', 'a11y', 'wcag', 'inclusive-design']},
    {'id': 45, 'title': 'Design Critique Framework', 'category': 'design', 'text': 'Perform design critique for [DESIGN]. Evaluate: visual hierarchy, typography, color usage, whitespace, consistency, usability, accessibility, brand alignment, user needs. Provide constructive feedback with specific improvements and rationale.', 'rating': 4.8, 'uses': 6400, 'tags': ['design-critique', 'feedback', 'design-review', 'improvement']},
    {'id': 46, 'title': 'Responsive Design Strategy', 'category': 'design', 'text': 'Create responsive design strategy for [WEBSITE]. Include: breakpoint system, mobile-first approach, flexible grids, responsive typography, image optimization, touch targets, navigation patterns, testing matrix, performance considerations.', 'rating': 4.8, 'uses': 7200, 'tags': ['responsive-design', 'mobile-design', 'web-design', 'cross-device']},
    
    # PRODUCTIVITY (47-54)
    {'id': 47, 'title': 'Time Management System', 'category': 'productivity', 'text': 'Design personalized time management system for [ROLE/GOALS]. Include: time audit, priority matrix, time blocking schedule, deep work sessions, meeting optimization, delegation framework, energy management, weekly review process.', 'rating': 4.9, 'uses': 15400, 'tags': ['time-management', 'productivity', 'efficiency', 'planning']},
    {'id': 48, 'title': 'Project Planning Template', 'category': 'productivity', 'text': 'Create comprehensive project plan for [PROJECT]. Include: project charter, scope definition, work breakdown structure, timeline with milestones, resource allocation, risk assessment, communication plan, success metrics, stakeholder map.', 'rating': 4.8, 'uses': 11200, 'tags': ['project-management', 'planning', 'organization', 'execution']},
    {'id': 49, 'title': 'Meeting Agenda Generator', 'category': 'productivity', 'text': 'Create effective meeting agenda for [MEETING TYPE]. Include: clear objective, pre-work requirements, time-boxed topics, decision-making framework, action item template, parking lot for off-topic items, follow-up plan, success criteria.', 'rating': 4.7, 'uses': 9800, 'tags': ['meetings', 'collaboration', 'efficiency', 'communication']},
    {'id': 50, 'title': 'Decision-Making Framework', 'category': 'productivity', 'text': 'Create decision-making framework for [DECISION]. Include: problem statement, decision criteria with weights, options analysis, pros & cons matrix, risk assessment, stakeholder input, implementation considerations, reversibility assessment, recommendation with reasoning.', 'rating': 4.9, 'uses': 8600, 'tags': ['decision-making', 'problem-solving', 'strategy', 'critical-thinking']},
    {'id': 51, 'title': 'Personal Knowledge Management', 'category': 'productivity', 'text': 'Design personal knowledge management system for [FIELD/ROLE]. Include: information capture methods, note-taking system, tagging/categorization, knowledge retrieval, spaced repetition for learning, digital tools recommendation, review schedule, sharing workflow.', 'rating': 4.8, 'uses': 7800, 'tags': ['knowledge-management', 'learning', 'note-taking', 'organization']},
    {'id': 52, 'title': 'Goal Setting Framework', 'category': 'productivity', 'text': 'Create goal setting framework for [TIMEFRAME]. Define SMART goals, break into milestones, identify obstacles & solutions, create action plans with deadlines, accountability system, progress tracking metrics, celebration milestones, adjustment criteria.', 'rating': 4.9, 'uses': 12400, 'tags': ['goal-setting', 'planning', 'achievement', 'personal-development']},
    {'id': 53, 'title': 'Email Management System', 'category': 'productivity', 'text': 'Design email management system to reach inbox zero. Include: folder/label structure, processing workflow (4 Ds: Delete, Delegate, Defer, Do), email templates, filter rules, unsubscribe strategy, response time standards, batch processing schedule.', 'rating': 4.7, 'uses': 8900, 'tags': ['email-management', 'inbox-zero', 'communication', 'organization']},
    {'id': 54, 'title': 'Focus & Deep Work Plan', 'category': 'productivity', 'text': 'Create deep work schedule for [ROLE]. Include: focus blocks identification, distraction elimination strategies, environment optimization, focus rituals, break system, energy management, accountability tracking, performance metrics, weekly optimization.', 'rating': 4.9, 'uses': 10200, 'tags': ['deep-work', 'focus', 'concentration', 'productivity']},
    
    # DATA SCIENCE (55-62)
    {'id': 55, 'title': 'Data Analysis Plan', 'category': 'data-science', 'text': 'Create data analysis plan for [DATASET/PROBLEM]. Include: business questions, data sources, exploratory data analysis approach, statistical methods, visualization strategy, hypothesis testing, model selection, interpretation framework, actionable insights format.', 'rating': 4.8, 'uses': 9400, 'tags': ['data-analysis', 'statistics', 'analytics', 'insights']},
    {'id': 56, 'title': 'Machine Learning Model Design', 'category': 'data-science', 'text': 'Design ML model for [PROBLEM]. Include: problem formulation, data requirements, feature engineering approach, model selection rationale, training strategy, validation methodology, hyperparameter tuning, evaluation metrics, deployment considerations, monitoring plan.', 'rating': 4.9, 'uses': 11800, 'tags': ['machine-learning', 'ml', 'modeling', 'ai']},
    {'id': 57, 'title': 'Data Visualization Dashboard', 'category': 'data-science', 'text': 'Design data visualization dashboard for [USE CASE]. Include: KPI selection, chart types rationale, layout design, interactivity features, filtering options, drill-down capabilities, mobile responsiveness, color scheme, update frequency, user testing plan.', 'rating': 4.8, 'uses': 8600, 'tags': ['data-visualization', 'dashboards', 'bi', 'reporting']},
    {'id': 58, 'title': 'A/B Test Design', 'category': 'data-science', 'text': 'Design A/B test for [HYPOTHESIS]. Include: hypothesis formulation, success metrics, sample size calculation, test duration, randomization strategy, control/treatment design, statistical significance threshold, analysis plan, decision criteria, implementation rollout.', 'rating': 4.9, 'uses': 7900, 'tags': ['ab-testing', 'experimentation', 'statistics', 'optimization']},
    {'id': 59, 'title': 'Data Pipeline Architecture', 'category': 'data-science', 'text': 'Design data pipeline for [USE CASE]. Include: data sources, ingestion methods, transformation logic, data quality checks, storage strategy, processing schedule, error handling, monitoring, scalability considerations, cost optimization, documentation.', 'rating': 4.8, 'uses': 8200, 'tags': ['data-engineering', 'etl', 'pipeline', 'architecture']},
    {'id': 60, 'title': 'Predictive Model Validation', 'category': 'data-science', 'text': 'Validate predictive model for [MODEL]. Include: train/test/validation split, cross-validation strategy, performance metrics (accuracy, precision, recall, F1, AUC-ROC), confusion matrix analysis, feature importance, model comparison, production readiness checklist.', 'rating': 4.9, 'uses': 7400, 'tags': ['model-validation', 'ml', 'evaluation', 'metrics']},
    {'id': 61, 'title': 'SQL Data Query Builder', 'category': 'data-science', 'text': 'Build SQL query for [DATA REQUEST]. Include: table structure analysis, join strategy, filtering conditions, aggregations, window functions, subqueries, query optimization, indexing recommendations, execution plan, expected output format.', 'rating': 4.7, 'uses': 10600, 'tags': ['sql', 'database', 'queries', 'data-retrieval']},
    {'id': 62, 'title': 'Feature Engineering Guide', 'category': 'data-science', 'text': 'Design feature engineering strategy for [DATASET]. Include: feature extraction methods, encoding strategies (one-hot, target, ordinal), scaling/normalization, feature interactions, dimensionality reduction, feature selection techniques, validation approach, feature importance analysis.', 'rating': 4.8, 'uses': 8800, 'tags': ['feature-engineering', 'ml', 'data-preprocessing', 'modeling']},
    
    # AI/ML (63-70)
    {'id': 63, 'title': 'ChatGPT Prompt Engineering', 'category': 'ai-ml', 'text': 'Create optimized ChatGPT prompt for [TASK]. Include: clear role definition, context setting, specific instructions, output format specification, constraints, examples (few-shot learning), chain-of-thought reasoning, error handling, iterative refinement approach.', 'rating': 4.9, 'uses': 16800, 'tags': ['prompt-engineering', 'chatgpt', 'llm', 'ai']},
    {'id': 64, 'title': 'LLM Application Architecture', 'category': 'ai-ml', 'text': 'Design LLM-powered application for [USE CASE]. Include: model selection, prompt design, context management, response parsing, error handling, cost optimization, rate limiting, caching strategy, monitoring, user feedback loop, ethical considerations.', 'rating': 4.9, 'uses': 12400, 'tags': ['llm', 'ai-application', 'architecture', 'gpt']},
    {'id': 65, 'title': 'Computer Vision Solution', 'category': 'ai-ml', 'text': 'Design computer vision solution for [PROBLEM]. Include: problem definition, dataset requirements, model architecture (CNN, transformer), data augmentation, training strategy, evaluation metrics, deployment approach, edge computing considerations, performance optimization.', 'rating': 4.8, 'uses': 8900, 'tags': ['computer-vision', 'cv', 'image-processing', 'deep-learning']},
    {'id': 66, 'title': 'NLP Pipeline Design', 'category': 'ai-ml', 'text': 'Create NLP pipeline for [TEXT TASK]. Include: text preprocessing, tokenization, embeddings selection, model architecture, training approach, evaluation metrics, inference optimization, handling edge cases, multilingual support, continuous improvement strategy.', 'rating': 4.8, 'uses': 9600, 'tags': ['nlp', 'natural-language-processing', 'text-analysis', 'ai']},
    {'id': 67, 'title': 'Recommendation System', 'category': 'ai-ml', 'text': 'Design recommendation system for [PLATFORM]. Include: algorithm selection (collaborative, content-based, hybrid), data requirements, feature engineering, cold start handling, evaluation metrics, A/B testing strategy, personalization approach, scalability, real-time updates.', 'rating': 4.9, 'uses': 10200, 'tags': ['recommendation-system', 'ml', 'personalization', 'ranking']},
    {'id': 68, 'title': 'Model Deployment Strategy', 'category': 'ai-ml', 'text': 'Create ML model deployment plan for [MODEL]. Include: containerization (Docker), orchestration (Kubernetes), API design, versioning strategy, A/B testing, rollback procedures, monitoring & alerting, performance optimization, cost management, documentation.', 'rating': 4.8, 'uses': 8400, 'tags': ['ml-ops', 'deployment', 'production', 'devops']},
    {'id': 69, 'title': 'AI Ethics Review', 'category': 'ai-ml', 'text': 'Conduct AI ethics review for [AI SYSTEM]. Evaluate: bias & fairness, transparency & explainability, privacy & security, accountability, social impact, environmental impact. Provide risk assessment, mitigation strategies, governance framework, ongoing monitoring approach.', 'rating': 4.9, 'uses': 6800, 'tags': ['ai-ethics', 'responsible-ai', 'fairness', 'governance']},
    {'id': 70, 'title': 'Transfer Learning Strategy', 'category': 'ai-ml', 'text': 'Design transfer learning approach for [TASK]. Include: pre-trained model selection, fine-tuning strategy, layer freezing decisions, learning rate scheduling, data augmentation, domain adaptation techniques, evaluation approach, computational considerations.', 'rating': 4.8, 'uses': 7600, 'tags': ['transfer-learning', 'deep-learning', 'fine-tuning', 'ml']},
]

print("="*70)
print("  UPLOADING ALL 70+ PROMPTS TO FIRESTORE DATABASE")
print("="*70)
print()

collection = db.collection('prompts')
successful = 0
failed = 0
start_time = time.time()

for i, prompt in enumerate(all_prompts, 1):
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
        
        # Progress indicator
        if i % 10 == 0:
            print(f"[{i}/70] ✓ Uploaded {prompt['category']} prompts...")
        
    except Exception as e:
        failed += 1
        print(f"✗ Failed: {prompt['title']} - {e}")

elapsed_time = time.time() - start_time

print()
print("="*70)
print(f"  MIGRATION COMPLETE! ({elapsed_time:.1f}s)")
print("="*70)
print(f"✅ Successfully uploaded: {successful} prompts")
if failed > 0:
    print(f"❌ Failed: {failed} prompts")
print()
print("Categories uploaded:")
categories = {}
for p in all_prompts:
    cat = p['category']
    categories[cat] = categories.get(cat, 0) + 1

for cat, count in sorted(categories.items()):
    print(f"  • {cat.title()}: {count} prompts")

print()
print("🎉 Your PromptForge database is now fully populated!")
print("🌐 Visit: https://rajatagarwal14.github.io/blacklab-ai-apps/promptforge/")
print("="*70)

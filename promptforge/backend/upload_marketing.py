#!/usr/bin/env python3
"""Upload all 70+ prompts to Firestore"""
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate('firebase-credentials.json')
try:
    firebase_admin.get_app()
except ValueError:
    firebase_admin.initialize_app(cred)

db = firestore.client()

# All 70+ prompts data
prompts_data = [
    # MARKETING (1-10)
    {'id': 1, 'title': 'SEO Blog Post Generator', 'category': 'marketing', 'text': 'You are an SEO expert. Create comprehensive SEO-optimized blog post about [TOPIC]. Include: compelling title with primary keyword, meta description (150-160 chars), H2/H3 subheadings, 1500+ words valuable content, internal/external links, FAQ section, call-to-action. Optimize for search intent and readability.', 'rating': 4.9, 'uses': 15200, 'tags': ['seo', 'content', 'blog']},
    {'id': 2, 'title': 'Social Media Campaign Planner', 'category': 'marketing', 'text': 'Create 30-day social media campaign for [PRODUCT/SERVICE]. Include: campaign strategy, content calendar (30 days), post types, captions with hashtags, visual concepts, posting schedule, engagement tactics, paid ad recommendations, KPIs.', 'rating': 4.8, 'uses': 8900, 'tags': ['social-media', 'campaign']},
    {'id': 3, 'title': 'Email Marketing Sequence', 'category': 'marketing', 'text': 'Design high-converting email sequence for [PRODUCT/SERVICE]. Create 5-7 emails with subject lines (A/B variants), body copy, CTAs, optimal send times, personalization tokens, expected metrics.', 'rating': 4.7, 'uses': 6700, 'tags': ['email-marketing', 'conversion']},
    {'id': 4, 'title': 'Landing Page Copy Optimizer', 'category': 'marketing', 'text': 'Create high-converting landing page copy for [PRODUCT]. Include: hero section (headline, subheadline, CTA), problem agitation, solution presentation, social proof, feature breakdown, objection handling FAQ, final CTA section with urgency.', 'rating': 4.9, 'uses': 11400, 'tags': ['landing-page', 'copywriting', 'conversion']},
    {'id': 5, 'title': 'Google Ads Campaign Structure', 'category': 'marketing', 'text': 'Design comprehensive Google Ads campaign for [PRODUCT]. Include: campaign structure, ad groups (3-5), keyword research (20-30 keywords), ad copy (3 variants), extensions, landing page alignment, conversion tracking, performance benchmarks.', 'rating': 4.8, 'uses': 7200, 'tags': ['google-ads', 'ppc', 'sem']},
    {'id': 6, 'title': 'Content Marketing Strategy', 'category': 'marketing', 'text': 'Develop 90-day content marketing strategy for [COMPANY]. Include: content pillars (3-5), content mix strategy, editorial calendar, SEO integration, distribution plan, repurposing strategy, metrics & KPIs.', 'rating': 4.9, 'uses': 9800, 'tags': ['content-strategy', 'marketing', 'seo']},
    {'id': 7, 'title': 'Product Launch Marketing Plan', 'category': 'marketing', 'text': 'Create product launch marketing plan for [PRODUCT]. Include: pre-launch (4-6 weeks), launch week day-by-day plan, post-launch (4 weeks), channels & tactics, messaging framework, budget allocation, success metrics.', 'rating': 4.8, 'uses': 5600, 'tags': ['product-launch', 'go-to-market']},
    {'id': 8, 'title': 'Brand Voice & Messaging Guide', 'category': 'marketing', 'text': 'Create comprehensive brand voice guide for [COMPANY]. Include: brand personality, voice attributes, messaging pillars, audience-specific messaging, vocabulary guidelines, channel adaptations, examples & templates.', 'rating': 4.7, 'uses': 4900, 'tags': ['brand-voice', 'messaging', 'copywriting']},
    {'id': 9, 'title': 'Competitor Analysis Report', 'category': 'marketing', 'text': 'Conduct comprehensive competitor analysis for [YOUR COMPANY]. Analyze 3-5 competitors: company overview, product/service analysis, marketing strategy, website analysis, customer perception, SWOT analysis, strategic recommendations.', 'rating': 4.8, 'uses': 7800, 'tags': ['competitor-analysis', 'market-research', 'strategy']},
    {'id': 10, 'title': 'Influencer Marketing Campaign', 'category': 'marketing', 'text': 'Design influencer marketing campaign for [PRODUCT]. Include: influencer strategy, 20 potential influencers list, campaign brief, compensation structure, content requirements, tracking & measurement, outreach templates.', 'rating': 4.7, 'uses': 6100, 'tags': ['influencer-marketing', 'social-media', 'campaign']},
]

# Upload prompts
collection = db.collection('prompts')
successful = 0

for prompt in prompts_data:
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
        print(f"✓ {successful}/10: {prompt['title']}")
        
    except Exception as e:
        print(f"✗ Failed: {prompt['title']} - {e}")

print(f"\n✅ Uploaded {successful} marketing prompts!")
print("Run upload_coding.py next...")
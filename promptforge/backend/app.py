from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore, auth
import os
from datetime import datetime
from functools import wraps

app = Flask(__name__)
CORS(app)

# Initialize Firebase
cred = credentials.Certificate('firebase-credentials.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Collections
PROMPTS_COLLECTION = 'prompts'
SUBMISSIONS_COLLECTION = 'submissions'
ANALYTICS_COLLECTION = 'analytics'

# Authentication decorator
def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({'error': 'No authentication token provided'}), 401
        
        try:
            decoded_token = auth.verify_id_token(token)
            request.user = decoded_token
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': 'Invalid authentication token'}), 401
    
    return decorated_function

# Admin check decorator
def require_admin(f):
    @wraps(f)
    @require_auth
    def decorated_function(*args, **kwargs):
        user_email = request.user.get('email', '')
        # Check if user is admin (you can customize this)
        admins = ['rajatagarwal14@example.com']  # Add your admin emails
        
        if user_email not in admins:
            return jsonify({'error': 'Admin access required'}), 403
        
        return f(*args, **kwargs)
    
    return decorated_function

# ==================== PUBLIC API ENDPOINTS ====================

@app.route('/api/prompts', methods=['GET'])
def get_prompts():
    """Get all approved prompts"""
    try:
        category = request.args.get('category')
        search = request.args.get('search', '').lower()
        
        prompts_ref = db.collection(PROMPTS_COLLECTION)
        
        # Filter by approval status
        query = prompts_ref.where('approved', '==', True)
        
        if category:
            query = query.where('category', '==', category)
        
        prompts = []
        for doc in query.stream():
            prompt = doc.to_dict()
            prompt['id'] = doc.id
            
            # Search filter
            if search:
                if search in prompt.get('title', '').lower() or search in prompt.get('text', '').lower():
                    prompts.append(prompt)
            else:
                prompts.append(prompt)
        
        return jsonify({'prompts': prompts, 'count': len(prompts)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/prompts/<prompt_id>', methods=['GET'])
def get_prompt(prompt_id):
    """Get a specific prompt by ID"""
    try:
        doc = db.collection(PROMPTS_COLLECTION).document(prompt_id).get()
        
        if not doc.exists:
            return jsonify({'error': 'Prompt not found'}), 404
        
        prompt = doc.to_dict()
        prompt['id'] = doc.id
        
        # Track view (analytics)
        track_analytics('view', prompt_id, prompt.get('category'))
        
        return jsonify(prompt), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/prompts/<prompt_id>/copy', methods=['POST'])
def copy_prompt(prompt_id):
    """Track when a prompt is copied"""
    try:
        doc = db.collection(PROMPTS_COLLECTION).document(prompt_id).get()
        
        if not doc.exists:
            return jsonify({'error': 'Prompt not found'}), 404
        
        prompt = doc.to_dict()
        
        # Increment copy count
        db.collection(PROMPTS_COLLECTION).document(prompt_id).update({
            'copy_count': firestore.Increment(1),
            'last_copied': datetime.utcnow()
        })
        
        # Track analytics
        track_analytics('copy', prompt_id, prompt.get('category'))
        
        return jsonify({'message': 'Copy tracked successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/submissions', methods=['POST'])
def submit_prompt():
    """Submit a new prompt for approval"""
    try:
        data = request.json
        
        # Validate required fields
        required = ['title', 'category', 'text']
        if not all(field in data for field in required):
            return jsonify({'error': 'Missing required fields'}), 400
        
        submission = {
            'title': data['title'],
            'category': data['category'],
            'text': data['text'],
            'expected_output': data.get('expected_output', ''),
            'author': data.get('author', 'Anonymous'),
            'submitted_at': datetime.utcnow(),
            'approved': False,
            'reviewed': False,
            'copy_count': 0,
            'view_count': 0
        }
        
        # Add to submissions collection
        doc_ref = db.collection(SUBMISSIONS_COLLECTION).add(submission)
        
        return jsonify({
            'message': 'Prompt submitted successfully',
            'id': doc_ref[1].id,
            'status': 'pending_review'
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all categories with prompt counts"""
    try:
        categories = [
            {'id': 'marketing', 'name': 'Marketing', 'icon': '📊'},
            {'id': 'coding', 'name': 'Coding', 'icon': '💻'},
            {'id': 'writing', 'name': 'Writing', 'icon': '✍️'},
            {'id': 'business', 'name': 'Business', 'icon': '💼'},
            {'id': 'project-management', 'name': 'Project Management', 'icon': '📋'},
            {'id': 'design', 'name': 'Design', 'icon': '🎨'},
            {'id': 'education', 'name': 'Education', 'icon': '🎓'},
            {'id': 'data-science', 'name': 'Data Science', 'icon': '📈'}
        ]
        
        # Add counts
        for category in categories:
            count = len(list(db.collection(PROMPTS_COLLECTION)
                           .where('category', '==', category['id'])
                           .where('approved', '==', True)
                           .stream()))
            category['count'] = count
        
        return jsonify({'categories': categories}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== ADMIN API ENDPOINTS ====================

@app.route('/api/admin/submissions', methods=['GET'])
@require_admin
def get_pending_submissions():
    """Get all pending submissions for review"""
    try:
        submissions = []
        query = db.collection(SUBMISSIONS_COLLECTION).where('reviewed', '==', False)
        
        for doc in query.stream():
            submission = doc.to_dict()
            submission['id'] = doc.id
            submissions.append(submission)
        
        return jsonify({'submissions': submissions, 'count': len(submissions)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/submissions/<submission_id>/approve', methods=['POST'])
@require_admin
def approve_submission(submission_id):
    """Approve a submission and move to prompts"""
    try:
        # Get submission
        submission_doc = db.collection(SUBMISSIONS_COLLECTION).document(submission_id).get()
        
        if not submission_doc.exists:
            return jsonify({'error': 'Submission not found'}), 404
        
        submission = submission_doc.to_dict()
        
        # Move to prompts collection
        submission['approved'] = True
        submission['reviewed'] = True
        submission['approved_at'] = datetime.utcnow()
        submission['approved_by'] = request.user.get('email')
        
        # Add to prompts
        prompt_ref = db.collection(PROMPTS_COLLECTION).add(submission)
        
        # Update submission status
        db.collection(SUBMISSIONS_COLLECTION).document(submission_id).update({
            'reviewed': True,
            'approved': True,
            'reviewed_at': datetime.utcnow(),
            'prompt_id': prompt_ref[1].id
        })
        
        return jsonify({
            'message': 'Submission approved',
            'prompt_id': prompt_ref[1].id
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/submissions/<submission_id>/reject', methods=['POST'])
@require_admin
def reject_submission(submission_id):
    """Reject a submission"""
    try:
        data = request.json
        reason = data.get('reason', 'No reason provided')
        
        # Update submission
        db.collection(SUBMISSIONS_COLLECTION).document(submission_id).update({
            'reviewed': True,
            'approved': False,
            'reviewed_at': datetime.utcnow(),
            'rejection_reason': reason,
            'reviewed_by': request.user.get('email')
        })
        
        return jsonify({'message': 'Submission rejected'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/prompts/<prompt_id>', methods=['DELETE'])
@require_admin
def delete_prompt(prompt_id):
    """Delete a prompt"""
    try:
        db.collection(PROMPTS_COLLECTION).document(prompt_id).delete()
        return jsonify({'message': 'Prompt deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== ANALYTICS API ENDPOINTS ====================

@app.route('/api/analytics/popular', methods=['GET'])
@require_admin
def get_popular_prompts():
    """Get most popular prompts by copies"""
    try:
        limit = int(request.args.get('limit', 10))
        
        prompts = []
        query = (db.collection(PROMPTS_COLLECTION)
                .where('approved', '==', True)
                .order_by('copy_count', direction=firestore.Query.DESCENDING)
                .limit(limit))
        
        for doc in query.stream():
            prompt = doc.to_dict()
            prompt['id'] = doc.id
            prompts.append(prompt)
        
        return jsonify({'prompts': prompts}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/stats', methods=['GET'])
@require_admin
def get_analytics_stats():
    """Get overall analytics statistics"""
    try:
        # Total prompts
        total_prompts = len(list(db.collection(PROMPTS_COLLECTION)
                                .where('approved', '==', True).stream()))
        
        # Total submissions
        total_submissions = len(list(db.collection(SUBMISSIONS_COLLECTION).stream()))
        
        # Pending submissions
        pending = len(list(db.collection(SUBMISSIONS_COLLECTION)
                          .where('reviewed', '==', False).stream()))
        
        # Total copies
        total_copies = 0
        for doc in db.collection(PROMPTS_COLLECTION).where('approved', '==', True).stream():
            total_copies += doc.to_dict().get('copy_count', 0)
        
        # Category breakdown
        categories = {}
        for doc in db.collection(PROMPTS_COLLECTION).where('approved', '==', True).stream():
            category = doc.to_dict().get('category', 'other')
            categories[category] = categories.get(category, 0) + 1
        
        return jsonify({
            'total_prompts': total_prompts,
            'total_submissions': total_submissions,
            'pending_review': pending,
            'total_copies': total_copies,
            'categories': categories
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== HELPER FUNCTIONS ====================

def track_analytics(action, prompt_id, category):
    """Track analytics event"""
    try:
        analytics_data = {
            'action': action,
            'prompt_id': prompt_id,
            'category': category,
            'timestamp': datetime.utcnow()
        }
        db.collection(ANALYTICS_COLLECTION).add(analytics_data)
    except Exception as e:
        print(f"Analytics tracking error: {e}")

# ==================== HEALTH CHECK ====================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'PromptForge API',
        'version': '1.0.0'
    }), 200

@app.route('/', methods=['GET'])
def home():
    """API home"""
    return jsonify({
        'name': 'PromptForge API',
        'version': '1.0.0',
        'endpoints': {
            'public': [
                'GET /api/prompts',
                'GET /api/prompts/<id>',
                'POST /api/prompts/<id>/copy',
                'POST /api/submissions',
                'GET /api/categories'
            ],
            'admin': [
                'GET /api/admin/submissions',
                'POST /api/admin/submissions/<id>/approve',
                'POST /api/admin/submissions/<id>/reject',
                'DELETE /api/admin/prompts/<id>',
                'GET /api/analytics/popular',
                'GET /api/analytics/stats'
            ]
        }
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

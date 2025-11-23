#!/usr/bin/env python3
"""
PromptForge - Admin Account Creator
Run this script once to create your first admin account.

Usage:
    python create_admin.py
    python create_admin.py --email admin@example.com --password YourPassword123
"""

import firebase_admin
from firebase_admin import credentials, auth
import argparse
import sys
import os

def create_admin_account(email=None, password=None):
    """Create admin account in Firebase"""
    
    # Default values
    if not email:
        email = input("Enter admin email (default: admin@promptforge.com): ").strip()
        if not email:
            email = "admin@promptforge.com"
    
    if not password:
        password = input("Enter admin password (min 6 chars): ").strip()
        if not password or len(password) < 6:
            print("❌ Password must be at least 6 characters")
            sys.exit(1)
    
    # Check if firebase credentials exist
    if not os.path.exists('firebase-credentials.json'):
        print("❌ Error: firebase-credentials.json not found!")
        print("📝 Please download your Firebase service account key and save it as 'firebase-credentials.json'")
        print("   Get it from: Firebase Console → Project Settings → Service Accounts → Generate New Private Key")
        sys.exit(1)
    
    try:
        # Initialize Firebase
        print("🔥 Initializing Firebase...")
        cred = credentials.Certificate('firebase-credentials.json')
        firebase_admin.initialize_app(cred)
        print("✅ Firebase initialized")
        
        # Check if user already exists
        print(f"\n🔍 Checking if {email} already exists...")
        try:
            existing_user = auth.get_user_by_email(email)
            print(f"⚠️  User {email} already exists (UID: {existing_user.uid})")
            
            upgrade = input("Do you want to upgrade this user to admin? (y/n): ").strip().lower()
            if upgrade == 'y':
                auth.set_custom_user_claims(existing_user.uid, {'admin': True, 'role': 'admin'})
                print("✅ User upgraded to admin!")
                return existing_user.uid
            else:
                print("❌ Operation cancelled")
                sys.exit(0)
        except auth.UserNotFoundError:
            pass  # User doesn't exist, continue to create
        
        # Create new admin user
        print(f"\n👤 Creating admin account for {email}...")
        user = auth.create_user(
            email=email,
            password=password,
            display_name='PromptForge Admin',
            email_verified=False
        )
        
        # Set custom claims for admin role
        print("🔐 Setting admin privileges...")
        auth.set_custom_user_claims(user.uid, {
            'admin': True,
            'role': 'admin',
            'created_via': 'script'
        })
        
        print("\n" + "="*60)
        print("✅ ADMIN ACCOUNT CREATED SUCCESSFULLY!")
        print("="*60)
        print(f"📧 Email:    {email}")
        print(f"🔑 Password: {password}")
        print(f"🆔 UID:      {user.uid}")
        print(f"👑 Role:     Admin")
        print("="*60)
        print("\n🎯 Next Steps:")
        print("1. Go to your admin panel:")
        print("   https://rajatagarwal14.github.io/blacklab-ai-apps/promptforge/admin.html")
        print(f"2. Login with: {email}")
        print("3. Start managing your prompts!")
        print("\n⚠️  IMPORTANT: Keep your credentials secure!")
        print("="*60)
        
        return user.uid
        
    except Exception as e:
        print(f"\n❌ Error creating admin account: {str(e)}")
        sys.exit(1)

def list_all_users():
    """List all existing users"""
    try:
        print("\n👥 Existing Users:")
        print("="*60)
        
        page = auth.list_users()
        if not page.users:
            print("No users found")
            return
        
        for user in page.users:
            # Get custom claims
            user_record = auth.get_user(user.uid)
            claims = user_record.custom_claims or {}
            is_admin = claims.get('admin', False)
            
            print(f"\n📧 Email: {user.email}")
            print(f"   UID: {user.uid}")
            print(f"   Role: {'👑 Admin' if is_admin else '👤 User'}")
            print(f"   Created: {user.user_metadata.creation_timestamp}")
        
        print("="*60)
        
    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    parser = argparse.ArgumentParser(
        description='Create admin account for PromptForge',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python create_admin.py
  python create_admin.py --email admin@example.com --password SecurePass123
  python create_admin.py --list
        """
    )
    
    parser.add_argument('--email', type=str, help='Admin email address')
    parser.add_argument('--password', type=str, help='Admin password (min 6 chars)')
    parser.add_argument('--list', action='store_true', help='List all existing users')
    
    args = parser.parse_args()
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         🎯 PromptForge Admin Account Creator 🎯             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Check if credentials exist
    if not os.path.exists('firebase-credentials.json'):
        print("❌ Error: firebase-credentials.json not found!")
        print("\n📝 Setup Instructions:")
        print("1. Go to Firebase Console: https://console.firebase.google.com")
        print("2. Select your project")
        print("3. Go to Project Settings → Service Accounts")
        print("4. Click 'Generate New Private Key'")
        print("5. Save the file as 'firebase-credentials.json' in this directory")
        print("6. Run this script again")
        sys.exit(1)
    
    # Initialize Firebase
    cred = credentials.Certificate('firebase-credentials.json')
    firebase_admin.initialize_app(cred)
    
    # List users if requested
    if args.list:
        list_all_users()
        return
    
    # Create admin account
    create_admin_account(args.email, args.password)

if __name__ == "__main__":
    main()

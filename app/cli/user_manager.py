import argparse
from typing import List
from sqlalchemy.orm import Session
from ..config import SessionLocal
from ..models import User


def create_user(username: str, password: str) -> User:
    db = SessionLocal()
    try:
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            print(f"Error: User '{username}' already exists")
            return None

        user = User(username=username, password=password)
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"User '{username}' created successfully")
        return user
    except Exception as e:
        db.rollback()
        print(f"Error creating user: {str(e)}")
        return None
    finally:
        db.close()


def list_users() -> List[User]:
    db = SessionLocal()
    try:
        users = db.query(User).all()
        return users
    finally:
        db.close()


def delete_user(username: str) -> bool:
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            print(f"Error: User '{username}' not found")
            return False

        db.delete(user)
        db.commit()
        print(f"User '{username}' deleted successfully")
        return True
    except Exception as e:
        db.rollback()
        print(f"Error deleting user: {str(e)}")
        return False
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(description="User Management CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Create command
    create_parser = subparsers.add_parser("create", help="Create a new user")
    create_parser.add_argument("username", help="Username for the new user")
    create_parser.add_argument("password", help="Password for the new user")

    list_parser = subparsers.add_parser("list", help="List all users")

    delete_parser = subparsers.add_parser("delete", help="Delete a user")
    delete_parser.add_argument("username", help="Username to delete")

    args = parser.parse_args()

    if args.command == "create":
        create_user(args.username, args.password)
    elif args.command == "list":
        users = list_users()
        if users:
            print("\nList of users:")
            for user in users:
                print(f"- {user.username}")
            print()
        else:
            print("No users found")
    elif args.command == "delete":
        delete_user(args.username)


if __name__ == "__main__":
    main()

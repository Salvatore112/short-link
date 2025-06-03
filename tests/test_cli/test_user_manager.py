from app.cli.user_manager import create_user, list_users, delete_user
from app.models import User


def test_create_user_success(db):
    """Test successful user creation"""
    user = create_user("newuser", "newpass")
    assert user is not None
    assert user.username == "newuser"
    assert isinstance(user.id, int)


def test_create_user_duplicate(db):
    """Test duplicate user creation fails"""
    create_user("duplicate", "pass1")
    user = create_user("duplicate", "pass2")
    assert user is None  # Should return None for duplicate


def test_list_users(db):
    """Test listing all users"""
    # Create test users
    create_user("user1", "pass1")
    create_user("user2", "pass2")

    users = list_users()
    assert len(users) >= 2
    usernames = [u.username for u in users]
    assert "user1" in usernames
    assert "user2" in usernames


def test_delete_user_success(db):
    """Test successful user deletion"""
    create_user("todelete", "password")
    result = delete_user("todelete")
    assert result is True

    # Verify user is gone
    users = list_users()
    assert "todelete" not in [u.username for u in users]


def test_delete_nonexistent_user(db):
    """Test deleting non-existent user"""
    result = delete_user("nonexistent")
    assert result is False

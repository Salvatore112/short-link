from app.cli.user_manager import create_user, list_users, delete_user
from app.models import User


def test_create_user(db):
    user = create_user("cli_test", "password")
    assert user.username == "cli_test"
    assert isinstance(user.id, int)


def test_list_users(db):
    create_user("user1", "pass1")
    create_user("user2", "pass2")
    users = list_users()
    assert len(users) >= 2
    assert any(u.username == "user1" for u in users)


def test_delete_user(db):
    create_user("to_delete", "password")
    result = delete_user("to_delete")
    assert result is True
    users = list_users()
    assert not any(u.username == "to_delete" for u in users)

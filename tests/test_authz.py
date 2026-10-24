from lead_harvester.authz import PERMISSIONS, is_permitted


def test_reviewer_and_admin_are_permitted_for_registered_permissions():
    for permission in PERMISSIONS:
        assert is_permitted(permission, "reviewer") is True
        assert is_permitted(permission, "admin") is True


def test_viewer_is_denied_for_every_registered_permission():
    for permission in PERMISSIONS:
        assert is_permitted(permission, "viewer") is False


def test_unregistered_permission_denies_every_role_by_default():
    assert is_permitted("not_a_real_permission", "admin") is False
    assert is_permitted("not_a_real_permission", "reviewer") is False
    assert is_permitted("not_a_real_permission", "viewer") is False

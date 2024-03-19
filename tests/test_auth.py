from sqlalchemy import insert, select

from src.auth.models import Role
from tests.conftest import client, _async_session_maker

# ORDER MATTERS

# REQUIRED
async def test_add_role():
    async with _async_session_maker() as session:
        stmt = insert(Role).values(id=1, name="user")
        await session.execute(stmt)
        await session.commit()

        query = select(Role)
        result = await session.execute(query)
        role_list = result.scalars().all()
        assert len(role_list) == 1
        assert role_list[0].name == "user"


def test_register():
    data = {
        "username": "string",
        "email": "user@example.com",
        "password": "string"
    }

    res = client.post("/auth/register", json=data)

    assert res.status_code == 201
    assert res.json() == {'id': 1, 'email': 'user@example.com', 'is_active': True, 'is_superuser': False,
                          'is_verified': False, 'role_id': 1, 'username': 'string'}





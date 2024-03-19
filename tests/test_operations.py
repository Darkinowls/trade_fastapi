from httpx import AsyncClient


# ac is a fixture
async def test_add_operation(ac: AsyncClient):
    res = await ac.post("/operations/",
                        json={
                            "quantity": 0,
                            "figi": "string",
                            "instrument_type": "string",
                            "type": "string"
                        }
                        )
    assert res.status_code == 200
    assert res.json() == {'message': True}


async def test_get_operations(ac: AsyncClient):
    res = await ac.get("/operations/?bigger_than=0")
    assert res.status_code == 200
    assert len(res.json()['message']) == 1

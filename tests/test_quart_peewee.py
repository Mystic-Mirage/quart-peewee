import pytest
from peewee_aio.fields import CharField
from quart import Quart, request

from quart_peewee import QuartPeewee


@pytest.mark.asyncio
async def test_quart_peewee(tmp_path):
    app = Quart(__name__)
    db = QuartPeewee(f"aiosqlite:///{tmp_path}/test.db")
    db.init_app(app)

    class User(db.Model):
        name = CharField(unique=True)

    await db.create_tables()

    @app.route("/create_user", methods=["POST"])
    async def create_user():
        data = await request.get_json()
        await User.create(name=data["name"])
        return ""

    @app.route("/get_users", methods=["GET"])
    async def get_users():
        return await User.select().dicts()

    @app.route("/delete_user", methods=["DELETE"])
    async def delete_user():
        data = await request.get_json()
        await User.delete().where(User.name == data["name"])
        return ""

    test_client = app.test_client()

    res = await test_client.post("/create_user", json={"name": "test"})
    assert res.status_code == 200

    res = await test_client.get("/get_users")
    json = await res.get_json()
    assert json[0]["name"] == "test"

    await test_client.delete("/delete_user", json={"name": "test"})
    res = await test_client.get("/get_users")
    json = await res.get_json()
    assert len(json) == 0

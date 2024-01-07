# Quart-Peewee

Integration between the [Quart](https://github.com/pallets/quart) web framework and the [Peewee ORM](https://github.com/coleifer/peewee) through the [Peewee-AIO](https://github.com/klen/peewee-aio)

## Installation

```
pip install quart-peewee
```

## Usage

```python
from peewee_aio.fields import CharField
from quart import Quart, request
from quart_peewee import QuartPeewee

app = Quart(__name__)
db = QuartPeewee("aiosqlite:///app.db")
db.init_app(app)


class User(db.Model):
    name = CharField(unique=True)


@app.before_serving
async def before_serving():
    await db.create_tables()


@app.route("/create_user", methods=["POST"])
async def create_user():
    data = await request.get_json(force=True)
    await User.create(name=data["name"])
    return ""


@app.route("/get_users", methods=["GET"])
async def get_users():
    return await User.select().dicts()


@app.route("/delete_user", methods=["DELETE"])
async def delete_user():
    data = await request.get_json(force=True)
    await User.delete().where(User.name == data["name"])
    return ""


if __name__ == "__main__":
    app.run()
```

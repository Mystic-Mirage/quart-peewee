from functools import cached_property
from typing import Type

from peewee_aio import AIOModel, Manager
from quart import Quart, g


class QuartPeewee(Manager):
    def init_app(self, app: Quart) -> "QuartPeewee":
        # noinspection PyTypeChecker
        app.before_serving(self.connect)
        app.after_serving(self.disconnect)

        def before_request():
            g.database = self

        def teardown_request(_):
            del g.database

        app.before_request(before_request)
        app.teardown_request(teardown_request)

        return self

    # noinspection PyPep8Naming
    @cached_property
    def Model(self) -> Type[AIOModel]:
        manager = self

        class Model(AIOModel):
            def __init_subclass__(cls):
                manager.register(cls)

        return Model

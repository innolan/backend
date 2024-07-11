from src.api.auth.routes import router as router_auth
from src.api.users.routes import router as router_users
from src.api.test.routes import router as router_test
from src.api.metrics.routes import router as router_metrics

routers = [
    router_auth,
    router_users,
    router_metrics,
    router_test,
]

__all__ = ["routers", *routers]

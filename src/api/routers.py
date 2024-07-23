from src.api.auth.routes import router as router_auth
from src.api.users.routes import router as router_users
from src.api.test.routes import router as router_test
from src.api.metrics.routes import router as router_metrics
from src.api.matching.routes import router as router_matching

routers = [
    router_auth,
    router_users,
    router_metrics,
    router_test,
    router_test,
    router_matching,
]

__all__ = ["routers", *routers]

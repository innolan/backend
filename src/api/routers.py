from src.api.auth.routes import router as router_auth

from src.api.users.routes import router as router_users

routers = [
    router_auth,
    router_users,
]

__all__ = ["routers", *routers]

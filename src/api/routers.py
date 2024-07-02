from src.api.auth.routes import router as router_auth
from src.api.profiles.routes import router as router_profiles

routers = [router_auth, router_profiles]

__all__ = ["routers", *routers]

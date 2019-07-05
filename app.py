import os

from dotenv_config import Config

from yutti import Yutti
from yutti.modules.pages.blueprints.admin import bp as admin_blueprint
from yutti.modules.pages.blueprints.auth import bp as auth_blueprint
from yutti.modules.pages.blueprints.profile import bp as profile_blueprint
from yutti.modules.pages.blueprints.tickets import bp as tickets_blueprint

# Initialize with given config:
app = Yutti(__name__)


# Register all application Blueprints:
# ------------------------------------
app.register_blueprint(auth_blueprint)
app.register_blueprint(admin_blueprint)
app.register_blueprint(profile_blueprint)
app.register_blueprint(tickets_blueprint)
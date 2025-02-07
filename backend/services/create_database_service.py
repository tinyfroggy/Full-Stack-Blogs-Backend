# get dependencies from dependencies/database.py
from dependencies.database import Base, engine


def create_database():
    from models.blogs_models import Blog
    from models.users_models import User
    from models.admins_models import Admin

    Base.metadata.create_all(bind=engine)

# in terminal add:
#  cd backend
#  python
#  from services import create_database_service
#  create_database_service.create_database()

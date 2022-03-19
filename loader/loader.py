import models.users as models
from configs.database import engine
import sys
sys.path.append("..")
models.Base.metadata.create_all(bind=engine)  # bulit db with the models file

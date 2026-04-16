from database import engine, Base
import models  

print(Base.metadata.tables.keys())

Base.metadata.create_all(bind=engine)
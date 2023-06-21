from sqlalchemy import create_engine, MetaData

# Replace 'your_password' with the actual password for the 'root' user
engine = create_engine('mysql+pymysql://root:guddu29@localhost:3306/fastapi_curd')
meta = MetaData()
con = engine.connect()

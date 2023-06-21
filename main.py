from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from schemas.student import Student
from config.db import con
from models.index import students

app = FastAPI()

@app.get('/api/students')
async def index():
    data = con.execute(students.select()).fetchall()
    data = [dict(row._asdict()) for row in data]
    return {
        "success": True,
        "data": jsonable_encoder(data)
    }

@app.post('/api/students')
async def store(student: Student):
    data = con.execute(students.insert().values(
        name=student.name,
        email=student.email,
        age=student.age,
        country=student.country,
    ))
    con.commit()
    
    if data.is_insert:
        return {
            "success": True,
            "msg": "Student Stored Successfully"
        }
    else:
        return {
            "success": False,
            "msg": "Some Problem"
        }

@app.patch('/api/students/{id}')
async def update(id: int, student: Student):
    data = con.execute(students.update().values(
        name=student.name,
        email=student.email,
        age=student.age,
        country=student.country,
    ).where(students.c.id == id))
    
    con.commit() 
    
    if data.rowcount > 0:
        return {
            "success": True,
            "msg": "Student Updated Successfully"
        }
    else:
        return {
            "success": False,
            "msg": "Some Problem"
        }

# update data
@app.put('/api/students/{id}')
async def edit_data(id:int):
    data=con.execute(students.select().where(students.c.id==id)).fetchall()
    data = [dict(row._asdict()) for row in data]

    return {
        "success": True,
        "data":data
    }
@app.delete('/api/students/{id}')
async def delete(id: int):
    data = con.execute(students.delete().where(students.c.id == id))
    con.commit()
    
    if data.rowcount > 0:
        return {
            "success": True,
            "msg": "Student Deleted Successfully"
        }
    else:
        raise HTTPException(status_code=404, detail="Student not found")

# search data
@app.get('/api/students/{search}')
async def search(search: str):
    data = con.execute(students.select().where(students.c.name.like('%' + search + '%'))).fetchall()
    data = [dict(row._asdict()) for row in data]
    
    return {
        "success": True,
        "data": jsonable_encoder(data)
    }

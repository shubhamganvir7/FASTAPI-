from fastapi import Depends, FastAPI,Request,Form,status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from database import engine,SessionLocal
import models
from sqlalchemy.orm import Session
from database import Base


models.Base.metadata.create_all(bind=engine)

app=FastAPI()

templates=Jinja2Templates(directory="templates")


app.mount("/static",StaticFiles(directory="static"),name="static")

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.get("/")
def home(request:Request,db:Session=Depends(get_db)):
    users=db.query(models.User).order_by(models.User.id.desc())
    return templates.TemplateResponse("index.html",{"request":request,"users":users})

@app.post("/add")
def add(request:Request,name:str=Form(...),DEPARTMAENT:str=Form(...),email:str=Form(...),db:Session=Depends(get_db)):
    print(name,DEPARTMAENT,email)
    users=models.User(name=name,DEPARTMAENT=DEPARTMAENT,email=email)
    print(users)
    db.add(users)
    db.commit()
    
    
    return RedirectResponse(url=app.url_path_for("home"),status_code=status.HTTP_303_SEE_OTHER)

@app.get("/addnew")
def addnew(request: Request):
    return templates.TemplateResponse("add.html", {"request": request})

@app.get("/edit/{user_id}")
async def edit(request: Request, user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    print(user)
    return templates.TemplateResponse("edit.html", {"request": request, "user": user})
 
@app.post("/update/{user_id}")
async def update(request: Request, user_id: int, name: str = Form(...), DEPARTMAENT: str = Form(...), email: str = Form(...), db: Session = Depends(get_db)):
    users = db.query(models.User).filter(models.User.id == user_id).first()
    users.name = name
    users.DEPARTMAENT = DEPARTMAENT
    users.email = email
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)
 
@app.get("/delete/{user_id}")
async def delete(request: Request, user_id: int, db: Session = Depends(get_db)):
    users = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(users)
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)
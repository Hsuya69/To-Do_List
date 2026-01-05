
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from App.routes import users,delete,insert,update

app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(update.router)
app.include_router(insert.router)
app.include_router(delete.router)







        
        

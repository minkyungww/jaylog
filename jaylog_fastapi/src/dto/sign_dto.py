from pydantic import BaseModel


class ReqSignUp(BaseModel):
    id : str
    password : str
    simpleDesc : str
    
class ResSignUp(BaseModel):
    idx : int
    
    class Config:
        orm_mode = True
        

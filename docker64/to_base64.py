# Author: Lin Tun Naing
# StudentID: st122403
# Contact: st122403@ait.asia


### Import libraries
from fastapi import FastAPI
import base64 
from pydantic import BaseModel
from fastapi.responses import JSONResponse


app = FastAPI()

class MyInput(BaseModel):
    text: str

### Convert input string to base64 string
@app.post('/convert')
def convert(input: MyInput)->str:

    text = input.text
    base64_str = base64.b64encode(text.encode("utf-8")).decode('utf-8')
    return JSONResponse(content=base64_str)
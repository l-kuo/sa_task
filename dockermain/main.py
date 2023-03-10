# Author: Lin Tun Naing
# StudentID: st122403
# Contact: st122403@ait.asia


### Import libraries
from fastapi import FastAPI, UploadFile, File, HTTPException
from PIL import Image, ImageDraw
from io import BytesIO
import base64 
import requests
# import uvicorn


### Initialize the FastAPI instance
app = FastAPI()

@app.get('/')
def read_root():
    return {'Hello': 'World'}

@app.post('/convert_csv')
async def converter(tsv_file:UploadFile=File(...))->list:
    """
    This function converts the tab-separated-values file into comma-separated-values

    Args:
        tsv_file(UploadFile): The .tsv file to be uploaded.

    Returns:
        list: A list of csv converted strings.
    """

    if tsv_file.content_type == "text/tab-separated-values":    ### Check file format
        try:
            data = await tsv_file.read()    ### wait for the reading file
            rows = data.decode().split('\n')    
            header = rows[0].strip().split(',')
            name_array = []
            for row in rows[1:]:
                if row:
                    new_row = row.replace('\t', ',')
                    name_array.append(new_row)
            name_array.insert(0, header[0])

            return name_array
        
        ### this exception raise error when converting the file
        except Exception as e:
            print("Something wrong during the file conversion process")
            raise HTTPException(status_code=400, detail=str(e))

    ### This raise the value error for incorrect format (.tsv)
    else:
        raise ValueError("Something wrong with the input file format.")

@app.post('/drawbb')
async def drawbb(img_file: UploadFile=File(...)):

    x_topleft = 192
    y_topleft = 180
    width = 384 
    height = 75
    try:
        img = Image.open(BytesIO(await img_file.read()))
        w, h = img.size

        if x_topleft < 0 or y_topleft < 0 or x_topleft+width > w or y_topleft+height > h:
            raise ValueError("The image size is not appropriate for the given bounding box.")

        draw = ImageDraw.Draw(img)
        draw.rectangle([x_topleft, y_topleft, x_topleft+width, y_topleft+height], outline='red', width=3)

        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='PNG')
        # img.tobytes("xbm", "rgb")
        img_byte_arr = img_byte_arr.getvalue()
        # cv2.rectangle(img, (x_topleft, y_topleft), (x_topleft+width, y_topleft+height), (0, 0, 255), 3)
        # cv2.imwrite("imgbb.png", img)
        # img = cv2.imencode('.png', img)[1].tobytes('hex', 'rgb')
        encoded_img = base64.b64encode(img_byte_arr)
        # print("Get value: ", encoded_img)
        return {"Image": encoded_img}
    except Exception as e:
        print(e)


username = 'Lin Tun Naing'
@app.post('/convert_name/')
def convert_name(name:str, text:str):
    if name != username:
        return {"UserError": "Permission denied for this user."}
    
    else:
        try:
            response = requests.post("http://base64:6464/convert", json={"text": text})
            response.raise_for_status() # will raise error is failed response
            # print(response.json())
            return {"base64" : response.json()}
        except Exception as e:
            return {"Error": f"Conversion error: {str(e)}"}
        

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port = 8080)
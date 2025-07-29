from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import pyfiglet
from run import main
from utils import utils
from contextlib import asynccontextmanager

def asciifiglet(text: str):
    ascii_art = pyfiglet.figlet_format(text)
    print(ascii_art)

@asynccontextmanager
async def life_span(app: FastAPI):
    asciifiglet("RFE ANALYZER SERVER HAS STARTED")
    yield
    asciifiglet("RFE ANALYZER SERVER HAS ENDED")

app = FastAPI(
    title="RFE Analyzer",
    version="v1",
    description="This is a simple server setup for the RFE project",
    lifespan=life_span
)

@app.get("/")
async def home():
    return {"status": "successful", "response": "You are welcome to the server!"}

@app.post("/upload")
async def uploadEB1Petition(file: UploadFile = File(...)):
    contents = await file.read()
    filename = file.filename

    file_path = f"temp_{filename}"
    with open(file_path, "wb") as f:
        f.write(contents)

    result: dict = main(file_path=file_path)

    output_path = utils.CriterionDocCreator(result)
    utils.jsonSaver(result)

    return FileResponse(
        output_path,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename="EB1A_Assessment_Report.docx"
    )

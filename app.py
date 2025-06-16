from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from puzzle import Puzzle
from rotate import Rotate

app = FastAPI()
puzzle = Puzzle()
rotate = Rotate()

@app.post("/captcha/puzzle/")
async def puzzle_server(piece: UploadFile = File(...), background: UploadFile = File(...)):
    path1 = await piece.read()
    path2 = await background.read()
    result = puzzle.solve(path1, path2)
    return JSONResponse(content=result)

@app.post("/captcha/rotate/")
async def rotate_server(inner: UploadFile = File(...), outer: UploadFile = File(...)):
    path1 = await inner.read()
    path2 = await outer.read()
    result = rotate.solve(path1, path2)
    return JSONResponse(content=result)
from fastapi import FastAPI
from FastAPIDoc import apiDoc
app = FastAPI()
apiDoc(app)

@app.get("/ssd")
def read_root():
    return {"Hello": "World"}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=888, reload=False, debug=True)

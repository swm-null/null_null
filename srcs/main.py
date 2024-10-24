from fastapi import FastAPI
import uvicorn
from init import init
from routers import embedding, memo, parser, search

app = FastAPI(
    title="Oatnote AI",
    description="after PR #91, https://github.com/swm-null/null_null/pull/91",
    version="0.2.41",
)
init(app)
    
@app.get("/")
async def default():
    return "yes. it works."

app.include_router(embedding.router)
app.include_router(memo.router)
app.include_router(parser.router)
app.include_router(search.router)

if __name__ == '__main__':
    uvicorn.run(app)

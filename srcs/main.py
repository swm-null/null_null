from fastapi import FastAPI
import uvicorn
from init import init
from routers import embedding, importer, memo, search

app = FastAPI(
    title="Oatnote AI",
    description="after PR NULL-675 hotfix batch structures(#131), https://github.com/swm-null/null_null/pull/131",
    version="0.2.122",
)
init(app)
    
@app.get("/")
async def default():
    return "yes. it works."

app.include_router(embedding.router)
app.include_router(memo.router)
app.include_router(importer.router)
app.include_router(search.router)

if __name__ == '__main__':
    uvicorn.run(app)

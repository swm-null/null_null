from fastapi import FastAPI
import uvicorn
from init import init
from routers import embedding, importer, memo, search

app = FastAPI(
    title="Oatnote AI",
    description="after PR NULL-588 fixed: modified headers to bypass anti-crawling webs(#110), https://github.com/swm-null/null_null/pull/110",
    version="0.2.80",
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

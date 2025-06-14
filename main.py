import asyncio
from fastapi import FastAPI, HTTPException, status, Query, Depends
from sqlalchemy import select, delete, asc, desc
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from models import ShopItem
from schemas import ItemCreate, ItemResponse
from db import init_db, get_db

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_db()

async def get_item_or_404(item_id: int, db: AsyncSession) -> ShopItem:
    result = await db.execute(select(ShopItem).where(ShopItem.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.get("/items/", response_model=List[ItemResponse])
async def get_items(
    name: Optional[str] = Query(None, description="Filter by name"),
    category: Optional[str] = Query(None, description="Filter by category"),
    purchased: Optional[bool] = Query(None, description="Filter by purchased status"),
    sort_by: Optional[str] = Query(None, pattern="^(createdAt|updatedAt)$", description="Sort by field"),
    sort_order: Optional[str] = Query("asc", pattern="^(asc|desc)$", description="Sort order"),
    limit: int = Query(100, ge=1, le=1000, description="Limit number of results"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    db: AsyncSession = Depends(get_db),
):
    query = select(ShopItem)
    if name:
        query = query.where(ShopItem.name.ilike(f"%{name}%"))
    if category:
        query = query.where(ShopItem.category == category)
    if purchased is not None:
        query = query.where(ShopItem.purchased == purchased)
    if sort_by:
        column = ShopItem.created_at if sort_by == "createdAt" else ShopItem.updated_at
        query = query.order_by(asc(column) if sort_order == "asc" else desc(column))
    query = query.limit(limit).offset(offset)
    result = await db.execute(query)
    return result.scalars().all()

@app.post("/items/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def add_item(item: ItemCreate, db: AsyncSession = Depends(get_db)):
    new_item = ShopItem(

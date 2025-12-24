from fastapi import FastAPI, HTTPException, Depends
from src.schemas.patients_schema import UserBase, UserCreate, UserRead
from src.db.session import User, Provider, Availability, Appointment, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select

# Here the 'create_db_and_tables' function runs before the app
@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)



@app.post("/register", response_model=UserRead)
async def register_users(
    user_in: UserCreate,
    session: AsyncSession = Depends(get_async_session)
    ):
    # Query the db to check if user already exists
    query = select(User).where(User.email == user_in.email)
    result = await session.execute(query)
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="User already registered")
    
    # Maap Pydantic data so SQLAlchemy Model
    new_user = User(
        full_name = user_in.full_name,
        email = user_in.email,
        role = user_in.role,
        hashed_password = user_in.password
    )

    # Commit to the database
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user

@app.get("/users", response_model=UserBase)
async def get_all_users(session: AsyncSession = Depends(get_async_session)):
    query = select(User)
    result = await session.execute(query)
    return result.scalars().all()


 

"""
@app.get("/profile/{profile_id}")
def get_profile_by_id(profile_id: int) -> ProfileResponse:
    if profile_id not in profile_data:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile_data.get(profile_id)

@app.post("/profile")
def create_profile(profile: ProfileCreate) -> ProfileResponse:
    new_profile = {"first_name": profile.first_name,
                    "last_name": profile.last_name,
                    "dob": profile.dob}
    profile_data[max(profile_data.keys()) + 1] = new_profile
    return new_profile
"""

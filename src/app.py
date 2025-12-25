from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import auth_backend, current_active_user, fastapi_users
from src.db.session import (
    Appointment,
    Availability,
    Provider,
    User,
    create_db_and_tables,
    get_async_session,
)
from src.schemas.patients_schema import (
    ProviderBase,
    ProviderRead,
    UserCreate,
    UserRead,
    UserRole,
    UserUpdate,
)


# Here the 'create_db_and_tables' function runs before the app
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Define the lifespan function"""
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix='/auth',
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead), prefix='/auth', tags=["auth"]
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix='/users',
    tags=["users"],
)


@app.get("/users", response_model=list[UserRead])
async def get_all_users(session: AsyncSession = Depends(get_async_session)):
    query = select(User)
    result = await session.execute(query)
    return result.scalars().all()


# ------- Providers endpoints ------
@app.post("/providers", response_model=list[ProviderRead])
async def create_provider(
    provider_data: ProviderBase,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    # Security Check: Ensure the user actually has the provider role
    if user.role != UserRole.PROVIDER:
        raise HTTPException(
            status_code=403,
            detail="Only users with 'provider' role can create a profile",
        )

    # Check if profile already exists to prevent duplicates
    existing_provider = await session.execute(
        select(Provider).where(Provider.user_id == user.id)
    )
    if existing_provider.scalar_one_or_none():
        raise HTTPException(
            status_code=400, detail="Provider profile already exists"
        )

    new_provider = Provider(**provider_data.model_dump(), user_id=user.id)

    session.add(new_provider)
    await session.commit()
    await session.refresh(new_provider)
    return new_provider


@app.get("/providers")
async def list_providers(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Provider))
    return result.scalars().all()


# ------- Availability endpoints ------

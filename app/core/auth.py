from datetime import datetime, timedelta, timezone
from typing import Annotated, List, Union
import os
import secrets
import bcrypt
from dotenv import load_dotenv
from jose import JWTError, jwt
from pydantic import BaseModel, ValidationError
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes, HTTPBasic, HTTPBasicCredentials

from core.database import SessionLocal
from models.api_user_model import Api_usuario

load_dotenv()

# OAuth2 and HTTP Basic security
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
security = HTTPBasic()

# JWT configuration
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRES_IN = 300  # seconds

# Role definitions with associated scopes
ROLES = {
    "viewer": ["profile.read", "data.view"],
    "editor": ["profile.read", "data.view", "data.edit"],
    "manager": ["profile.read", "data.*"],
    "admin": ["*"],  # Full access to all scopes
}

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Token schema
class Token(BaseModel):
    access_token: str
    token_type: str

# Token data structure
class TokenData(BaseModel):
    username: Union[str, None] = None
    scopes: List[str] = []

# Public user model
class User(BaseModel):
    username: str
    full_name: Union[str, None] = None
    email: Union[str, None] = None
    token_expire_minutes: Union[int, None] = None
    role: Union[str, None] = None
    disabled: Union[bool, None] = None

# Internal user model with hashed password
class UserInDB(User):
    hashed_password: str

# Password verification using bcrypt
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

# Password hashing using bcrypt
def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

# Fetch a user from the database by username
def get_user(db: Session, username: str):
    return db.query(Api_usuario).filter(Api_usuario.username == username).first()

# Authenticate a user with username and password
def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

# Create a JWT access token
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, os.getenv('SECRET_KEY'), algorithm=ALGORITHM)

# Basic authentication handler (for CLI or simple scripts)
def get_current_username_basic(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    db: Session = Depends(get_db)
):
    user = get_user(db, credentials.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    is_valid_username = secrets.compare_digest(credentials.username.encode("utf-8"), user.username.encode("utf-8"))
    is_valid_password = verify_password(credentials.password, user.hashed_password)

    if not (is_valid_username and is_valid_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# Validate and decode JWT token, enforce security scopes
async def get_current_user(
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db)
):
    authenticate_value = f'Bearer scope="{security_scopes.scope_str}"' if security_scopes.scopes else "Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized user",
        headers={"WWW-Authenticate": authenticate_value},
    )

    try:
        payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(username=username, scopes=token_scopes)
    except (JWTError, ValidationError):
        raise credentials_exception

    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception

    if security_scopes.scopes:
        if not any(scope in token_data.scopes for scope in security_scopes.scopes):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Insufficient permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user

# Ensure that user is active (not disabled)
async def get_current_active_user(
    current_user: Annotated[User, Security(get_current_user)],
    db: Session = Depends(get_db)
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


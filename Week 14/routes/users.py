from fastapi import APIRouter, HTTPException
from schema import User, UserCreate
from user_store import UserStore               # Import our new UserStore Class !!!

router = APIRouter()

store = UserStore("users.txt")


# Each endpoint now just calls the appropriate UserStore method

@router.post("/", response_model = User)
def create_user(user: UserCreate):
    new_user = store.create_user(user.dict())   # Try to create the user using the UserStore method
    if new_user is None:                        # Check if creation failed; email already exists
        raise HTTPException(status_code = 400, detail = "Email already registered")
    
    return new_user

@router.get("/", response_model = list[User])
def get_all_users():
    return store.load()


@router.get("/search", response_model = list[User])
def search_users(q: str = None):
    if not q:
        return []
    
    users = store.load()
    results = [user for user in users if q.lowe() in user['name'].lower()]          # Filters users whose names contain the search term
    return results

@router.get("/{user_id}", response_model = User)
def get_user(user_id: int):                     # find_by_id method now handles the search logic
    user = store.find_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail = "User not found")
    return user

@router.put("/{user_id}", response_model= User)
def update_user(user_id: int, user_update: UserCreate):
    updated_user = store.update_user(user_id, user_update.dict())
    if updated_user is None:
        # Determine why it failed
        if store.find_by_id(user_id) is None:                                   # Check if user exists
            raise HTTPException(status_code=404, detail = "User not found")
        else:
            raise HTTPException(status_code=400, detail = "Email already registered")       # User exists but update failed because of the email conflict
    return updated_user

@router.delete("/{user_id}")
def delete_user(user_id: int):
    if store.delete_user(user_id):
        return {"message": f"User {user_id} deleted successfully"}
    
    raise HTTPException(status_code=404, detail = "User not found")                         # If delete_user returned False and user wasn't found

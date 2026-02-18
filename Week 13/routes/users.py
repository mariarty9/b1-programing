from fastapi import APIRouter, HTTPException
from schema import User, UserCreate
import json
import os

router = APIRouter()

# Need to implement these helper functions:
# read_users()
# write_users()
# get_next_id()

#6 Endpoints
# POST /users                   create a user
# GET /users                    get all users
# GET /users/search?q=          search users by name
# GET /users/{id}               get user by ID
# PUT /users/{id}               update user
# DELETE /users/{id}            delete user

DATA_FILE = "users.txt"                         # THis will store each user as a JSON object

# Helper function read_users()
def read_users():                               # Read all users from the text file
    if not os.path.exists(DATA_FILE):           # Checks if the file exists, if not return empty list
        return []
    
    users = []
    try:
        with open(DATA_FILE, 'r') as f:       # Open the file in read mode
            for line in f:
                if line.strip():          # Strip whitespace and check if line has content
                    users.append(json.loads(line))      
        return users 
    except Exception as e:                      # In case anything goes wrong (file corruption, etc), return empty list
        print(f"Error reading users: {e}")
        return []

# Helper function write_users()
def write_users(users):  # Write all users to the text file
   with open(DATA_FILE, 'w') as f:              # Open the file in write mode
        for user in users:
            f.write(json.dumps(user) + '\n') # Convert user dictionary to JSON string and write it with a newline


# Helper fucntion get_next_id()
def get_next_id(users):                         # Generates the next available user ID
    if not users:                               # If there are no users, return 1
        return 1
    return max(user['id'] for user in users) + 1  # Find the last currrent ID and add 1


# API Endpoints

@router.post("/", response_model=User)

def create_user(user: UserCreate):
    users = read_users()                      # Reads all existing users from the file
    for existing_user in users:               # Cheack if the email already exists in the system
        if existing_user ['email'] == user.email:
            raise HTTPException(status_code = 400, detail = "Email is already registered.")
    new_id = get_next_id(users)               # Generates new ID
    new_user = {"id": new_id, "name": user.name, "email": user.email}       # COnverts the Pydantic model to a dictionary
   # Add to list and save 
    users.append(new_user)
    write_users(users)
    return new_user                         # Return the created user
                                  
@router.get("/", response_model = list[User])
def get_all_users():                        # Simply reads all users from file and returns them
    return read_users()

@router.get("/search", response_model = list[User])
def search_users(q: str = None):            # URL:  /users/search?q=searchterm
    if not q:                               # If no search query provided return empty list
        return[]
    
    users = read_users()                

    results = [                             # Filters users whose name contain the search term
        user for user in users
        if q.lower() in user['name'].lower()    # Convert term and user name to lowercase for comparison
    ]
    return results

@router.get("/{user_id}", response_model = User)
def get_user(user_id: int):                     # Get a specific user by ID
    users = read_users()

    for user in users:                          # Search for user with matching ID
        if user['id'] == user_id:
            return user                         # Found the user, return it
        
    raise HTTPException(status_code = 404, detail = "User not found")   # If no user found, raise 404 error


@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user_update: UserCreate):                 # Update an existing user
    
    users = read_users()
    for i, user in enumerate(users):                                    # Find the user to find the one to update
        if user['id'] == user_id:
            if user['email'] != user_update.email:                      # If email is being changed
                # Check if new email is already used by another user
                for other_user in users:
                    if other_user['email'] == user_update.email and other_user['id'] != user_id:
                        raise HTTPException(status_code = 400, detail = "Email is already registed on another account.")
            users[i] = {"id": user_id, "name": user_update.name, "email": user_update.email}    #Updates the user data, but keeps ID same
            write_users(users)
            return users[i]
    raise HTTPException(status_code=404, detail = "User not found.")    # If case the user was not found

@router.delete("/{user_id}")
def delete_user(user_id: int):                                          # Delete a user
    users = read_users()
    # Create new list excluding the user to delete; list keeps all users where ID doesn't match
    new_users = [user for user in users if user['id'] != user_id]

    if len(new_users) == len(users):
        raise HTTPException(status_code = 404, detail = "User not found.")
    
    write_users(new_users)
    return {"message": f"User {user_id} deleted successfully"}

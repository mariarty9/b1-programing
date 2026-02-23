Week 15 Upgrading to SQLite Database

What I did
    - Convert from file-based storage to SQLite database
    - Implement UserStore with SQLite methods
    - Test all CRUD operations
    - Implement basic frontend that displays the list of users at http://127.0.0.1:8002/static/


Database Info
    - 'users.db'
    - Table 'users' with id(autoincrement), name, email
    - IDs start from 2 because I tested DELETE operation. According to my research it's better to leave it that way because: old references to ID 1 can point to wrong data; audit logs can be confusing, foreign key relationships can break

Endpoints Tested
    - Post /users - Create User
    - GET /users - Get all users
    - GET /users/{id}   - Get user by ID
    - GET /users/search - Search users
    - PUT /users/{id}   - Update user
    - DELETE /users/{id} - Delete user    

Problem I've encountered
    - Email uniqueness error when updating the user's info. Fixed it by modifying SQL query to exclude current user

Week15/
├── main.py                 # Updated for Week 15
├── schema.py               # Pydantic models reamins unchanged
├── user_store.py           # SQLite version COMPLETELY REWRITTEN
├── routes/
│   ├── __init__.py         
│   └── users.py  
├── static/
│   └── index.html          # Basic frontend with list of users        
├── users.db                # SQLite database that was created automatically
└── README.md   
Week 14 Building Your UserStore Class
What changed:
    - New file 'user_store.py'
        1. Created a 'UserStore' class that handles all file operations
        2. Contains methods 'load()', 'save()', 'find_by_id()', 'get_next_id()', 'create_user()', 'update_user()', 'delete_user()'

    - Refactored in routes/users.py
        1. Removed: all helper functions ('read_users', 'write_users', 'get_next_id')
        2. Removed: all file operartion logic from endpoints
        3. Added: import 'UserStore' class
        4. Changed: each endpoint now just calls store method
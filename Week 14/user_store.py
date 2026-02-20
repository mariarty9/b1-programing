import json
import os

class UserStore:
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):                         # Returns list of user dictionaries, or empty list if file doesn't exist
        if not os.path.exists(self.file_path):
            print(f"File {self.file_path} does not exist yet, returning empty list")
            return []
        
        users = []                          # Empty list to store users
        try:
            with open(self.file_path, 'r') as f:
                for line in f:
                    if line.strip():
                        users.append(json.loads(line))
            print (f"Loaded {len(users)} users from file")
            return users
        except Exception as e:
            print (f"Error loading users: {e}")
            return []
        
    # Replaces the write_users() function from week 13
    def save(self, users):                  # Writes users as JSON lines
        try:
            with open(self.file_path, 'w') as f:
                for user in users:
                    f.write(json.dumps(user) + '\n')
            print (f"Saved {len(users)} users to file")
            return True                     # If successful
        except Exception as e:
            print (f"Error saving users: {e}")
            return False
        
        
    def find_by_id(self, user_id):          # Returns user dict or None
        users = self.load()                 # Load all users by calling another method of the same class

        # Search for user with matching ID
        for user in users:
            if user['id'] == user_id:
                print (f"Found user with ID {user_id}")
                return user                 # If found
        print (f"User with ID {user_id} not found" )
        return None                         # If not found
    

    def get_next_id(self):                  # Replacing the function from week 13 with same logic, but a class method
        users = self.load()
        if not users:                       # If no users found, start with 1
            return 1
        
        return max(user['id'] for user in users) + 1    # Find usr with maximum Id and add 1; same logic as week 13
    
    def create_user(self, user_data):       # In week 13 this logic was in the POST endpoint
        users = self.load()
        # Check if email already exists
        for user in users:
            if user['email'] == user_data['email']:
                print (f"Email {user_data['email']} already exists")
                return None                     # Email exist, so we can't create new user
            
        new_id = self.get_next_id()             # Generate new ID
        new_user = {"id": new_id, **user_data}  # Create new user dictionary; the **user_data unpacks the dictionary
        users.append(new_user)
        self.save(users)  

        print (f"Create new user: {new_user}")
        return new_user
    
    def update_user(self, user_id, user_data):  # In week 13 this logic was in the PUT endpoint
        users = self.load()
        for i, user in enumerate(users):
            if user['id'] == user_id:
                if user['email'] != user_data['email']:     # Check email uniqueness if changing
                    for other_user in users:
                        if other_user['email'] == user_data['email'] and other_user['id'] != user_id:
                            print (f"Email {user_data['email']} already in use by another user")
                            return None
                users[i] = {"id": user_id, **user_data}
                self.save(users)
                print (f"Updated user with ID {user_id}")
                return users[i]                             # Return updated user
        
        print (f"User with ID {user_id} not found for update")
        return None
    
    def delete_user(self, user_id):
        users = self.load()
        new_users = [user for user in users if user['id'] != user_id]       # Create new list without the user to delete

        if len(new_users) == len(users):
            print (f"User with ID {user_id} not found for deletion")
            return False                                                    # Since user is not found
        
        self.save(new_users)                                                # Save the filtered list
        print (f"Deleted user with ID {user_id}")
        return True                                                         # Successful deletion
    
        
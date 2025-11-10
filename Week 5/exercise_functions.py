import string

#Individual Validation Functions

def check_min_length(password, min_len=8):
    return len(password) >= min_len

def has_uppercase(password):
   return any(char in string.ascii_uppercase for char in password)

def has_lowercase(password):
   return any(char in string.ascii_lowercase for char in password)

def has_digit(password):
   return any(char in string.digits for char in password)

def has_special_char(password):
   return any(char in string.punctuation for char in password)

#Master Validation Function

def validate_password(password):
    results = {
        'min_length': check_min_length(password),
        'has_uppercase': has_uppercase(password),
        'has_lowercase': has_lowercase(password),
        'has_digit': has_digit(password),
        'has_special': has_special_char(password)
    }
    results['is_valid'] = all(results.values())
    return results

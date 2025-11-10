#Generate strong password
import string
import random

def generate_strong_password(length = 12):
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special = string.punctuation

    password_chars = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(special)
    ]

    all_chars = lowercase + uppercase + digits + special
    password_chars += [random.choice(all_chars) for _ in range(length - 4)]

#Random shuffle
    random.shuffle(password_chars)
    return ''.join(password_chars)
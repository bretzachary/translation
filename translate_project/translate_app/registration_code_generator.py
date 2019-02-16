import string
import random

def generate(size=32, chars=string.ascii_letters + string.digits):
  return ''.join(random.choice(chars) for n in range(size))
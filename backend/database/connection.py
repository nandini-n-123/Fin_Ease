# database/connection.py
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv() # This line is fine here, though main.py also loads it.

# This file now primarily serves for organization.
# The actual client object is instantiated in main.py, and the db object
# is retrieved via the get_db_instance dependency in the routers.

# Do NOT instantiate client or db here directly anymore.
# The 'client' variable used in main.py will be a global variable.
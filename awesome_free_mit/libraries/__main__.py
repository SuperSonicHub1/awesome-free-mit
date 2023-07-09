from . import MITLibraries
from requests import Session

print(MITLibraries(Session()).markdown())

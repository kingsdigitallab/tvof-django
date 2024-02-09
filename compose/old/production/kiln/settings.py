import json
from os import getenv
LINKS = json.loads(getenv('KILN_DOWNLOAD_LINKS', '[]'))

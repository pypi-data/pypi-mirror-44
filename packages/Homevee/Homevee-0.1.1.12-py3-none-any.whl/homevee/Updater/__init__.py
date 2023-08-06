import json
import urllib

import pip
from packaging import version

from homevee import constants


def get_homevee_update_version():
    installed_version = constants.HOMEVEE_VERSION_NUMBER

    newest_version = get_newest_version()

    if(newest_version is None):
        return False

    if(version.parse(newest_version) > version.parse(installed_version)):
        return newest_version
    else:
        return None

def get_newest_version():
    url = "https://pypi.org/pypi/Homevee/json"

    try:
        response = urllib.request.urlopen(url).read()
        response = response.decode('utf-8')
        response_json = json.loads(response)
        version = response_json['info']['version']

        return version
    except:
        return None

'''
Updates the Homevee PIP-Package
Returns true if update was successful,
returns false if there was an error
'''
def do_homevee_update():
    try:
        pip.main(["install", "--upgrade", "Homevee"])
    except:
        return False

    #Send notification to admin

    #Reboot the system after the update
    os.system('reboot')
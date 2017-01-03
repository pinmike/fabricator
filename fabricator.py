# Python script to gifiti your github timeline

# imports
import requests
import json
import subprocess
import os

import config
owner = config.owner
repo = config.repo

token = "token " + config.token
tokenHeader = {'Authorization': token}
repoUrl = 'https://api.github.com/repos/' + owner + '/' + repo

# Check the token is still valid
checkTokenResult = requests.get('https://api.github.com/user', headers=tokenHeader)
if checkTokenResult.status_code!=requests.codes.ok:
	print("Auth token is not valid")
	quit()
else:
	print("Token valid")

# Then try to delete the repo in case it already exists
deleteResult = requests.delete(repoUrl, headers=tokenHeader)
if deleteResult.status_code==requests.codes.no_content:
	print("Existing repo deleted from github")
else:
	print("No previous repo found to delete")

# Then create the repo afresh
createPayload = {'name': repo, 'private': "true"}
createResult = requests.post('https://api.github.com/user/repos', data=json.dumps(createPayload), headers=tokenHeader)
if createResult.status_code!=requests.codes.created:
	print("Failed to create the repo")
	quit()
else:
	print("New repo created")

# Delete the last local .sh file if one exists
if os.path.isfile('gitfiti.sh'):
	os.remove("gitfiti.sh")
	print("Old bash script file removed")

# Then run the script to create the bash script to fake github commits
subprocess.call(['python', 'gitfiti.py'])
print("New bash script file created")

# Then run the script to post the commits to github
subprocess.call('gitfiti.sh', shell=True)

# Then finally patch the repo to make it public
#patchPayload = {'private': "false"}
#patchResult = requests.patch(repoUrl, data=json.dumps(patchPayload), headers=tokenHeader)
#if patchResult.status_code!=requests.codes.ok:
#	print("Failed to set the repo to public")
#	quit()
#else:
#	print("New repo set to public")

print("Process complete!")

quit()
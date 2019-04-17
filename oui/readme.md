OUI Finder
------
Another script created before using AWX, again, if made today I would build it from scratch in AWX. 

This one takes input from HTML page of OUI, passes MAC OUI and Ansible Host Group to python script which:
1) verifies it's a vendor registered MAC using a REST API provided online
2) Executes an ansible play against host group defined in the HTML page (IT MUST EXIST INSIDE /ETC/ANSIBLE/HOSTS or whatever your default inventory is!)
3) return ansible results in iframe

Show Command
This play allows me to run show commands on a statically defined set of switches in my environment.

Requirements: the hostnames defined in the combobox list must be contained in /etc/hosts to pass sanity check.

This play is from back before I started using AWX.  Should I have made it now, it would have been totally done through AWX but this is a combination of an html webpage which loads values into a python script which then sends a system call to the ansible play, with the result being contained with an iframe on the original html page.

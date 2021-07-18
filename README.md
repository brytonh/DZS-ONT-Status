# DZS-ONT-Status
I wrote this script to limit the number of back-office network ops tickets for something as trivial as troubleshooting light level, bridge/mac tables for connected devices on ONT ports, leased IP addresses or delegated IPv6 prefixes, etc. 

</br>
**zhone-status-webapp** folder contains the files needed for running a basic web form to take in ONT MAC and spit out troubleshooting information. 

**templates folder:** </br>
form.html - the initial web form, input MAC address and submit button </br>
results.html - only used for an error case where the ONT is not found via MAC on any OLT </br>
results_template.html - the verbose output of ONT status / troubleshooting commands </br>

**screenshots folder:** </br>
example-case.png - a successful find of an ONT, and the status output for this ONT that would be seen in the webpage after the POST call from web form
error-case.png - an example of an ONT not being found on any OLT, you'd see this err message in the webpage after POST

the zhone-status.py file can be run without the flask webapp, the OLT's searched are still indexed in the python list within the code 

*FYI this script currently uses telnet to interact with the OLT devices for these calls* 
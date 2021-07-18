# DZS-ONT-Status
Get status information from DZS OLT about specific ONT, feed in as input the MAC address of ONT

zhone-status-webapp contains the files needed for running a basic web form to take in ONT MAC and spit out troubleshooting information. 

templates:
form.html - the initial web form, input MAC address and submit button 
results.html - only used for an error case where the ONT is not found via MAC on any OLT 
results_template.html - the verbose output of ONT status / troubleshooting commands 
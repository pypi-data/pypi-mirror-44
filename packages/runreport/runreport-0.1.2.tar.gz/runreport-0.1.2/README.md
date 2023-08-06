# runreport:  send contents of executing code to instructor's CGI 

Usage:
```
import runreport
runreport.name = 'Joe Wilson'
```

`runreport` attempts to send the contents of the Python file being executed to a CGI script run and maintained by the instructor.  

Upon execution, `runreport` reads sys.argv[0] to find the name/location of the script being executed; it reads the file into a string and sends it to a CGI script so it can be recorded and reviewed by the instructor.  



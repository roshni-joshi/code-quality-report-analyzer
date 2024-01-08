1. Download eclipse enterprise version.
2. Import project in eclipse by following below steps :
	File -> Import -> Existing maven project -> select your project
3. Once import is fully completed, right click 'CodeQualityAnalyzerBackendApplication' class present in  src/main/java folder and click 'run as' -> java application to run the application.
4. Once application is up, rest services can be accessed on localhost. 

Test cases will be present in src/test/java folder.
To execute unit test cases:
	Right click on test class -> Run as -> Junit Test

Application properties will be present in .properties files in src/main/resources folder.

If dependencies are not installed properly, right click the project folder and click 'run as' -> 'maven install'.
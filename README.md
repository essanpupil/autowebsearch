# ScamSearcher
ScamSearcher is an application with the goal to search for scam website. In this early stage, the target is web scam using Indonesian language.

I divide this project into several application and package:
1. search_extractor, python package to extract link from search engine. Currently it only support search queried to google.  
2. website_management, django app to store website url, edit website property, & extract link from the webpage.  
3. website_analyzer, python package to analize website. The main objective is to determine if the websites are scam or not. The decision is made based-on certain rules.  
4. operation, django app that give interface to control all the above package & apps.   
5. administrative, django app to manage user that can operate this project. And also manage client that uses this project to protect their interest.  

# Knowledge-Quiz
Python Desktop GUI Application  
  
Proiect realizat de:  
*Lupu Mihai - Razvan  
*State Corina  
*Munteanu Ionela  
*Sin Andrei  
  
Link Trello (Backlog + User Stories + Organizare): https://trello.com/b/khRKXneB/knowledge-quiz  
  
User stories: UPLOADED  

  
Code Refactoring: UPLOADED   
  
Diagrama UML: UPLOADED  
  
Bug Reporting:  
Pe parcursul proiectului nu am intalnit bug-uri numeroase, dar printre cele mai importante se regasesc:  

-Datorita functiei after(), prin intermediul careia puteam edita widgeturile Tkinter, utilizatorul avea sansa sa mai apese de cateva ori
butoanele care reprezentau raspunsuri corecte, astfel oferindu-i-se un avantaj nedrept. Bug-ul a fost rezolvat prin modificarea starii
butoanelor in DISABLED.

-OperationalError: database is locked,
SQLite is meant to be a lightweight database, and thus can't support a high level of concurrency. OperationalError: database is locked 
errors indicate that your application is experiencing more concurrency than sqlite can handle in default configuration. This error means 
that one thread or process has an exclusive lock on the database connection and another thread timed out waiting for the lock the be released.
Solutie: Am rescris codul pentru ca baza de date sa faca tranzactii cat mai scurte.  
  
Link prezentare(demo): https://youtu.be/AEIfbUIWM5k

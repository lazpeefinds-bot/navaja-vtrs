** Tech stack: python flask, sqlite with sqlalchemy, tailwindv4, jinja2. **
(The file structure are these:
    instance/election.db
    models/
    templates/
    app.py
    electiom.sql
)



Develop a Election system that implements the following specifications: 

BACKEND: (preloaded database: Election.sql)

Election database with the following tables each with its corresponding fields:
**Positions Table
    - posID (pk)
    - posName
    - numOfPositions
    - posStat (open/closed)

**Votes Table
    - posID (fk from Positions)
    - voterID (fk from Voters)
    - candID (fk from Candidates)

**Voters Table
    - voterID (pk)
    - voterPass
    - voterFName
    - voterMName
    - voterLName
    - voterStat (active/inactive)
    - voted (Y/N)

**Candidates Table
    - candID (PK)
    - candFName
    - candLName
    - posID (fk)
    - candStat (active/inactive)



FRONTED: 
modules:
    *Provide for a Positions Management UI that contains: 
        -Adding a position record [1]
        - Deactivating a position record [1]
        - Updating a postion record [1]
    
    *Provide for a Candidates Management UI that contains:
        - Adding a candidate record [1]
        - Deactivating a candidate record [1]
        - Updating a candidate record [1]
    
    *Provide for a Voting/Votation UI that lets the voter vote for a candidate in each position:  
        To be able to vote, the voter:
            - Must be active (HINT: voterStat)
            - Must login using his/her voterID and voterPass as the username and password, respectively, and
            - The number of voted candidate/s must be less than or equal to the number of vacant positions. (For example, the voter may vote up to 12 senators only.)
            - Must NOT be allowed to vote again (HINT: voted)

    *Provide for an Election Results UI that will display the total votes of the candidates per position and his/her voting percentage, to wit::
        (example table)
        President:         Total Votes             Voting %
        Candidate 1             125                 47.53
        Candidate 2             138                 52.47

        Vice President          
        Candidate 1             150                 ....    
        Candidate 2             120                 .....


    Provide for an Election Winners UI that will display the winner/s per position and his/her corresponding number of votes earned, in descending order for positions with more than 1 winner, to wit:
        (example table)
        Elective Position      Winner               Total Votes
        President               Candidate 1             125
        Vice President          Candidate 3             138
        senators                Candidate 40            142
        Senator                 Candidate 1             133
        
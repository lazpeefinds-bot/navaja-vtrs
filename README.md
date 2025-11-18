# Election System

A comprehensive web-based election management system built with Flask, SQLAlchemy, and Tailwind CSS.

## Features

### 1. Positions Management
- Add new election positions
- Update existing positions
- Deactivate positions
- Set number of available positions (e.g., 12 senators)

### 2. Candidates Management
- Add candidates for each position
- Update candidate information
- Deactivate candidates
- Associate candidates with positions

### 3. Voting System
- Secure voter login with voter ID and password
- Validation for active voters only
- Prevention of duplicate voting
- Limit votes per position based on available slots
- Support for single and multiple candidate selection

### 4. Election Results
- Real-time vote counting
- Percentage calculation for each candidate
- Visual representation with progress bars
- Sorted by vote count

### 5. Election Winners
- Display winners for each position
- Ranked display with medals (gold, silver, bronze)
- Shows total votes earned
- Descending order for multi-winner positions

### 6. Voters Management
- View all registered voters
- Check voter status (active/inactive)
- Track who has voted

## Tech Stack

- **Backend**: Python Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: Jinja2 Templates
- **Styling**: Tailwind CSS v4
- **Session Management**: Flask Sessions

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone or download the repository**
   ```bash
   cd Navaja-election
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database with sample data**
   ```bash
   sqlite3 instance/election.db < election.sql
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   Open your browser and navigate to: `http://127.0.0.1:5000`

## Database Schema

### Positions Table
- `posID` (Primary Key)
- `posName` (Position name)
- `numOfPositions` (Number of available positions)
- `posStat` (Status: open/closed)

### Voters Table
- `voterID` (Primary Key)
- `voterPass` (Password)
- `voterFName`, `voterMName`, `voterLName` (Name fields)
- `voterStat` (Status: active/inactive)
- `voted` (Y/N)

### Candidates Table
- `candID` (Primary Key)
- `candFName`, `candLName` (Name fields)
- `posID` (Foreign Key to Positions)
- `candStat` (Status: active/inactive)

### Votes Table
- `id` (Primary Key)
- `posID` (Foreign Key to Positions)
- `voterID` (Foreign Key to Voters)
- `candID` (Foreign Key to Candidates)

## Sample Login Credentials

Use any of these sample voter credentials to test the voting system:

- **Voter ID**: 2021-0001, **Password**: pass123
- **Voter ID**: 2021-0002, **Password**: pass123
- **Voter ID**: 2021-0003, **Password**: pass123

(See election.sql for more sample voters)

## Usage Guide

### For Administrators

1. **Manage Positions**: Navigate to "Positions" to add, edit, or deactivate election positions
2. **Manage Candidates**: Navigate to "Candidates" to add, edit, or deactivate candidates
3. **Monitor Results**: View real-time results in the "Results" section
4. **Check Winners**: See election winners in the "Winners" section

### For Voters

1. Click on "Vote" in the navigation menu
2. Enter your Voter ID and Password
3. Select your preferred candidates for each position
4. Review your selections
5. Submit your vote (this action cannot be undone)

## File Structure

```
Navaja-election/
├── instance/
│   └── election.db          # SQLite database
├── models/
│   └── __init__.py          # SQLAlchemy models
├── templates/
│   ├── base.html            # Base template
│   ├── index.html           # Home page
│   ├── positions.html       # Positions list
│   ├── add_position.html    # Add position form
│   ├── edit_position.html   # Edit position form
│   ├── candidates.html      # Candidates list
│   ├── add_candidate.html   # Add candidate form
│   ├── edit_candidate.html  # Edit candidate form
│   ├── login.html           # Voter login
│   ├── vote.html            # Voting interface
│   ├── results.html         # Election results
│   ├── winners.html         # Election winners
│   └── voters.html          # Voters list
├── app.py                   # Main Flask application
├── election.sql             # Database schema and sample data
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Security Notes

- Change the `SECRET_KEY` in `app.py` before deploying to production
- In production, use stronger password hashing (bcrypt, argon2)
- Consider adding CSRF protection for forms
- Implement rate limiting for login attempts
- Use HTTPS in production

## Future Enhancements

- Add voter registration functionality
- Implement password hashing
- Add email notifications
- Export results to PDF/Excel
- Add admin authentication
- Implement vote verification system
- Add support for multiple elections

## License

This project is created for educational purposes.

## Support

For issues or questions, please contact the development team.


in app.py: 
from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, Position, Voter, Candidate, Vote
from sqlalchemy import func
import os

app = Flask(_name_)
app.config['SECRET_KEY'] = 'navaja-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///election.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


# Initialize database
def init_db():
    with app.app_context():
        db.create_all()
        print("Database initialized!")


# Home route
@app.route('/')
def index():
    return render_template('index.html')

if _name_ == '_main_':
    # Initialize database
    with app.app_context():
        db.create_all()

    app.run(debug=True)
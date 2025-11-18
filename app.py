from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, Position, Voter, Candidate, Vote
from sqlalchemy import func
import os

app = Flask(__name__)
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


# ==================== POSITIONS MANAGEMENT ====================
@app.route('/positions')
def positions():
    all_positions = Position.query.all()
    return render_template('positions.html', positions=all_positions)


@app.route('/positions/add', methods=['GET', 'POST'])
def add_position():
    if request.method == 'POST':
        pos_name = request.form.get('posName')
        num_positions = request.form.get('numOfPositions')
        pos_stat = request.form.get('posStat', 'open')

        new_position = Position(
            posName=pos_name,
            numOfPositions=int(num_positions),
            posStat=pos_stat
        )
        db.session.add(new_position)
        db.session.commit()
        flash('Position added successfully!', 'success')
        return redirect(url_for('positions'))

    return render_template('add_position.html')


@app.route('/positions/edit/<int:pos_id>', methods=['GET', 'POST'])
def edit_position(pos_id):
    position = Position.query.get_or_404(pos_id)

    if request.method == 'POST':
        position.posName = request.form.get('posName')
        position.numOfPositions = int(request.form.get('numOfPositions'))
        position.posStat = request.form.get('posStat')
        db.session.commit()
        flash('Position updated successfully!', 'success')
        return redirect(url_for('positions'))

    return render_template('edit_position.html', position=position)


@app.route('/positions/deactivate/<int:pos_id>')
def deactivate_position(pos_id):
    position = Position.query.get_or_404(pos_id)
    position.posStat = 'closed'
    db.session.commit()
    flash('Position deactivated successfully!', 'success')
    return redirect(url_for('positions'))


# ==================== CANDIDATES MANAGEMENT ====================
@app.route('/candidates')
def candidates():
    all_candidates = Candidate.query.join(Position).all()
    return render_template('candidates.html', candidates=all_candidates)


@app.route('/candidates/add', methods=['GET', 'POST'])
def add_candidate():
    if request.method == 'POST':
        cand_fname = request.form.get('candFName')
        cand_lname = request.form.get('candLName')
        pos_id = request.form.get('posID')
        cand_stat = request.form.get('candStat', 'active')

        new_candidate = Candidate(
            candFName=cand_fname,
            candLName=cand_lname,
            posID=int(pos_id),
            candStat=cand_stat
        )
        db.session.add(new_candidate)
        db.session.commit()
        flash('Candidate added successfully!', 'success')
        return redirect(url_for('candidates'))

    positions = Position.query.filter_by(posStat='open').all()
    return render_template('add_candidate.html', positions=positions)


@app.route('/candidates/edit/<int:cand_id>', methods=['GET', 'POST'])
def edit_candidate(cand_id):
    candidate = Candidate.query.get_or_404(cand_id)

    if request.method == 'POST':
        candidate.candFName = request.form.get('candFName')
        candidate.candLName = request.form.get('candLName')
        candidate.posID = int(request.form.get('posID'))
        candidate.candStat = request.form.get('candStat')
        db.session.commit()
        flash('Candidate updated successfully!', 'success')
        return redirect(url_for('candidates'))

    positions = Position.query.all()
    return render_template('edit_candidate.html', candidate=candidate, positions=positions)


@app.route('/candidates/deactivate/<int:cand_id>')
def deactivate_candidate(cand_id):
    candidate = Candidate.query.get_or_404(cand_id)
    candidate.candStat = 'inactive'
    db.session.commit()
    flash('Candidate deactivated successfully!', 'success')
    return redirect(url_for('candidates'))


# ==================== VOTER LOGIN AND VOTING ====================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        voter_id = request.form.get('voterID')
        voter_pass = request.form.get('voterPass')

        voter = Voter.query.filter_by(voterID=voter_id).first()

        if voter and voter.voterPass == voter_pass:
            if voter.voterStat == 'inactive':
                flash('Your account is inactive. Please contact the administrator.', 'error')
                return redirect(url_for('login'))

            if voter.voted == 'Y':
                flash('You have already voted!', 'error')
                return redirect(url_for('login'))

            session['voter_id'] = voter.voterID
            session['voter_name'] = f"{voter.voterFName} {voter.voterLName}"
            return redirect(url_for('vote'))
        else:
            flash('Invalid credentials!', 'error')

    return render_template('login.html')


@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if 'voter_id' not in session:
        flash('Please login first!', 'error')
        return redirect(url_for('login'))

    voter = Voter.query.filter_by(voterID=session['voter_id']).first()

    if voter.voted == 'Y':
        flash('You have already voted!', 'error')
        return redirect(url_for('logout'))

    if request.method == 'POST':
        # Get all positions
        positions = Position.query.filter_by(posStat='open').all()

        # Validate and process votes
        for position in positions:
            selected_candidates = request.form.getlist(f'position_{position.posID}')

            # Check if number of votes doesn't exceed allowed positions
            if len(selected_candidates) > position.numOfPositions:
                flash(f'You can only vote for {position.numOfPositions} candidate(s) for {position.posName}!', 'error')
                return redirect(url_for('vote'))

            # Save votes
            for cand_id in selected_candidates:
                new_vote = Vote(
                    posID=position.posID,
                    voterID=session['voter_id'],
                    candID=int(cand_id)
                )
                db.session.add(new_vote)

        # Mark voter as voted
        voter.voted = 'Y'
        db.session.commit()

        flash('Your vote has been recorded successfully!', 'success')
        return redirect(url_for('logout'))

    # Get positions and candidates for voting
    positions = Position.query.filter_by(posStat='open').all()
    positions_with_candidates = []

    for position in positions:
        candidates = Candidate.query.filter_by(posID=position.posID, candStat='active').all()
        positions_with_candidates.append({
            'position': position,
            'candidates': candidates
        })

    return render_template('vote.html', positions_data=positions_with_candidates, voter_name=session.get('voter_name'))


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully!', 'success')
    return redirect(url_for('index'))


# ==================== ELECTION RESULTS ====================
@app.route('/results')
def results():
    positions = Position.query.all()
    results_data = []

    for position in positions:
        # Get vote counts for each candidate in this position
        candidates = Candidate.query.filter_by(posID=position.posID).all()
        candidate_votes = []

        total_votes_for_position = Vote.query.filter_by(posID=position.posID).count()

        for candidate in candidates:
            vote_count = Vote.query.filter_by(candID=candidate.candID).count()
            percentage = (vote_count / total_votes_for_position * 100) if total_votes_for_position > 0 else 0

            candidate_votes.append({
                'candidate': candidate,
                'votes': vote_count,
                'percentage': round(percentage, 2)
            })

        # Sort by votes descending
        candidate_votes.sort(key=lambda x: x['votes'], reverse=True)

        results_data.append({
            'position': position,
            'candidate_votes': candidate_votes
        })

    return render_template('results.html', results_data=results_data)


# ==================== ELECTION WINNERS ====================
@app.route('/winners')
def winners():
    positions = Position.query.all()
    winners_data = []

    for position in positions:
        # Get vote counts for each candidate in this position
        candidates = Candidate.query.filter_by(posID=position.posID).all()
        candidate_votes = []

        for candidate in candidates:
            vote_count = Vote.query.filter_by(candID=candidate.candID).count()
            candidate_votes.append({
                'candidate': candidate,
                'votes': vote_count
            })

        # Sort by votes descending
        candidate_votes.sort(key=lambda x: x['votes'], reverse=True)

        # Get top N winners based on numOfPositions
        top_winners = candidate_votes[:position.numOfPositions]

        # Only include if there are votes
        if top_winners and top_winners[0]['votes'] > 0:
            winners_data.append({
                'position': position,
                'winners': top_winners
            })

    return render_template('winners.html', winners_data=winners_data)


# ==================== VOTERS MANAGEMENT (BONUS) ====================
@app.route('/voters')
def voters():
    all_voters = Voter.query.all()
    return render_template('voters.html', voters=all_voters)


if __name__ == '__main__':
    # Create instance directory if it doesn't exist
    os.makedirs('instance', exist_ok=True)

    # Initialize database
    with app.app_context():
        db.create_all()

    app.run(debug=True)

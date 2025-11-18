# Flask Routes Study Guide - Programming Skilltest

## Table of Contents
1. [CRUD Operations](#crud-operations)
2. [Count Operations](#count-operations)
3. [Search & Filter Operations](#search--filter-operations)
4. [Join Operations](#join-operations)
5. [Authentication & Session](#authentication--session)
6. [Aggregation & Statistics](#aggregation--statistics)
7. [Status Management](#status-management)
8. [API Routes (JSON Response)](#api-routes-json-response)

---

## CRUD Operations

### CREATE (Add New Record)

```python
# Basic Create - Single Record
@app.route('/positions/add', methods=['GET', 'POST'])
def add_position():
    if request.method == 'POST':
        # Get data from form
        pos_name = request.form.get('posName')
        num_positions = request.form.get('numOfPositions')
        pos_stat = request.form.get('posStat', 'open')  # default value

        # Create new object
        new_position = Position(
            posName=pos_name,
            numOfPositions=int(num_positions),
            posStat=pos_stat
        )

        # Add to database
        db.session.add(new_position)
        db.session.commit()

        flash('Position added successfully!', 'success')
        return redirect(url_for('positions'))

    return render_template('add_position.html')


# Create with Validation
@app.route('/candidates/add', methods=['GET', 'POST'])
def add_candidate():
    if request.method == 'POST':
        cand_fname = request.form.get('candFName')
        cand_lname = request.form.get('candLName')
        pos_id = request.form.get('posID')

        # Validation
        if not cand_fname or not cand_lname:
            flash('First name and last name are required!', 'error')
            return redirect(url_for('add_candidate'))

        new_candidate = Candidate(
            candFName=cand_fname,
            candLName=cand_lname,
            posID=int(pos_id),
            candStat='active'
        )

        db.session.add(new_candidate)
        db.session.commit()
        flash('Candidate added successfully!', 'success')
        return redirect(url_for('candidates'))

    # Get related data for dropdown
    positions = Position.query.filter_by(posStat='open').all()
    return render_template('add_candidate.html', positions=positions)


# Bulk Create
@app.route('/votes/submit', methods=['POST'])
def submit_votes():
    positions = Position.query.filter_by(posStat='open').all()

    for position in positions:
        selected_candidates = request.form.getlist(f'position_{position.posID}')

        # Save multiple votes
        for cand_id in selected_candidates:
            new_vote = Vote(
                posID=position.posID,
                voterID=session['voter_id'],
                candID=int(cand_id)
            )
            db.session.add(new_vote)

    db.session.commit()
    flash('Votes submitted successfully!', 'success')
    return redirect(url_for('results'))
```

---

### READ (Retrieve Records)

```python
# Read All Records
@app.route('/positions')
def positions():
    all_positions = Position.query.all()
    return render_template('positions.html', positions=all_positions)


# Read Single Record by ID
@app.route('/positions/<int:pos_id>')
def view_position(pos_id):
    position = Position.query.get_or_404(pos_id)
    return render_template('view_position.html', position=position)


# Read with Filter
@app.route('/positions/active')
def active_positions():
    active_positions = Position.query.filter_by(posStat='open').all()
    return render_template('positions.html', positions=active_positions)


# Read with Multiple Filters
@app.route('/candidates/filter')
def filter_candidates():
    status = request.args.get('status', 'active')
    position_id = request.args.get('position_id')

    query = Candidate.query

    if status:
        query = query.filter_by(candStat=status)

    if position_id:
        query = query.filter_by(posID=int(position_id))

    candidates = query.all()
    return render_template('candidates.html', candidates=candidates)


# Read with Pagination
@app.route('/voters/page/<int:page>')
def voters_paginated(page):
    per_page = 10
    voters = Voter.query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template('voters.html', voters=voters)


# Read with Ordering
@app.route('/candidates/sorted')
def sorted_candidates():
    # Order by last name ascending
    candidates = Candidate.query.order_by(Candidate.candLName.asc()).all()

    # Order by multiple columns
    # candidates = Candidate.query.order_by(
    #     Candidate.posID.asc(),
    #     Candidate.candLName.asc()
    # ).all()

    return render_template('candidates.html', candidates=candidates)
```

---

### UPDATE (Modify Records)

```python
# Basic Update
@app.route('/positions/edit/<int:pos_id>', methods=['GET', 'POST'])
def edit_position(pos_id):
    position = Position.query.get_or_404(pos_id)

    if request.method == 'POST':
        # Update fields
        position.posName = request.form.get('posName')
        position.numOfPositions = int(request.form.get('numOfPositions'))
        position.posStat = request.form.get('posStat')

        # Commit changes
        db.session.commit()
        flash('Position updated successfully!', 'success')
        return redirect(url_for('positions'))

    return render_template('edit_position.html', position=position)


# Partial Update (Status Only)
@app.route('/positions/deactivate/<int:pos_id>')
def deactivate_position(pos_id):
    position = Position.query.get_or_404(pos_id)
    position.posStat = 'closed'
    db.session.commit()
    flash('Position deactivated successfully!', 'success')
    return redirect(url_for('positions'))


# Update with Validation
@app.route('/candidates/edit/<int:cand_id>', methods=['GET', 'POST'])
def edit_candidate(cand_id):
    candidate = Candidate.query.get_or_404(cand_id)

    if request.method == 'POST':
        first_name = request.form.get('candFName')
        last_name = request.form.get('candLName')

        # Validation
        if not first_name or not last_name:
            flash('Name fields cannot be empty!', 'error')
            return redirect(url_for('edit_candidate', cand_id=cand_id))

        candidate.candFName = first_name
        candidate.candLName = last_name
        candidate.posID = int(request.form.get('posID'))
        candidate.candStat = request.form.get('candStat')

        db.session.commit()
        flash('Candidate updated successfully!', 'success')
        return redirect(url_for('candidates'))

    positions = Position.query.all()
    return render_template('edit_candidate.html', candidate=candidate, positions=positions)


# Bulk Update
@app.route('/voters/mark-voted', methods=['POST'])
def mark_all_voted():
    voter_ids = request.form.getlist('voter_ids')

    Voter.query.filter(Voter.voterID.in_(voter_ids)).update(
        {Voter.voted: 'Y'},
        synchronize_session=False
    )

    db.session.commit()
    flash(f'{len(voter_ids)} voters marked as voted!', 'success')
    return redirect(url_for('voters'))
```

---

### DELETE (Remove Records)

```python
# Soft Delete (Status Change)
@app.route('/candidates/deactivate/<int:cand_id>')
def deactivate_candidate(cand_id):
    candidate = Candidate.query.get_or_404(cand_id)
    candidate.candStat = 'inactive'
    db.session.commit()
    flash('Candidate deactivated successfully!', 'success')
    return redirect(url_for('candidates'))


# Hard Delete (Permanent)
@app.route('/positions/delete/<int:pos_id>', methods=['POST'])
def delete_position(pos_id):
    position = Position.query.get_or_404(pos_id)

    # Check if position has candidates
    candidate_count = Candidate.query.filter_by(posID=pos_id).count()
    if candidate_count > 0:
        flash('Cannot delete position with existing candidates!', 'error')
        return redirect(url_for('positions'))

    db.session.delete(position)
    db.session.commit()
    flash('Position deleted successfully!', 'success')
    return redirect(url_for('positions'))


# Delete with Cascade (Delete related records)
@app.route('/positions/delete-cascade/<int:pos_id>', methods=['POST'])
def delete_position_cascade(pos_id):
    position = Position.query.get_or_404(pos_id)

    # Delete related candidates first
    Candidate.query.filter_by(posID=pos_id).delete()

    # Delete related votes
    Vote.query.filter_by(posID=pos_id).delete()

    # Delete position
    db.session.delete(position)
    db.session.commit()

    flash('Position and related records deleted successfully!', 'success')
    return redirect(url_for('positions'))


# Bulk Delete
@app.route('/candidates/delete-multiple', methods=['POST'])
def delete_multiple_candidates():
    candidate_ids = request.form.getlist('candidate_ids')

    if not candidate_ids:
        flash('No candidates selected!', 'error')
        return redirect(url_for('candidates'))

    Candidate.query.filter(Candidate.candID.in_(candidate_ids)).delete(
        synchronize_session=False
    )

    db.session.commit()
    flash(f'{len(candidate_ids)} candidates deleted!', 'success')
    return redirect(url_for('candidates'))
```

---

## Count Operations

```python
# Basic Count
@app.route('/dashboard')
def dashboard():
    total_positions = Position.query.count()
    total_candidates = Candidate.query.count()
    total_voters = Voter.query.count()
    total_votes = Vote.query.count()

    return render_template('dashboard.html',
                         positions_count=total_positions,
                         candidates_count=total_candidates,
                         voters_count=total_voters,
                         votes_count=total_votes)


# Count with Filter
@app.route('/stats/positions')
def position_stats():
    open_positions = Position.query.filter_by(posStat='open').count()
    closed_positions = Position.query.filter_by(posStat='closed').count()

    return render_template('position_stats.html',
                         open=open_positions,
                         closed=closed_positions)


# Count by Group
@app.route('/stats/candidates-by-position')
def candidates_by_position():
    from sqlalchemy import func

    # Count candidates grouped by position
    stats = db.session.query(
        Position.posName,
        func.count(Candidate.candID).label('candidate_count')
    ).join(Candidate).group_by(Position.posID).all()

    return render_template('candidate_stats.html', stats=stats)


# Count with Join
@app.route('/stats/votes-per-candidate')
def votes_per_candidate():
    from sqlalchemy import func

    vote_counts = db.session.query(
        Candidate.candFName,
        Candidate.candLName,
        func.count(Vote.id).label('vote_count')
    ).join(Vote, Candidate.candID == Vote.candID)\
     .group_by(Candidate.candID)\
     .order_by(func.count(Vote.id).desc())\
     .all()

    return render_template('vote_counts.html', counts=vote_counts)


# Count Distinct
@app.route('/stats/unique-voters')
def unique_voters_who_voted():
    from sqlalchemy import func, distinct

    unique_voter_count = db.session.query(
        func.count(distinct(Vote.voterID))
    ).scalar()

    return render_template('voter_participation.html',
                         unique_voters=unique_voter_count)


# Conditional Count
@app.route('/stats/voter-participation')
def voter_participation():
    total_voters = Voter.query.count()
    voted_voters = Voter.query.filter_by(voted='Y').count()
    not_voted = total_voters - voted_voters
    percentage = (voted_voters / total_voters * 100) if total_voters > 0 else 0

    return render_template('participation.html',
                         total=total_voters,
                         voted=voted_voters,
                         not_voted=not_voted,
                         percentage=round(percentage, 2))
```

---

## Search & Filter Operations

```python
# Simple Search (Single Field)
@app.route('/candidates/search')
def search_candidates():
    search_query = request.args.get('q', '')

    if search_query:
        candidates = Candidate.query.filter(
            Candidate.candLName.ilike(f'%{search_query}%')
        ).all()
    else:
        candidates = Candidate.query.all()

    return render_template('candidates.html',
                         candidates=candidates,
                         search_query=search_query)


# Multi-Field Search
@app.route('/voters/search')
def search_voters():
    search_query = request.args.get('q', '')

    if search_query:
        voters = Voter.query.filter(
            db.or_(
                Voter.voterFName.ilike(f'%{search_query}%'),
                Voter.voterLName.ilike(f'%{search_query}%'),
                Voter.voterID.ilike(f'%{search_query}%')
            )
        ).all()
    else:
        voters = Voter.query.all()

    return render_template('voters.html', voters=voters)


# Advanced Filter with Multiple Parameters
@app.route('/candidates/advanced-search')
def advanced_candidate_search():
    first_name = request.args.get('first_name', '')
    last_name = request.args.get('last_name', '')
    position_id = request.args.get('position_id')
    status = request.args.get('status')

    query = Candidate.query

    if first_name:
        query = query.filter(Candidate.candFName.ilike(f'%{first_name}%'))

    if last_name:
        query = query.filter(Candidate.candLName.ilike(f'%{last_name}%'))

    if position_id:
        query = query.filter_by(posID=int(position_id))

    if status:
        query = query.filter_by(candStat=status)

    candidates = query.all()
    positions = Position.query.all()

    return render_template('advanced_search.html',
                         candidates=candidates,
                         positions=positions)


# Filter with Range
@app.route('/positions/filter-by-slots')
def filter_by_slots():
    min_slots = request.args.get('min', type=int, default=1)
    max_slots = request.args.get('max', type=int, default=20)

    positions = Position.query.filter(
        Position.numOfPositions.between(min_slots, max_slots)
    ).all()

    return render_template('positions.html', positions=positions)


# Filter with IN clause
@app.route('/candidates/by-positions')
def candidates_by_positions():
    position_ids = request.args.getlist('pos_ids', type=int)

    if position_ids:
        candidates = Candidate.query.filter(
            Candidate.posID.in_(position_ids)
        ).all()
    else:
        candidates = Candidate.query.all()

    return render_template('candidates.html', candidates=candidates)


# Filter with NOT
@app.route('/voters/not-voted')
def voters_not_voted():
    voters = Voter.query.filter(
        Voter.voted != 'Y'
    ).all()

    return render_template('voters.html', voters=voters)


# Combined Filter and Search
@app.route('/candidates/filter-search')
def filter_and_search():
    search = request.args.get('search', '')
    status = request.args.get('status', 'active')
    position_id = request.args.get('position_id', type=int)

    query = Candidate.query

    # Apply status filter
    if status:
        query = query.filter_by(candStat=status)

    # Apply position filter
    if position_id:
        query = query.filter_by(posID=position_id)

    # Apply search
    if search:
        query = query.filter(
            db.or_(
                Candidate.candFName.ilike(f'%{search}%'),
                Candidate.candLName.ilike(f'%{search}%')
            )
        )

    candidates = query.all()
    return render_template('candidates.html', candidates=candidates)
```

---

## Join Operations

```python
# Simple Join
@app.route('/candidates/with-positions')
def candidates_with_positions():
    # Join candidates with positions
    candidates = Candidate.query.join(Position).all()
    # Access: candidate.position.posName
    return render_template('candidates.html', candidates=candidates)


# Left Join (Include candidates even without positions)
@app.route('/candidates/left-join')
def candidates_left_join():
    candidates = Candidate.query.outerjoin(Position).all()
    return render_template('candidates.html', candidates=candidates)


# Multiple Joins
@app.route('/votes/details')
def vote_details():
    votes = db.session.query(Vote, Candidate, Position, Voter)\
        .join(Candidate, Vote.candID == Candidate.candID)\
        .join(Position, Vote.posID == Position.posID)\
        .join(Voter, Vote.voterID == Voter.voterID)\
        .all()

    return render_template('vote_details.html', votes=votes)


# Join with Filter
@app.route('/positions/<int:pos_id>/candidates')
def position_candidates(pos_id):
    position = Position.query.get_or_404(pos_id)
    candidates = Candidate.query.filter_by(
        posID=pos_id,
        candStat='active'
    ).all()

    return render_template('position_candidates.html',
                         position=position,
                         candidates=candidates)


# Join with Aggregation
@app.route('/results/detailed')
def detailed_results():
    from sqlalchemy import func

    results = db.session.query(
        Position.posName,
        Candidate.candFName,
        Candidate.candLName,
        func.count(Vote.id).label('vote_count')
    ).select_from(Position)\
     .join(Candidate, Position.posID == Candidate.posID)\
     .outerjoin(Vote, Candidate.candID == Vote.candID)\
     .group_by(Position.posID, Candidate.candID)\
     .order_by(Position.posID, func.count(Vote.id).desc())\
     .all()

    return render_template('detailed_results.html', results=results)
```

---

## Authentication & Session

```python
# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        voter_id = request.form.get('voterID')
        voter_pass = request.form.get('voterPass')

        # Find user
        voter = Voter.query.filter_by(voterID=voter_id).first()

        # Validate credentials
        if voter and voter.voterPass == voter_pass:
            # Check account status
            if voter.voterStat == 'inactive':
                flash('Your account is inactive!', 'error')
                return redirect(url_for('login'))

            # Check if already voted
            if voter.voted == 'Y':
                flash('You have already voted!', 'error')
                return redirect(url_for('login'))

            # Set session variables
            session['voter_id'] = voter.voterID
            session['voter_name'] = f"{voter.voterFName} {voter.voterLName}"
            session['logged_in'] = True

            flash('Login successful!', 'success')
            return redirect(url_for('vote'))
        else:
            flash('Invalid credentials!', 'error')

    return render_template('login.html')


# Logout Route
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully!', 'success')
    return redirect(url_for('index'))


# Protected Route (Requires Login)
@app.route('/vote')
def vote():
    # Check if user is logged in
    if 'voter_id' not in session:
        flash('Please login first!', 'error')
        return redirect(url_for('login'))

    # Check if already voted
    voter = Voter.query.filter_by(voterID=session['voter_id']).first()
    if voter.voted == 'Y':
        flash('You have already voted!', 'error')
        return redirect(url_for('logout'))

    # Get voting data
    positions = Position.query.filter_by(posStat='open').all()
    return render_template('vote.html',
                         positions=positions,
                         voter_name=session.get('voter_name'))


# Session Check Decorator (Advanced)
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'voter_id' not in session:
            flash('Please login first!', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/protected')
@login_required
def protected_route():
    return render_template('protected.html')


# Admin Route with Role Check
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_role' not in session or session['user_role'] != 'admin':
            flash('Admin access required!', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    return render_template('admin_dashboard.html')
```

---

## Aggregation & Statistics

```python
# Sum Aggregation
@app.route('/stats/total-slots')
def total_available_slots():
    from sqlalchemy import func

    total_slots = db.session.query(
        func.sum(Position.numOfPositions)
    ).scalar()

    return render_template('stats.html', total_slots=total_slots)


# Average Calculation
@app.route('/stats/average-candidates')
def average_candidates_per_position():
    from sqlalchemy import func

    avg_candidates = db.session.query(
        func.avg(func.count(Candidate.candID))
    ).select_from(Position)\
     .outerjoin(Candidate, Position.posID == Candidate.posID)\
     .group_by(Position.posID)\
     .scalar()

    return render_template('stats.html',
                         avg_candidates=round(avg_candidates, 2))


# Min/Max Values
@app.route('/stats/position-range')
def position_slot_range():
    from sqlalchemy import func

    min_slots = db.session.query(func.min(Position.numOfPositions)).scalar()
    max_slots = db.session.query(func.max(Position.numOfPositions)).scalar()

    return render_template('stats.html',
                         min_slots=min_slots,
                         max_slots=max_slots)


# Group By with Having
@app.route('/stats/popular-positions')
def popular_positions():
    from sqlalchemy import func

    # Positions with more than 3 candidates
    popular = db.session.query(
        Position.posName,
        func.count(Candidate.candID).label('candidate_count')
    ).join(Candidate)\
     .group_by(Position.posID)\
     .having(func.count(Candidate.candID) > 3)\
     .all()

    return render_template('popular_positions.html', positions=popular)


# Percentage Calculation
@app.route('/results/percentage')
def vote_percentages():
    from sqlalchemy import func

    positions = Position.query.all()
    results_data = []

    for position in positions:
        total_votes = Vote.query.filter_by(posID=position.posID).count()

        candidates = db.session.query(
            Candidate.candFName,
            Candidate.candLName,
            func.count(Vote.id).label('votes')
        ).outerjoin(Vote, Candidate.candID == Vote.candID)\
         .filter(Candidate.posID == position.posID)\
         .group_by(Candidate.candID)\
         .all()

        candidate_data = []
        for cand in candidates:
            percentage = (cand.votes / total_votes * 100) if total_votes > 0 else 0
            candidate_data.append({
                'name': f"{cand.candFName} {cand.candLName}",
                'votes': cand.votes,
                'percentage': round(percentage, 2)
            })

        results_data.append({
            'position': position.posName,
            'candidates': candidate_data
        })

    return render_template('percentages.html', results=results_data)


# Ranking/Top N
@app.route('/winners/<int:pos_id>')
def position_winners(pos_id):
    from sqlalchemy import func

    position = Position.query.get_or_404(pos_id)

    # Get top N candidates based on numOfPositions
    winners = db.session.query(
        Candidate.candFName,
        Candidate.candLName,
        func.count(Vote.id).label('vote_count')
    ).join(Vote, Candidate.candID == Vote.candID)\
     .filter(Candidate.posID == pos_id)\
     .group_by(Candidate.candID)\
     .order_by(func.count(Vote.id).desc())\
     .limit(position.numOfPositions)\
     .all()

    return render_template('winners.html',
                         position=position,
                         winners=winners)
```

---

## Status Management

```python
# Toggle Status
@app.route('/positions/toggle-status/<int:pos_id>')
def toggle_position_status(pos_id):
    position = Position.query.get_or_404(pos_id)

    # Toggle between open and closed
    if position.posStat == 'open':
        position.posStat = 'closed'
        message = 'Position closed'
    else:
        position.posStat = 'open'
        message = 'Position opened'

    db.session.commit()
    flash(f'{message} successfully!', 'success')
    return redirect(url_for('positions'))


# Activate/Deactivate
@app.route('/candidates/activate/<int:cand_id>')
def activate_candidate(cand_id):
    candidate = Candidate.query.get_or_404(cand_id)
    candidate.candStat = 'active'
    db.session.commit()
    flash('Candidate activated!', 'success')
    return redirect(url_for('candidates'))

@app.route('/candidates/deactivate/<int:cand_id>')
def deactivate_candidate(cand_id):
    candidate = Candidate.query.get_or_404(cand_id)
    candidate.candStat = 'inactive'
    db.session.commit()
    flash('Candidate deactivated!', 'success')
    return redirect(url_for('candidates'))


# Batch Status Update
@app.route('/positions/close-all', methods=['POST'])
def close_all_positions():
    Position.query.update({Position.posStat: 'closed'})
    db.session.commit()
    flash('All positions have been closed!', 'success')
    return redirect(url_for('positions'))


# Status with Condition
@app.route('/voters/reset-voted-status', methods=['POST'])
def reset_voted_status():
    # Reset only for active voters
    Voter.query.filter_by(voterStat='active').update({Voter.voted: 'N'})
    db.session.commit()
    flash('Voted status reset for all active voters!', 'success')
    return redirect(url_for('voters'))
```

---

## API Routes (JSON Response)

```python
# Get All (JSON)
@app.route('/api/positions')
def api_get_positions():
    positions = Position.query.all()
    return jsonify([{
        'posID': p.posID,
        'posName': p.posName,
        'numOfPositions': p.numOfPositions,
        'posStat': p.posStat
    } for p in positions])


# Get Single (JSON)
@app.route('/api/positions/<int:pos_id>')
def api_get_position(pos_id):
    position = Position.query.get_or_404(pos_id)
    return jsonify({
        'posID': position.posID,
        'posName': position.posName,
        'numOfPositions': position.numOfPositions,
        'posStat': position.posStat
    })


# Create (JSON)
@app.route('/api/positions', methods=['POST'])
def api_create_position():
    data = request.get_json()

    # Validation
    if not data.get('posName'):
        return jsonify({'error': 'Position name is required'}), 400

    new_position = Position(
        posName=data['posName'],
        numOfPositions=data.get('numOfPositions', 1),
        posStat=data.get('posStat', 'open')
    )

    db.session.add(new_position)
    db.session.commit()

    return jsonify({
        'message': 'Position created successfully',
        'posID': new_position.posID
    }), 201


# Update (JSON)
@app.route('/api/positions/<int:pos_id>', methods=['PUT'])
def api_update_position(pos_id):
    position = Position.query.get_or_404(pos_id)
    data = request.get_json()

    if 'posName' in data:
        position.posName = data['posName']
    if 'numOfPositions' in data:
        position.numOfPositions = data['numOfPositions']
    if 'posStat' in data:
        position.posStat = data['posStat']

    db.session.commit()

    return jsonify({'message': 'Position updated successfully'})


# Delete (JSON)
@app.route('/api/positions/<int:pos_id>', methods=['DELETE'])
def api_delete_position(pos_id):
    position = Position.query.get_or_404(pos_id)

    db.session.delete(position)
    db.session.commit()

    return jsonify({'message': 'Position deleted successfully'})


# Search (JSON)
@app.route('/api/candidates/search')
def api_search_candidates():
    query = request.args.get('q', '')

    candidates = Candidate.query.filter(
        db.or_(
            Candidate.candFName.ilike(f'%{query}%'),
            Candidate.candLName.ilike(f'%{query}%')
        )
    ).all()

    return jsonify([{
        'candID': c.candID,
        'candFName': c.candFName,
        'candLName': c.candLName,
        'posID': c.posID,
        'candStat': c.candStat
    } for c in candidates])


# Statistics (JSON)
@app.route('/api/stats/dashboard')
def api_dashboard_stats():
    from sqlalchemy import func

    stats = {
        'total_positions': Position.query.count(),
        'open_positions': Position.query.filter_by(posStat='open').count(),
        'total_candidates': Candidate.query.count(),
        'active_candidates': Candidate.query.filter_by(candStat='active').count(),
        'total_voters': Voter.query.count(),
        'voted_voters': Voter.query.filter_by(voted='Y').count(),
        'total_votes': Vote.query.count()
    }

    return jsonify(stats)


# Error Handling (JSON)
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500
```

---

## Common Query Patterns Cheatsheet

### Filters
```python
# Equal
Model.query.filter_by(field=value)
Model.query.filter(Model.field == value)

# Not Equal
Model.query.filter(Model.field != value)

# Like (Case Insensitive)
Model.query.filter(Model.field.ilike('%search%'))

# In List
Model.query.filter(Model.field.in_([val1, val2]))

# Range
Model.query.filter(Model.field.between(min, max))

# AND
Model.query.filter(Model.field1 == val1, Model.field2 == val2)
Model.query.filter(db.and_(Model.field1 == val1, Model.field2 == val2))

# OR
Model.query.filter(db.or_(Model.field1 == val1, Model.field2 == val2))

# Greater Than / Less Than
Model.query.filter(Model.field > value)
Model.query.filter(Model.field < value)
Model.query.filter(Model.field >= value)
Model.query.filter(Model.field <= value)
```

### Ordering
```python
# Ascending
Model.query.order_by(Model.field.asc())

# Descending
Model.query.order_by(Model.field.desc())

# Multiple columns
Model.query.order_by(Model.field1.asc(), Model.field2.desc())
```

### Limiting
```python
# First N records
Model.query.limit(10).all()

# Offset and Limit
Model.query.offset(10).limit(10).all()

# First record
Model.query.first()

# Get by ID
Model.query.get(id)
Model.query.get_or_404(id)
```

### Aggregations
```python
from sqlalchemy import func

# Count
db.session.query(func.count(Model.id)).scalar()

# Sum
db.session.query(func.sum(Model.field)).scalar()

# Average
db.session.query(func.avg(Model.field)).scalar()

# Min/Max
db.session.query(func.min(Model.field)).scalar()
db.session.query(func.max(Model.field)).scalar()
```

---

## Quick Tips for Skilltest

1. **Always use `get_or_404()`** for single records - it handles missing records
2. **Use `flash()`** to show user feedback messages
3. **Redirect after POST** requests to prevent form resubmission
4. **Validate user input** before database operations
5. **Use sessions** for user authentication and temporary data
6. **Remember to commit** after database changes: `db.session.commit()`
7. **Use try-except** for error handling in production code
8. **Filter sensitive data** before displaying (passwords, etc.)
9. **Use query parameters** (`request.args`) for GET, form data (`request.form`) for POST
10. **Always check user permissions** before allowing sensitive operations

---

## Common HTTP Status Codes

- **200**: OK (Success)
- **201**: Created (Resource created successfully)
- **400**: Bad Request (Invalid input)
- **401**: Unauthorized (Not logged in)
- **403**: Forbidden (Logged in but no permission)
- **404**: Not Found (Resource doesn't exist)
- **500**: Internal Server Error (Something went wrong)

---

## Template Variables Access

```python
# Passing data to templates
return render_template('page.html',
    single_var=value,
    list_var=list_data,
    dict_var=dict_data)

# In template (Jinja2):
{{ single_var }}
{% for item in list_var %}
    {{ item }}
{% endfor %}

# Flash messages
{% with messages = get_flashed_messages(with_categories=true) %}
    {% for category, message in messages %}
        <div class="{{ category }}">{{ message }}</div>
    {% endfor %}
{% endwith %}
```

Good luck with your skilltest!

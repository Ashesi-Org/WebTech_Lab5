from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore

#initialize Flask app
app = Flask(__name__)

# Initialize Firestore DB
cred = credentials.Certificate('key.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
url_prefix = '/api/v1'

# Registering voters
@app.route(url_prefix + '/voters/', methods=['POST'])
def register_voter():
    voter_data = request.json
    if not voter_data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Check if all required fields are present
    required_fields = ['name', 'email', 'student_id', 'year_group', 'major']
    for field in required_fields:
        if field not in voter_data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Create a new document in Firestore
    voters_ref = db.collection('voters')
    voters_ref.add(voter_data)
    
    return jsonify({'message': 'Voter registered successfully'}), 200

# De-registering a student as a voter
@app.route(url_prefix + '/voters', methods=['DELETE'])
def delete_voter():
    year_group = request.args.get('year_group')
    voters_ref = db.collection('voters')
    query = voters_ref.where('year_group', '==', year_group)
    voter_docs = query.get()
    
    # Return an error response if no voters found for the given year group
    if len(voter_docs) == 0:
        return jsonify({'error': 'No voters found for the given year group.'}), 404
    
    # Delete the voter document(s)
    for doc in voter_docs:
        doc.reference.delete()
    
    return jsonify({'message': 'Voters de-registered successfully.'}), 200

# Updating a registered voter information
@app.route(url_prefix + '/voters/<student_id>', methods=['PUT'])
def update_voter(student_id):
    record = request.json
    voter_ref = db.collection('voters').document(student_id)
    voter_ref.set(record, merge=True)
    return jsonify(record)

#Retrieving a registered voter's information
@app.route(url_prefix + '/voters', methods=['GET'])
def retrieve_voter():
    year_group = request.args.get('year_group')
    voters_ref = db.collection('voters').where('year_group', '==', year_group).get()
    voters = [voter.to_dict() for voter in voters_ref]
    if voters:
        return jsonify(voters)
    else:
        return jsonify({'error': 'data not found'}), 404
    
# Creating elections
@app.route(url_prefix + '/elections/', methods=['POST'])
def create_elections():
    election_data = request.json
    if not election_data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Check if all required fields are present
    required_fields = ['election_id', 'name', 'session', 'positions']
    for field in required_fields:
        if field not in election_data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Create a new document in Firestore
    elections_ref = db.collection('elections')
    elections_ref.add(election_data)
    
    return jsonify({'message': 'Election registered successfully'}), 200

#Retrieving an election
@app.route(url_prefix + '/elections', methods=['GET'])
def retrieve_election():
    election_id = request.args.get('election_id')
    elections_ref = db.collection('elections').where('election_id', '==', election_id).get()
    elections = [election.to_dict() for election in elections_ref]
    if elections:
        return jsonify(elections)
    else:
        return jsonify({'error': 'data not found'}), 404
    
#Deleting an Election
@app.route(url_prefix + '/elections', methods=['DELETE'])
def delete_election():
    election_id = request.args.get('election_id')
    elections_ref = db.collection('elections')
    query = elections_ref.where('election_id', '==', election_id)
    election_docs = query.get()
    
    # Return an error response if no elections found for the given election id
    if len(election_docs) == 0:
        return jsonify({'error': 'No elections found for election id.'}), 404
    
    # Delete the election document(s)
    for doc in election_docs:
        doc.reference.delete()
    return jsonify({'message': 'Elections removed successfully.'}), 200

# Creating Voting App
@app.route(url_prefix + '/voteapp/', methods=['POST'])
def create_voteapp():
    voteapp_data = request.json
    if not voteapp_data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Check if all required fields are present
    required_fields = ['election_id', 'student_id', 'candidate_id']
    for field in required_fields:
        if field not in voteapp_data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Create a new document in Firestore
    voteapp_ref = db.collection('voteapp')
    voteapp_ref.add(voteapp_data)
    
    return jsonify({'message': 'VoteApp registered successfully'}), 200

if __name__ == '__main__':
    app.run()

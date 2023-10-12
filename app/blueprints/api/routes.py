from flask import jsonify, request
import requests
import os 
from app import db
from flask_cors import CORS, cross_origin
# import base64
# import requests
from app.blueprints.api import api
from app.blueprints.api.models import Event, Invitees, Questions, PollAnswers
from sqlalchemy import select, and_
from sqlalchemy import desc






# # Login - Get Token with Username/Password in header
# @api.route('/token', methods=['POST'])
# # @cross_origin
# @basic_auth.login_required
# def get_token():
#     user = basic_auth.current_user()
#     token = user.get_token()
#     return jsonify({'token': token})


# Create an event
@api.route('/event', methods=['POST'])
# @cross_origin
def create_event():
    data = request.json
    # Validate the data
     # modeled data from front end:
        # data = { 'event':{creatorname:bleh,...},
        #         'questions':{'question1': {questiondate:blah, questiontime:bleh}, 'question2'...
        #   
        # }
    for field in ['creatorname', 'creatoremail', 'eventname', 'shareresults']:
        if field not in data['event']:
            return jsonify({'error': f"You are missing the {field} field"}), 400
    new_event = Event(**data['event'])
    new_event_dict = new_event.to_dict()
    # Grab the data from the request body
    count = 0 
   
    for question in data['questions']:
        for fieldq in ['questiondate', 'questiontime']:
            if fieldq not in question:
                return jsonify({'error': f"You are missing the {fieldq} field"}), 400
        count += 1
        question['event_id'] = new_event_dict['id']
        #i think we need a line here to query from the new_event
        new_question = Questions(**question)
        print(new_question.to_dict())

       


        # }
    print(count)

    # Check if the username or email already exists
    #user_exists = User.query.filter((User.username == username)|(User.email == email)).all()
    # if it is, return back to register
    #if user_exists:
        #return jsonify({'error': f"User with username {username} or email {email} already exists"}), 400

    # Create the new user
    # new_user = User(username=username, email=email, password=password)
    
    return jsonify(new_event_dict)

@api.route('/pollresults', methods=['POST'])
def poll_results():
    data = request.json
    # data = {invitees:{id:, inviteename:, inviteeemail:, eventid:}, pollanswers:{question1{questions_id:, answer:, invitees_id}, question2 {questionsid:,  answer:, invitees_id}
    for field in ['inviteename', 'inviteeemail', 'event_id']:
        if field not in data['invitees']:
            return jsonify({'error': f"You are missing the {field} field"}), 400
    new_invitee = Invitees(**data['invitees'])
    count = 0
    for answer in data['pollanswers']:
        for fielda in ['answer', 'questions_id', 'invitees_id']:
            if fielda not in answer:
                return jsonify({'error': f"You are missing the {fielda} field"}), 400
        count += 1
        new_answer = PollAnswers(**answer)
    return(jsonify(new_invitee.to_dict))





@api.route('/getresults/<int:event_id>')
#@cross_origin
def get_results(event_id):



    #what do i need to return to react:
    #questiondates and question times, amount of answers for each(), who voted for what.
    # we having a page the admin and page the voters.  the page for the admin needs qds and qts, 
    #could be nice to have per person {questiondate, questionname, answers:{personA:answer}, {personB:answer}}
    #get all questions with eventID = blank. then get all answers to each question and get the corresponfing person 
    question_dict = {}
    count = 0
    questions = db.session.execute(db.select(Questions.questiondate, Questions.questiontime, PollAnswers).where(and_((Questions.event_id == event_id), Questions.id == PollAnswers.questions_id))).all()
    print(questions)
    return(jsonify(questions))

# Get user info from token
# @api.route('/me')
# # @cross_origin
# @token_auth.login_required
# def me():
#     return token_auth.current_user().to_dict()

   



# # Get all invitees
# @api.route('/characters1')
# def get_characters():
#     characters = Characters.query.all()
#     return jsonify([c.to_dict() for c in characters])


# # Get a single character with id
# @api.route('/characters/<int:character_id>')
# def get_character(character_id):
#     character = Characters.query.get_or_404(character_id)
#     linkstat = requests.get(character.link).status_code
#     print(linkstat)
#     if linkstat > 209:
#         response1 = openai.Image.create(
#         prompt= character.description,
#         n=1,
#         size="1024x1024"
#         )
#         champ_char = (character.to_dict())
#         print(champ_char)
#         print("hellO")
#         print(type(champ_char))
#         champ_char['link'] = response1['data'][0]['url']
#         print('here')
#         character1 = Characters.query.get_or_404(character.id)
#         character1.update(champ_char)
#         return jsonify(character.to_dict())
#     else:
#         print("hi")
#         return jsonify(character.to_dict())
    


# # Update a single character with id
# @api.route('/characters/<int:character_id>', methods=['PUT'])
# def update_character(character_id):
#     character = Characters.query.get_or_404(character_id)
#     data = request.json
#     character.update(data)
#     return jsonify(character.to_dict())



# @api.route('/hof')
# def get_hof():
#     results = db.session.execute(db.select(Characters).order_by(Characters.wins.desc()).limit(10))
#     counter = 1
#     char_dict = {}
#     for chars in results:
#         for thing in chars:
#             char_dict.update({counter:thing.to_dict()})
#             counter += 1 
#     return jsonify(char_dict)



# # Get champion
# @api.route('/champ')
# def get_champ():
#     results = db.session.execute(db.select(Characters).where(Characters.champion == True)).scalars().all()
#     for chars in results:
#             if chars.champion == True:
#                 print (type(chars))
#                 champ = chars
#                 break
#     linkstat = requests.get(champ.link).status_code
#     print(linkstat)
#     if linkstat > 209:
#         response1 = openai.Image.create(
#         prompt= champ.description,
#         n=1,
#         size="1024x1024"
#         )
#         champ_char = (champ.to_dict())
#         print(champ_char)
#         print("hellO")
#         print(type(champ_char))
#         champ_char['link'] = response1['data'][0]['url']
#         print('here')
#         character = Characters.query.get_or_404(champ.id)
#         character.update(champ_char)
#         return jsonify(character.to_dict())
#     else:
#         print("hi")
#         return jsonify(champ.to_dict())


# # Delete a single character with id
# @api.route('/characters/<int:character_id>', methods=['DELETE'])
# @token_auth.login_required
# def delete_character(character_id):
#     character = Characters.query.get_or_404(character_id)
#     user = token_auth.current_user()
#     if user.id != character.user_id:
#         return jsonify({'error': 'You are not allowed to edit this character'}), 403
#     character.delete()
#     return jsonify({'success': f'{character.title} has been deleted'})

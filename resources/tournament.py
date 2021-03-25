import psycopg2
import os
from flask_restful import Resource, reqparse
from models.tournament import TournamentModel
from flask_jwt_extended import jwt_required, get_jwt_identity

class Tournament(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('t_name',
                        type=str,
                        required=True,
                        help="Tournament name cant be blank"
                        )
    parser.add_argument('location',
                        type=str,
                        required=True,
                        help="location cant be blank"
                        )
    parser.add_argument('college',
                        type=str,
                        required=True,
                        help="college cant be blank"
                        )

    @jwt_required()
    def get(self,username):
        tournaments = TournamentModel.find_by_id(username)

        userTournaments = { 
            "tournaments": []
        }
        
        for t in tournaments:
            userTournaments['tournaments'].append({
                "tournament_id":t[0],
                "t_name":t[1],
                "location":t[2],
                "college":t[3]
            })

        if tournaments:
            return userTournaments
        
        return {"message": "tournaments not found"},404

    @jwt_required()
    def post(self, username):
        user = get_jwt_identity()
        #tournament = TournamentModel.find_by_id(_id)
        #if tournament:
            # status code indicates bad request from client
        #   return {"message": "Tournament with id: {} already exists".format(_id)},400
        
        data = Tournament.parser.parse_args()

        tournament = TournamentModel(data['t_name'],data['location'],data['college'])

        tournament.save_to_db(user)



        return tournament.json(),201


class TournamentList(Resource):
    @jwt_required()
    def get(self):
        tournaments = TournamentModel.findAll()

        userTournaments = { 
            "tournaments": []
        }
        
        for t in tournaments:
            userTournaments['tournaments'].append({
                "tournament_id":t[0],
                "t_name":t[1],
                "location":t[2],
                "college":t[3]
            })

        if tournaments:
            return userTournaments
        
        return {"message": "tournaments not found"},404
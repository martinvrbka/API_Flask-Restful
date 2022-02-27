from flask import Flask, request, jsonify
from flask_restful import Resource, Api

customers = [
             {
              "email": "jan.novak@example.cz",
              "username": "johny",
              "name": "Jan Novak",
              "newsletter_status": True,
              "trips": [
                            {
                             "destination": "Oslo, Norway",
                             "price": 150.00
                            },
                            {
                             "destination": "Bangkok, Thailand",
                             "price": 965.00
                            }
                          ]
             },
             {
              "email": "ivan.opletal@example.com",
              "username": "ivan123",
              "name": "Ivan Opletal",
              "newsletter_status": False,
              "trips": []
             }
        ]

app = Flask(__name__)

api = Api(app)


class Customers(Resource):
    def get(self):
        return {"customers": customers}, 200

class Customer(Resource):
    def get(self, username):
        for customer in customers:
            if customer["username"] == username:
                return customer["username"], 200
        return {"message": f"There is no user with username: {username}"}, 404

    def post(self):
        request_data = request.get_json()
        new_customer = {
            "email": request_data['email'],
            "username": request_data['username'],
            "name": request_data['name'],
            "newsletter_status": request_data['newsletter_status'],
            "trips": []
        }
        for customer in customers:
            if customer['username'] == new_customer['username']:
                return {'error': 'username already exist'}, 409

        customers.append(new_customer)
        return new_customer, 201


    def put(self, username):
        request_data = request.get_json()
        updated_customer = {
            "email": request_data['email'],
            "username": request_data['username'],
            "name": request_data['name'],
            "newsletter_status": request_data['newsletter_status'],
            "trips": []
        }
        for customer in customers:
            if username == customer['username']:
                customer.update(updated_customer)
                return updated_customer, 200

        new_customer = {
            "email": request_data['email'],
            "username": username,
            "name": request_data['name'],
            "newsletter_status": request_data['newsletter_status'],
            "trips": []
        }
        customers.append(new_customer)
        return new_customer, 201


    def delete(self, username):
        for customer in customers:
            if customer["username"] == username:
                customers.remove(customer)
                return {f'message': f'customer {username} was successfully removed'}
        return {"message": "Username not found"}, 404

class Trips(Resource):

    def get(self, username):
        for customer in customers:
            if customer["username"] == username:
                return {"trips": customer["trips"]}
            return {"message": "Username not found"}, 404


    def post(self, username):

        for customer in customers:
            request_data = request.get_json()
            new_trip = {
                "destination": request_data['destination'],
                "price": request_data['price']
            }
            if customer["username"] == username:
                customer["trips"].append(new_trip)
                return new_trip, 201
        return {"message": "Username not found"}, 404



if __name__=='__main__':
    api.add_resource(Customers, '/customers')
    api.add_resource(Customer, '/customer/<string:username>')
    api.add_resource(Trips, '/customer/<string:username>/trips')
    app.run(port=3333, debug=True)



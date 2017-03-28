from flask import Flask, request
from flaskext.mysql import MySQL
from flask_restful import Resource, Api, reqparse
import time
from uuid import getnode as get_mac
app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'XXXXXXX'
app.config['MYSQL_DATABASE_DB'] = 'jarvis_dms'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route("/")
def hello():
	return "Welcome to Python Flask App"

api = Api(app)

def generate_passcode():
	f =  open('/dev/random','r')
	f =  f.read(10)
	passcode = '' # Take starting 6 or 8 characters convert it to integer depending on the need 
	for x in f:
		passcode+=str(ord(x))
	mac =  str(hex(get_mac()))
	print mac[2:-1] # this will print the hex format of the mac address removing the 0x and L characters in string format
	return int(passcode[0:8]) # this is int 

class CreateDevice(Resource):
	def post(self):
		try:
			# Parse the arguments
			# parser = reqparse.RequestParser(bundle_errors=True)
			# parser.add_argument('email', type=str, help='Email address to create user', required=True)
			# parser.add_argument('password', type=str, help='Password to create user', required=True)
			# args = parser.parse_args()

			# _userEmail = args['email']
			# _userPassword = args['password']	
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute("SELECT * FROM `devices` order by id DESC LIMIT 1")
			data = cursor.fetchone()
			if data is None:
				startID = 0
			else:
				startID  = data[0]
			startID += 1001
			requestChannel = 'req' + str(startID)
			responseChannel = 'resp' + str(startID)
			passcode = generate_passcode()
			print passcode
			print type(passcode)
			created_at = time.strftime('%Y-%m-%d %H:%M:%S')

			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute("INSERT INTO devices (requestChannel, responseChannel, passcode, created_at) VALUES (%s,%s,%s,%s)" , 
				(requestChannel, responseChannel, passcode, created_at)
				)
			conn.commit()

			return {
						'deviceID': cursor.lastrowid, 
						'requestChannel': requestChannel, 
						'responseChannel' : responseChannel, 
						'passcode' : passcode, 
						'created_at' : created_at
					}

		except Exception as e:
			return {'error': str(e)}
	
	def get(self):
		return {'status' : 'get'}

api.add_resource(CreateDevice, '/create_device')

if __name__ == "__main__":
	app.run(debug=True, port=5001)
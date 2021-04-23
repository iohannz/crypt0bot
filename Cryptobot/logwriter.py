from datetime import datetime

class Logger:
	def __init__(self):
		pass

	def listen(self, message):
		try:
			print(f"""{datetime.now()}
--------------------------
ID : {message.from_user.id}
Name : {message.from_user.first_name}
Surname : {message.from_user.last_name}
Username : {message.from_user.username}
Language code : {message.from_user.language_code}
Message : {message.text}""")
		except Exception as e:
			print(e)
			print('Something went wrong.. I can feel it.')

	def write_user(self, message):
		username = message.from_user.first_name
		ID = message.from_user.id
		language_code = message.from_user.language_code
		
		lines = []
		with open('users.txt', 'r') as f:
			for line in f:
				if ID in line:
					print('User already in database.')
				else:
					lines.append(f"""
--------------------------
ID : {message.from_user.id}
Name : {message.from_user.first_name}
Language code : {message.from_user.language_code}
User written.""")		
		# Write them back to the file
		with open('users.txt', 'w') as f:
		    f.writelines(lines)
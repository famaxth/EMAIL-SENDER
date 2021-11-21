try:
	EMAIL = str((open('login.txt')).read())
	PASSWORD = str((open('password.txt')).read())
except:
	EMAIL = None
	PASSWORD = None

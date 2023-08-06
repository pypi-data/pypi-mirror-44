import random
first_name = "Chirag"
last_name = "Aswani"
full_name = first_name + " " + last_name
email_address = "chirag@aswani.net"
github = "https://github.com/ChiragAswani"
linkedin = "https://www.linkedin.com/in/chiragaswani/"
facebook = "https://www.facebook.com/ChiragAswani15"
instagram = "https://www.instagram.com/theogchig/"


def random_fact():
	facts = ["Chirag Aswani is 5'6", "Chirag Aswani goes to Boston University", "Chirag loves playing basketball", "Chirag has never broken a bone"]
	random_number = random.randint(0, len(facts)-1)
	return facts[random_number]

import random
name = "Chirag Aswani"

def random_fact():
	facts = ["Chirag Aswani is 5'6", "Chirag Aswani goes to Boston University", "Chirag loves playing basketball", "Chirag has never broken a bone"]
	random_number = random.randint(0, len(facts)-1)
	return facts[random_number]

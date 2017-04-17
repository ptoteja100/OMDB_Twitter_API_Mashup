## Your name: PRASHANT TOTEJA
## The option you've chosen: OPTION 2

# Put import statements you expect to need here!

import unittest
import itertools
import collections
import requests
import tweepy
import twitter_info 
import json
import sqlite3


#Create your caching set up:


#--------calling APIs---------

#Define a function Tweet() that takes an input string and returns a dictionary of 20+ tweets on that input


#Define a function called Twitterusers() that takes a user screen name that is found in any given tweet and returns a dictionary of all that user's info
#Hint: use api.get_user() to get the dictionary of user info

#Define a function called OMDB() that takes and input of a movie name and returns a dictionary of all of that movie's info from the OMDB API




#---------Movie Class------------

#Define a class Movie that will have the info representing any given movie


#Create the __init__ constructor here:


#Define a __str__ method within the movie class that returns a readable output for the user that gives us the name of the movie, by whom it was directed, and the IMDB rating it received


#Define a method within the movie class called listactors() that returns a list of actors that were in that movie


#Define a method within the movie class called numlanguages() that returns the number of languages that were in that movie



#---------------------------------


#Create 3 sql tables: Tweets, Users, Movies 
#Tweets will have the following columns: text, tweet_id(primary key), username(reference the user table), movie_search, num_fav, num_retweets

#Users will have the following columns: user_id(primary key), username, num_fav 

#Movies will have the following columns:  movie_id (primary key), title, director, num_languages, IMDB_rating, top_actor

#Load your info into the database and create two queries, one utilizing JOIN INNER, on your new table


#Find the frequencies of all the actors across all of the movie we iterate over. Save the dictionary in a variable called actor_frequency

 
#Did you find anything interesting? Create a quick summary about your findings and write it into a .txt file for your users!








#Tweepy Setup:

consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

#Create your caching set up:

CACHE_FNAME = "SI206_final_project_cache.json"    

try:
	cache_file = open(CACHE_FNAME, 'r')
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}




CACHE_MNAME = "OMDB_final_project_cache.json"    #Second cache file needed for OMDB function since tweet query and movie query may be the same!

try:
	cache_file = open(CACHE_MNAME, 'r')
	cache_contents = cache_file.read()
	cache_file.close()
	OMDB_CACHE_DICTION = json.loads(cache_contents)
except:
	OMDB_CACHE_DICTION = {}


CACHE_UNAME = "User_final_project_cache.json"      #another needed since user_mentions will cause us to always get cached data 

try:
	cache_file = open(CACHE_UNAME, 'r')
	cache_contents = cache_file.read()
	cache_file.close()
	USER_CACHE_DICTION = json.loads(cache_contents)
except:
	USER_CACHE_DICTION = {}
#--------calling APIs---------

#Define a function Tweet() that takes an input string and returns a dictionary of 20+ tweets on that input

def get_tweets(input_string):
	returnedList = []

	if input_string in CACHE_DICTION:
		print("Using cached data for", input_string)
		returnedList = CACHE_DICTION[input_string]
	else:
		print("getting new data from the web for", input_string)
		search_results = api.search(input_string)
		toString = json.dumps(search_results)
		toJsonAgain = json.loads(toString)
		returnedList = toJsonAgain

	CACHE_DICTION[input_string] = returnedList
	f = open(CACHE_FNAME, "w")
	f.write(json.dumps(CACHE_DICTION))
	f.close()

	return returnedList



def user_info(dictionary):
	returnedList = []
	screenames_list = []
	stringed_version = json.dumps(dictionary)
	if stringed_version in USER_CACHE_DICTION:
		print("Using cached data")
		returnedList = USER_CACHE_DICTION[stringed_version]
	else:
		for i in dictionary['statuses']:
			tester = i['user']['screen_name']
			screenames_list.append(tester)

	for j in screenames_list:
		search_results = api.get_user(screen_name = j)  
		toString = json.dumps(search_results)
		toJsonAgain = json.loads(toString)
		returnedList.append(toJsonAgain)

	USER_CACHE_DICTION[stringed_version] = returnedList
	f = open(CACHE_UNAME, "w")
	f.write(json.dumps(USER_CACHE_DICTION))
	f.close()

	return returnedList




somelist = []
def usersmentioned_info(dictionary):        #returns all the user mentions without duplicates
	returnedList = []
	screenames_list = []
	dummylist = []
	stringed_version = json.dumps(dictionary)
	if stringed_version in CACHE_DICTION:
		print("Using cached data")
		returnedList = CACHE_DICTION[stringed_version]

	else:

		for i in dictionary['statuses']:
			tester = i['entities']['user_mentions']
			dummylist.append(tester)
		for listy in dummylist:
			for j in listy:
				screenames_list.append(j['screen_name'])



	remove_duplicates_list = []
	for i in screenames_list:
		if i not in remove_duplicates_list:
			remove_duplicates_list.append(i)		
	


	somelist.append(len(remove_duplicates_list))

		
					   #Should be a list holding all the screennames for the people mentioned in the tweets
			

	for j in remove_duplicates_list:
		search_results = api.get_user(screen_name = j)  
		toString = json.dumps(search_results)
		toJsonAgain = json.loads(toString)
		returnedList.append(toJsonAgain)

	CACHE_DICTION[stringed_version] = returnedList
	f = open(CACHE_FNAME, "w")
	f.write(json.dumps(CACHE_DICTION))
	f.close()

	return returnedList



def OMDB(movie_name):
	returnedList = []

	if movie_name in OMDB_CACHE_DICTION:
		print("Using cached data for", movie_name)
		omdb_data_dictionary = OMDB_CACHE_DICTION[movie_name]
	else:
		print("getting new data from the web for", movie_name)
		customizingurl = movie_name.replace(" ", "+")
		customizingurlfinal = "http://www.omdbapi.com/?t=" + customizingurl
		omdb_data_dictionary = requests.get(customizingurlfinal).text   #omdb_data now holds all of the movie's data in a dictionary.
		toJson = json.loads(omdb_data_dictionary)
		omdb_data_dictionary = toJson
	OMDB_CACHE_DICTION[movie_name] = omdb_data_dictionary
	f = open(CACHE_MNAME, "w")
	f.write(json.dumps(OMDB_CACHE_DICTION))
	f.close()

	return omdb_data_dictionary


class Movie():


	def __init__(self, dict_of_movie_data, title, director, rating):

		self.dict_of_movie_data = dict_of_movie_data
		self.title = title
		self.director = director
		self.rating = rating

	def __str__(self):

		return "{} is a movie that was directed by {} and was given an IMDB rating of {}.".format(self.title, self.director, self.rating)

	def listactors(self):
		list_of_actors = []
		string_of_actors = self.dict_of_movie_data['Actors']
		list_of_actors = string_of_actors.split(", ")	
			
		return list_of_actors

	def numlanguages(self):
		list_of_languages = []
		string_of_languages = self.dict_of_movie_data['Language']
		list_of_languages = string_of_languages.split(", ")

		return len(list_of_languages)






search_terms = ["Batman Begins", "National Treasure", "Moneyball"] 
list_of_movies = []
for movie in search_terms:
	movie_data = OMDB(movie)

	type_movie = Movie(movie_data, movie_data['Title'], movie_data['Director'], movie_data['imdbRating'])
	list_of_movies.append(type_movie)

list_of_tweets = []
star_actorlist = []



for i in list_of_movies:
	star_actor = i.listactors()[0]
	star_actorlist.append(star_actor)
	star_actor_tweets = get_tweets(star_actor)
	list_of_tweets.append(star_actor_tweets)





list_of_user_info = []
for tweetdata in list_of_tweets:
	x = usersmentioned_info(tweetdata)
	list_of_user_info.append(x)

listofposterinfo = []
for tweetdata in list_of_tweets:
	y = user_info(tweetdata)
	listofposterinfo.append(y)











conn = sqlite3.connect('final_project_206.db')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS final_project_206')

table_spec = "CREATE TABLE IF NOT EXISTS "
table_spec += "Tweets (tweet_id TEXT PRIMARY KEY, text TEXT, user TEXT, movie_search_term TEXT, num_favs INTEGER, num_retweets INTEGER)"  
cur.execute(table_spec)


table_spec = "CREATE TABLE IF NOT EXISTS "    #to vizualize the social network in the database
table_spec += "Users_Mentioned (user_id TEXT PRIMARY KEY, user TEXT, num_favs_by_user INTEGER)"
cur.execute(table_spec)


table_spec = "CREATE TABLE IF NOT EXISTS "
table_spec += "Movies (movie_id TEXT PRIMARY KEY, title TEXT, director TEXT, num_languages INTEGER, IMDB_rating TEXT, main_actor TEXT)"
cur.execute(table_spec)

table_spec = "CREATE TABLE IF NOT EXISTS "
table_spec += "Users (user_ids TEXT PRIMARY KEY, users TEXT, number_favs_by_user INTEGER)"
cur.execute(table_spec)

statement = 'DELETE FROM Tweets'
cur.execute(statement)
statement = 'DELETE FROM Users_Mentioned'
cur.execute(statement)
statement = 'DELETE FROM Movies'
cur.execute(statement)
statement = 'DELETE FROM Users'
cur.execute(statement)
conn.commit()


movieidlist = []  
titlelist = []       
directorlist = []      
numlanguageslist = []     
ratinglist = []       
mainactorlist = []       

for i in list_of_movies:
	movieidlist.append(i.dict_of_movie_data['imdbID'])
	titlelist.append(i.title)
	directorlist.append(i.director)
	numlanguageslist.append(i.numlanguages())
	ratinglist.append(i.rating)
	mainactorlist.append(i.listactors()[0])

movietups = list(zip(movieidlist, titlelist, directorlist, numlanguageslist, ratinglist, mainactorlist))

statement = 'INSERT INTO Movies VALUES (?, ?, ?, ?, ?, ?)'

for t in movietups:
	cur.execute(statement, t)

conn.commit()

listofuserids = []
listofuserscreennames = []
listofnumfavsbyuser = []



for i in list_of_user_info:
	for j in i:
		listofuserids.append(j['id_str'])
		listofuserscreennames.append(j['screen_name'])
		listofnumfavsbyuser.append(j['favourites_count'])





usersmentionedtups = list(zip(listofuserids, listofuserscreennames, listofnumfavsbyuser))

statement = 'INSERT OR IGNORE INTO Users_Mentioned VALUES (?, ?, ?)'

for t in usersmentionedtups:
	cur.execute(statement, t)

conn.commit()



ids = []
postersnames = []
numberfavs = []
for i in listofposterinfo:
	for j in i:
		ids.append(j['id_str'])
		postersnames.append(j['screen_name'])
		numberfavs.append(j['favourites_count'])


usertups = list(zip(ids, postersnames, numberfavs))

statement = 'INSERT OR IGNORE INTO Users VALUES (?, ?, ?)'

for t in usertups:
	cur.execute(statement,t)

conn.commit()






tweetidlist = []
textlist = []
userscreennamelist = []   #from user table
moviesearchlist = []      #from movie table
numberfavoriteslist = []
numberofretweetslist = []

numberoftweetsforeachmovie = []


for i in list_of_tweets:
	
	for j in i['statuses']:      #j -- [[tweet,tweet,tweet,tweet], [tweet, tweet, tweet], [tweet]]
		tweetidlist.append(j['id_str'])
		textlist.append(j['text'])
	#listofuserscreennames
	#titlelist
		numberfavoriteslist.append(j['favorite_count'])
		numberofretweetslist.append(j['retweet_count'])
	


count = 0
for search_term in mainactorlist:       #referring to the movie table since we found our tweets based on the main actor
	while count < 15:						#search() returns 15 tweets for each search term
		moviesearchlist.append(search_term)
		count += 1
	count = 0              #reset the counter





tweetstups = list(zip(tweetidlist, textlist, postersnames, moviesearchlist,  numberfavoriteslist, numberofretweetslist))

statement  = 'INSERT OR IGNORE INTO Tweets VALUES (?, ?, ?, ?, ?, ?)'

for t in tweetstups:
	cur.execute(statement, t)

conn.commit()





query = "SELECT Tweets.text FROM Tweets WHERE num_retweets > 50"
tupled_more_than_50_rts = list(cur.execute(query))						#list comprehension
list_of_more_than_50_rts = [i[0] for i in tupled_more_than_50_rts]    #list of all tweets with more than 1000 retweets     

print("-------------------")
print("-------------------")
print("These are all the tweets with more than 50 retweets:")
print(list_of_more_than_50_rts)




query = "SELECT Movies.title, Tweets.num_retweets FROM Movies INNER JOIN Tweets ON Movies.main_actor = Tweets.movie_search_term"
joined_result = list(cur.execute(query))

d = collections.defaultdict(list)
for k,v in joined_result:
	d[k].append(v)				#new containers from collections library
twitter_dictionary = dict(d)    #dictionary of users joined with their tweets

print("-------------------")
print("-------------------")
print("Which leading actor is most popular?")
print("Here are all the movies along side the number or retweets for their leading actor:")
print(twitter_dictionary)    


query = "SELECT Tweets.text, Tweets.num_favs FROM Tweets"
tupled_list = list(cur.execute(query))
tweets_with_likes = list(filter(lambda x: x[1] > 0, tupled_list))   #filter used

print("-------------------")
print("-------------------")
print("Here are all the tweets that actually got some likes...and how many likes they got:")
print(tweets_with_likes)



query = "SELECT Users_Mentioned.user, Users_Mentioned.num_favs_by_user FROM Users_Mentioned"
tupled_mentioned = list(cur.execute(query))
users_mentioned_filtered = {}    #accumulating dictionary
for i in tupled_mentioned:
	if i[1] > 10000:
		users_mentioned_filtered[i[0]] = i[1]


print("-------------------")
print("-------------------")
print("Here are the active twitter users amongst the users mentioned based off how much they favorite (greater than 10,000!):")
print(users_mentioned_filtered)

print("-------------------")
print("-------------------")








text_file = "Check_Out_The_Results.txt"
textfile = open(text_file, 'w')
textfile.write("These are the movies we did some digging on:")
textfile.write("\n")
textfile.write("\n")
for i in search_terms:
	textfile.write(str(i))
	textfile.write("\n")
textfile.write("\n")
textfile.write("\n")	
for i in list_of_movies:
	textfile.write(i.__str__())
	textfile.write("\n")
textfile.write("\n")
textfile.write("\n")
textfile.write("These are all the tweets with more than 50 retweets:")
textfile.write("\n")
textfile.write("\n")
textfile.write(str(list_of_more_than_50_rts))
textfile.write("\n")
textfile.write("\n")
textfile.write("Which leading actor is most popular?")
textfile.write("Here are all the movies along side the number or retweets for their leading actor:")
textfile.write("\n")
textfile.write("\n")
textfile.write(str(twitter_dictionary))
textfile.write("\n")
textfile.write("\n")
textfile.write("Here are all the tweets that actually got some likes...and how many likes they got:")
textfile.write("\n")
textfile.write("\n")
textfile.write(str(tweets_with_likes))
textfile.write("\n")
textfile.write("\n")
textfile.write("Here are the active twitter users amongst the users mentioned based off how much they favorite (greater than 10,000!):")
textfile.write("\n")
textfile.write("\n")
textfile.write(str(users_mentioned_filtered))
textfile.write("\n")
textfile.close()






print("---------------Test Cases Below This Line--------------")

# Write your test cases here.

class Sqltask(unittest.TestCase):
	def test_users1(self):
		conn = sqlite3.connect('finalproject_tweets.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Users');
		result = cur.fetchall()
		self.assertTrue(len(result) >= 2, "There should be 2 or more distinct users in the User table!!")
		conn.close()

	def test_users2(self):
		conn = sqlite3.connect('finalproject_tweets.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Tweets');
		result = cur.fetchall()
		self.assertTrue(len(result[0]) == 6, "Testing that there are 6 columns in the Tweets table")
		conn.close()

class Moretests(unittest.TestCase):
	def test_tweeter(self):
		self.assertTrue(type(tweeter('Tom Cruise')), type({"hi","bye"}), "Testing that the tweeter function returns a type dictionary of tweets")

	def test_twitterusers(self):
		self.assertTrue(type(twitterusers('Tome Cruise')), type({"hi","bye"}), "Testing that the twitterusers function returns a type dictionary of users")
	def test_Movie1(self):
		x = omdb('Titanic')
		mymovie = Movie(dict = x)
		self.assertTrue(type(mymovie.listactors()), type([]), "Testing that the listactors function returns a type list when called on a movie")
	def test_Movie2(self):
		x = omdb('Titanic')
		mymovie = Movie(dict = x)
		self.assertTrue(type(mymovie.numlanguages()), type(1), "Testing that the numlanguages function returns a type integer when called on a movie")
	def test_actor_frequency(self):
		self.assertEqual(type(actor_frequency),type({}),"Testing that mostcommon_actor across inputed movies is of type dictionary")


	def test_movielist(self):
		self.assertEqual(len(movielist) >= 3,"Testing that we will be running the ombd function on a list that contains 3 or more movie names")




## Remember to invoke all your tests...

if __name__ == "__main__":
	unittest.main(verbosity = 2)
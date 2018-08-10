
import unittest
import itertools
import collections
import requests
import tweepy
import twitter_info 
import json
import sqlite3


#Tweepy Setup:

consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

#Creating caching set up:

CACHE_FNAME = "SI206_final_project_cache.json"    #three cache files because reptitive keys will change our value even though we want to display different information for each key

try:
	cache_file = open(CACHE_FNAME, 'r')
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}




CACHE_MNAME = "OMDB_final_project_cache.json"    #Second cache file for OMDB function

try:
	cache_file = open(CACHE_MNAME, 'r')
	cache_contents = cache_file.read()
	cache_file.close()
	OMDB_CACHE_DICTION = json.loads(cache_contents)
except:
	OMDB_CACHE_DICTION = {}


CACHE_UNAME = "User_final_project_cache.json"       

try:
	cache_file = open(CACHE_UNAME, 'r')
	cache_contents = cache_file.read()
	cache_file.close()
	USER_CACHE_DICTION = json.loads(cache_contents)
except:
	USER_CACHE_DICTION = {}

#--------calling APIs---------

def get_tweets(input_string):
	returnedList = []

	if input_string in CACHE_DICTION:
		print("Using cached data for", input_string)    #If we've searched this leading actor before, return the cached twitter info
		returnedList = CACHE_DICTION[input_string]
	else:
		print("getting new data from the web for", input_string)   #else, we are going to the web to find the tweets about that query
		search_results = api.search(input_string)    
		toString = json.dumps(search_results)     #Converting into a string for visualizing purposes
		toJsonAgain = json.loads(toString)		#putting it all back into json format and assigning it to variable returnedList in the next line.
		returnedList = toJsonAgain

	CACHE_DICTION[input_string] = returnedList    #caching
	f = open(CACHE_FNAME, "w")
	f.write(json.dumps(CACHE_DICTION))
	f.close()

	return returnedList    



def user_info(dictionary):  #this function takes a dictionary of tweets and returns the info of the user who tweeted
	returnedList = []
	screenames_list = []
	stringed_version = json.dumps(dictionary)
	if stringed_version in USER_CACHE_DICTION:   #Get from cached if we've run this before
		print("Using cached data")
		returnedList = USER_CACHE_DICTION[stringed_version]
	else:
		for i in dictionary['statuses']:     #accessing the user's screen names
			tester = i['user']['screen_name']
			screenames_list.append(tester)

	for j in screenames_list:
		search_results = api.get_user(screen_name = j)   #tweepy function to get the user's info based on their inputted user name
		toString = json.dumps(search_results)
		toJsonAgain = json.loads(toString)
		returnedList.append(toJsonAgain)

	USER_CACHE_DICTION[stringed_version] = returnedList    #Cache
	f = open(CACHE_UNAME, "w")
	f.write(json.dumps(USER_CACHE_DICTION))
	f.close()

	return returnedList      #return users info




somelist = []
def usersmentioned_info(dictionary):        #returns all the user mentions without duplicates
	returnedList = []
	screenames_list = []
	dummylist = []
	stringed_version = json.dumps(dictionary)
	if stringed_version in CACHE_DICTION:     #use cached data
		print("Using cached data")
		returnedList = CACHE_DICTION[stringed_version]

	else:

		for i in dictionary['statuses']:
			tester = i['entities']['user_mentions']    #Getting the screenames of the users that are mentioned in the tweets
			dummylist.append(tester)
		for listy in dummylist:
			for j in listy:
				screenames_list.append(j['screen_name'])



	remove_duplicates_list = []
	for i in screenames_list:
		if i not in remove_duplicates_list:
			remove_duplicates_list.append(i)	#Removing duplicates
	


	somelist.append(len(remove_duplicates_list))

		
					   #list holding all the screennames for the people mentioned in the tweets
			

	for j in remove_duplicates_list:
		search_results = api.get_user(screen_name = j)   #tweepy function to get the users who are mentioned in twitter info
		toString = json.dumps(search_results)
		toJsonAgain = json.loads(toString)
		returnedList.append(toJsonAgain)

	CACHE_DICTION[stringed_version] = returnedList   #caching
	f = open(CACHE_FNAME, "w")
	f.write(json.dumps(CACHE_DICTION))
	f.close()

	return returnedList   #returning the twitter info about the users mentioned



def OMDB(movie_name):        #takes a movie name and makes a call to the OMDB API to get a JSON object
	returnedList = []

	if movie_name in OMDB_CACHE_DICTION:    #Use cached 
		print("Using cached data for", movie_name)
		omdb_data_dictionary = OMDB_CACHE_DICTION[movie_name]
	else:
		print("getting new data from the web for", movie_name)
		customizingurl = movie_name.replace(" ", "+")               #For movie names with multiple words, cleaning the data
		customizingurlfinal = "http://www.omdbapi.com/?t=" + customizingurl
		omdb_data_dictionary = requests.get(customizingurlfinal).text   #omdb_data holds movie's data in a dictionary.
		toJson = json.loads(omdb_data_dictionary)
		omdb_data_dictionary = toJson
	OMDB_CACHE_DICTION[movie_name] = omdb_data_dictionary
	f = open(CACHE_MNAME, "w")
	f.write(json.dumps(OMDB_CACHE_DICTION))       #Caching our movie info into our file
	f.close()

	return omdb_data_dictionary    #returning the dictionary that hold all of our movie info


class Movie():      


	def __init__(self, dict_of_movie_data, title, director, rating):   #constructor takes a few parameters - the dictionary of the movie data, the title, director, and rating of the movie

		self.dict_of_movie_data = dict_of_movie_data    
		self.title = title
		self.director = director
		self.rating = rating

	def __str__(self):

		return "{} is a movie that was directed by {} and was given an IMDB rating of {}.".format(self.title, self.director, self.rating)   #For reading purposes - gives us summary on the movie 

	def listactors(self):				#returns a list of the actors in the movie out of the dictionary of movie info inputted.
		list_of_actors = []
		string_of_actors = self.dict_of_movie_data['Actors']
		list_of_actors = string_of_actors.split(", ")	
			
		return list_of_actors

	def numlanguages(self):      #returns the number of languages that the movie is in out of the dictionary of movie info
		list_of_languages = []
		string_of_languages = self.dict_of_movie_data['Language']
		list_of_languages = string_of_languages.split(", ")

		return len(list_of_languages)






search_terms = ["Batman Begins", "National Treasure", "Moneyball"]      #Tests
list_of_movies = []
for movie in search_terms:
	movie_data = OMDB(movie)

	type_movie = Movie(movie_data, movie_data['Title'], movie_data['Director'], movie_data['imdbRating'])
	list_of_movies.append(type_movie)

list_of_tweets = []
star_actorlist = []



for i in list_of_movies:    #for each leading actor, make list with all the tweet info
	star_actor = i.listactors()[0]
	star_actorlist.append(star_actor)
	star_actor_tweets = get_tweets(star_actor)
	list_of_tweets.append(star_actor_tweets)





list_of_user_info = []    #accumulating all the twitter info for the users mentioned
for tweetdata in list_of_tweets:
	x = usersmentioned_info(tweetdata)
	list_of_user_info.append(x)

listofposterinfo = []          #for each tweet, we are getting the poster's user info and putting it all into single list.
for tweetdata in list_of_tweets:
	y = user_info(tweetdata)
	listofposterinfo.append(y)











conn = sqlite3.connect('final_project_206.db')    #Setting up database
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS final_project_206')

table_spec = "CREATE TABLE IF NOT EXISTS "
table_spec += "Tweets (tweet_id TEXT PRIMARY KEY, text TEXT, user TEXT, movie_search_term TEXT, num_favs INTEGER, num_retweets INTEGER)"  
cur.execute(table_spec)


table_spec = "CREATE TABLE IF NOT EXISTS "    
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

statement = 'INSERT INTO Movies VALUES (?, ?, ?, ?, ?, ?)'     #movie info to database

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

statement = 'INSERT OR IGNORE INTO Users VALUES (?, ?, ?)'   #putting all the tweet info into our database.

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
	
	for j in i['statuses']:      
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
	count = 0            





tweetstups = list(zip(tweetidlist, textlist, postersnames, moviesearchlist,  numberfavoriteslist, numberofretweetslist))

statement  = 'INSERT OR IGNORE INTO Tweets VALUES (?, ?, ?, ?, ?, ?)'    #putting all the tweets found into database

for t in tweetstups:
	cur.execute(statement, t)

conn.commit()





query = "SELECT Tweets.text FROM Tweets WHERE num_retweets > 50"
tupled_more_than_50_rts = list(cur.execute(query))				
list_of_more_than_50_rts = [i[0] for i in tupled_more_than_50_rts]    #list of all tweets with more than 50 retweets     

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

print("-------------------")	#getting all the movies along side the number of retweets for their leading actor 
print("-------------------")
print("Which leading actor is most popular?")
print("Here are all the movies along side the number of retweets for their leading actor:")
print(twitter_dictionary)    


query = "SELECT Tweets.text, Tweets.num_favs FROM Tweets"
tupled_list = list(cur.execute(query))
tweets_with_likes = list(filter(lambda x: x[1] > 0, tupled_list))   

print("-------------------")				#Get all the tweets that got likes and how many they got
print("-------------------")
print("Here are all the tweets that actually got some likes...and how many likes they got:")
print(tweets_with_likes)



query = "SELECT Users_Mentioned.user, Users_Mentioned.num_favs_by_user FROM Users_Mentioned"
tupled_mentioned = list(cur.execute(query))
users_mentioned_filtered = {}    
for i in tupled_mentioned:
	if i[1] > 10000:
		users_mentioned_filtered[i[0]] = i[1]


print("------------------")          #From the users mentioned, we got all the active users based on whether or not they favorited more than 10,000 times
print("------------------")
print("Here are the active twitter users amongst the users mentioned based off how much they favorite (greater than 10,000!):")
print(users_mentioned_filtered)

print("------------------")
print("------------------")






#Writing to text file


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
	textfile.write(i.__str__())    #calling the __str__() function for us to get the basic information about the movies inputted
	textfile.write("\n")
textfile.write("\n")
textfile.write("\n")
textfile.write("These are all the tweets with more than 50 retweets:")
textfile.write("\n")
textfile.write("\n")
for tweet in list_of_more_than_50_rts:
	textfile.write(str(tweet))
	textfile.write("\n")
	textfile.write("\n")
textfile.write("\n")
textfile.write("\n")
textfile.write("Which leading actor is most popular? ")
textfile.write("Here are all the movies along side the number of retweets each of the 15 tweets got for their leading actor:")
textfile.write("\n")
textfile.write("\n")
listofmoviekeys = list(twitter_dictionary.keys())
for i in listofmoviekeys:
	textfile.write("Movie Name: " + str(i))
	textfile.write("\n")
	textfile.write("The 15 tweets got ")
	for j in twitter_dictionary[i]:
		textfile.write(str(j) + " ")
	textfile.write("retweets respectively")
	textfile.write("\n")
	textfile.write("\n")



textfile.write("\n")
textfile.write("\n")
textfile.write("Here are all the tweets that actually got some likes...and how many likes they got:")
textfile.write("\n")
textfile.write("\n")
for i in tweets_with_likes:
	textfile.write(str(i[0]))
	textfile.write("\n")
	textfile.write("The number of likes this tweet got: " + str(i[1]))
	textfile.write("\n")
	textfile.write("\n")

textfile.write("\n")
textfile.write("\n")
textfile.write("Here are the active twitter users amongst the users mentioned. They all have more than 10,000 favorites!:")
textfile.write("\n")
textfile.write("\n")
listofkeys = list(users_mentioned_filtered.keys())
for i in listofkeys:
	textfile.write("Screename: " + str(i))
	textfile.write("\n")
	textfile.write("And their number of favorites: " + str(users_mentioned_filtered[i]))
	textfile.write("\n")
	textfile.write("\n")

textfile.write("\n")
textfile.close()






print("---------------Test Cases Below This Line--------------")


class Sqltask(unittest.TestCase):
	def test_users1(self):
		conn = sqlite3.connect('final_project_206.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Users');
		result = cur.fetchall()
		self.assertTrue(len(result) >= 2, "There should be 2 or more distinct users in the User table!!")
		conn.close()

	def test_users2(self):
		conn = sqlite3.connect('final_project_206.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Tweets');
		result = cur.fetchall()
		self.assertTrue(len(result[0]) == 6, "Testing that there are 6 columns in the Tweets table")
		conn.close()

class APItests(unittest.TestCase):
	def test_get_tweets(self):
		self.assertTrue(type(get_tweets('Tom Cruise')), type({"hi","bye"}))   

	def test_get_tweets2(self):
		self.assertTrue(len(get_tweets('Nicolas Cage')['statuses']) > 1)   

	def test_user_info1(self):
		self.assertTrue(type(user_info(get_tweets('Will Smith'))), type({"hello", "goodbye"}))   

	def test_usersmentioned_info(self):
		self.assertTrue(type(usersmentioned_info(get_tweets('Christian Bale'))), type({"hi", "bye"}))  

	def test_OMDB(self):
		self.assertTrue(type(OMDB('King Kong')['Title']), type('string please'))  

	def test_OMDB2(self):
		self.assertTrue(OMDB('21')['Title'], '21')  



class MovieClassMethodsTests(unittest.TestCase):

	
	def test_constructor(self):
		moviedata = OMDB('Finding Nemo')
		tester_movie = Movie(moviedata, moviedata['Title'], moviedata['Director'], moviedata['imdbRating'])
		self.assertTrue(type(tester_movie.title), type('This should be a string'))    


	def test_str(self):
		moviedata = OMDB('Finding Nemo')
		tester_movie = Movie(moviedata, moviedata['Title'], moviedata['Director'], moviedata['imdbRating'])
		self.assertTrue(type(tester_movie.__str__()), type('This should be a string too!'))   

	def test_listactors(self):
		moviedata = OMDB('Finding Nemo')
		tester_movie = Movie(moviedata, moviedata['Title'], moviedata['Director'], moviedata['imdbRating'])
		self.assertTrue(type(tester_movie.listactors()), type([]))      

	def test_numlanguages(self):
		moviedata = OMDB('Finding Nemo')
		tester_movie = Movie(moviedata, moviedata['Title'], moviedata['Director'], moviedata['imdbRating'])
		self.assertTrue(type(tester_movie.numlanguages()), type(1))    



#invoke tests

if __name__ == "__main__":
	unittest.main(verbosity = 2)
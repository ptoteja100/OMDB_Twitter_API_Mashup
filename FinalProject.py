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


#--------calling APIs-----------------

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

CACHE_FNAME = "SI206_final_project_cache.json"       #We use three cache files because reptitive keys will change our value even though we want to display different information for that key.

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


CACHE_UNAME = "User_final_project_cache.json"      #Another needed since user_mentions will cause us to always get cached data! 

try:
	cache_file = open(CACHE_UNAME, 'r')
	cache_contents = cache_file.read()
	cache_file.close()
	USER_CACHE_DICTION = json.loads(cache_contents)
except:
	USER_CACHE_DICTION = {}

#--------calling APIs---------

#Define a function get_tweets() that takes an input string and returns a dictionary of 15 tweets on that input

def get_tweets(input_string):
	returnedList = []

	if input_string in CACHE_DICTION:
		print("Using cached data for", input_string)    #If we've searched this leading actor before, return the cached tiwtter information about it.
		returnedList = CACHE_DICTION[input_string]
	else:
		print("getting new data from the web for", input_string)   #else, we are going to the web to find the tweets about that query
		search_results = api.search(input_string)    
		toString = json.dumps(search_results)     #Converting into a string for visualizing purposes
		toJsonAgain = json.loads(toString)		#putting it all back into json format and assigning it to variable returnedList in the next line.
		returnedList = toJsonAgain

	CACHE_DICTION[input_string] = returnedList    #Now that we went to the web, let's cache the data in one of our files so that we can access it later.
	f = open(CACHE_FNAME, "w")
	f.write(json.dumps(CACHE_DICTION))
	f.close()

	return returnedList    #return the tweet information



def user_info(dictionary):  #this function takes a dictionary (should be tweets) and returns the info of the user who tweeted
	returnedList = []
	screenames_list = []
	stringed_version = json.dumps(dictionary)
	if stringed_version in USER_CACHE_DICTION:   #Get from cached if we've run this before
		print("Using cached data")
		returnedList = USER_CACHE_DICTION[stringed_version]
	else:
		for i in dictionary['statuses']:     #accessing the user's screenames so that we can get their info based on this field
			tester = i['user']['screen_name']
			screenames_list.append(tester)

	for j in screenames_list:
		search_results = api.get_user(screen_name = j)   #tweepy function to get the user's info based on their inputted user name
		toString = json.dumps(search_results)
		toJsonAgain = json.loads(toString)
		returnedList.append(toJsonAgain)

	USER_CACHE_DICTION[stringed_version] = returnedList    #Cache this info for next time we run this function
	f = open(CACHE_UNAME, "w")
	f.write(json.dumps(USER_CACHE_DICTION))
	f.close()

	return returnedList      #return our users' info




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
			tester = i['entities']['user_mentions']    #Otherwise, getting the screenames of the users that are mentioned in the tweets. We will use this function in constructing our social network in our database.
			dummylist.append(tester)
		for listy in dummylist:
			for j in listy:
				screenames_list.append(j['screen_name'])



	remove_duplicates_list = []
	for i in screenames_list:
		if i not in remove_duplicates_list:
			remove_duplicates_list.append(i)		  #Removing duplicates so that we do not gather replicated data when getting info of each user.
	


	somelist.append(len(remove_duplicates_list))

		
					   #Should be a list holding all the screennames for the people mentioned in the tweets
			

	for j in remove_duplicates_list:
		search_results = api.get_user(screen_name = j)   #tweepy function to get the users who are mentioned's twitter info
		toString = json.dumps(search_results)
		toJsonAgain = json.loads(toString)
		returnedList.append(toJsonAgain)

	CACHE_DICTION[stringed_version] = returnedList   #caching in our file so we have it for next time!
	f = open(CACHE_FNAME, "w")
	f.write(json.dumps(CACHE_DICTION))
	f.close()

	return returnedList   #returning the twitter info about the users mentioned



def OMDB(movie_name):        #takes a movie name and makes a call to the OMDB API to get a JSON object that essentially holds all the important information about the movie.
	returnedList = []

	if movie_name in OMDB_CACHE_DICTION:    #Used cached data if we've run this on a movie we've searched before.
		print("Using cached data for", movie_name)
		omdb_data_dictionary = OMDB_CACHE_DICTION[movie_name]
	else:
		print("getting new data from the web for", movie_name)
		customizingurl = movie_name.replace(" ", "+")               #For movie names with multiple words, we need to do a little clean up to make sure we make the right call to the URL.
		customizingurlfinal = "http://www.omdbapi.com/?t=" + customizingurl
		omdb_data_dictionary = requests.get(customizingurlfinal).text   #omdb_data now holds all of the movie's data in a dictionary.
		toJson = json.loads(omdb_data_dictionary)
		omdb_data_dictionary = toJson
	OMDB_CACHE_DICTION[movie_name] = omdb_data_dictionary
	f = open(CACHE_MNAME, "w")
	f.write(json.dumps(OMDB_CACHE_DICTION))       #Caching our movie info into our file
	f.close()

	return omdb_data_dictionary    #returning the dictionary that hold all of our movie info.


class Movie():      #This class will represent a movie


	def __init__(self, dict_of_movie_data, title, director, rating):   #constructor takes a few parameters - the dictionary of the movie data, the title, director, and rating of the movie

		self.dict_of_movie_data = dict_of_movie_data    
		self.title = title
		self.director = director
		self.rating = rating

	def __str__(self):

		return "{} is a movie that was directed by {} and was given an IMDB rating of {}.".format(self.title, self.director, self.rating)   #For reading purposes - basically gives us a quick summary on the movie we have on hand

	def listactors(self):				#returns a list of the actors in the movie out of the dictionary of movie info inputted.
		list_of_actors = []
		string_of_actors = self.dict_of_movie_data['Actors']
		list_of_actors = string_of_actors.split(", ")	
			
		return list_of_actors

	def numlanguages(self):      #returns the number of languages that the movie has out of the dictionary of movie info inputted.
		list_of_languages = []
		string_of_languages = self.dict_of_movie_data['Language']
		list_of_languages = string_of_languages.split(", ")

		return len(list_of_languages)






search_terms = ["Batman Begins", "National Treasure", "Moneyball"]      #These are the movies I ran. Plug in something different and check out the results!
list_of_movies = []
for movie in search_terms:
	movie_data = OMDB(movie)

	type_movie = Movie(movie_data, movie_data['Title'], movie_data['Director'], movie_data['imdbRating'])
	list_of_movies.append(type_movie)

list_of_tweets = []
star_actorlist = []



for i in list_of_movies:    #for the leading actor in each movie, we are making a list with all the tweet info.
	star_actor = i.listactors()[0]
	star_actorlist.append(star_actor)
	star_actor_tweets = get_tweets(star_actor)
	list_of_tweets.append(star_actor_tweets)





list_of_user_info = []    #accumulating all the twitter info for the users mentioned in order to create our social network in the database.
for tweetdata in list_of_tweets:
	x = usersmentioned_info(tweetdata)
	list_of_user_info.append(x)

listofposterinfo = []          #for each of the tweets, we are getting the poster's user info and putting it all into 1 list.
for tweetdata in list_of_tweets:
	y = user_info(tweetdata)
	listofposterinfo.append(y)











conn = sqlite3.connect('final_project_206.db')    #Setting up our database
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

statement = 'INSERT INTO Movies VALUES (?, ?, ?, ?, ?, ?)'     #putting our movie info in the database

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

statement = 'INSERT OR IGNORE INTO Users_Mentioned VALUES (?, ?, ?)'    #putting in our social network info into the database

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

statement = 'INSERT OR IGNORE INTO Users VALUES (?, ?, ?)'   #putting all the posters info into our database.

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

statement  = 'INSERT OR IGNORE INTO Tweets VALUES (?, ?, ?, ?, ?, ?)'    #putting all the tweets we found into the database

for t in tweetstups:
	cur.execute(statement, t)

conn.commit()





query = "SELECT Tweets.text FROM Tweets WHERE num_retweets > 50"
tupled_more_than_50_rts = list(cur.execute(query))						#list comprehension
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
tweets_with_likes = list(filter(lambda x: x[1] > 0, tupled_list))   #filter used

print("-------------------")				#Got all the tweets that got likes and how many they got
print("-------------------")
print("Here are all the tweets that actually got some likes...and how many likes they got:")
print(tweets_with_likes)



query = "SELECT Users_Mentioned.user, Users_Mentioned.num_favs_by_user FROM Users_Mentioned"
tupled_mentioned = list(cur.execute(query))
users_mentioned_filtered = {}    #accumulating dictionary
for i in tupled_mentioned:
	if i[1] > 10000:
		users_mentioned_filtered[i[0]] = i[1]


print("-------------------")          #From the users mentioned, we got all the active users based on if they favorited more than 10,000 times.
print("-------------------")
print("Here are the active twitter users amongst the users mentioned based off how much they favorite (greater than 10,000!):")
print(users_mentioned_filtered)

print("-------------------")
print("-------------------")






#Everything below is for writing our findings into a text file so that it is clear and easy to read for the user!


text_file = "Check_Out_The_Results.txt"    #defining our .txt file
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
	textfile.write(i.__str__())    #calling the __str__() function for us to get the basic information about the movies we inputted.
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

# Write your test cases here. Here are all of our test cases - at least 1 per method.

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
		self.assertTrue(type(get_tweets('Tom Cruise')), type({"hi","bye"}))   #testing to see if the returned value of get_tweets() is of type dictionary.

	def test_get_tweets2(self):
		self.assertTrue(len(get_tweets('Nicolas Cage')['statuses']) > 1)   #testing if the twitter information is processed correctly and that list inside 'statuses' has adequate information that we will be pulling for our tweet table.

	def test_user_info1(self):
		self.assertTrue(type(user_info(get_tweets('Will Smith'))), type({"hello", "goodbye"}))   #testing to see if the user_info function returns a type dictionary.

	def test_usersmentioned_info(self):
		self.assertTrue(type(usersmentioned_info(get_tweets('Christian Bale'))), type({"hi", "bye"}))  #testing to see if usersmentioned_info() returns a dictionary with all the info of the users mentioned in the tweets.

	def test_OMDB(self):
		self.assertTrue(type(OMDB('King Kong')['Title']), type('string please'))  #tests to see if we successfully return a dictionary of the movie's info by checking the type of the title which should be type string.

	def test_OMDB2(self):
		self.assertTrue(OMDB('21')['Title'], '21')  #testing to see if we got the right movie information by checking to see if the title in the dictionary matches our query. Supplemental to test_OMDB().



class MovieClassMethodsTests(unittest.TestCase):

	
	def test_constructor(self):
		moviedata = OMDB('Finding Nemo')
		tester_movie = Movie(moviedata, moviedata['Title'], moviedata['Director'], moviedata['imdbRating'])
		self.assertTrue(type(tester_movie.title), type('This should be a string'))    #testing the constructor with the instance variable, checking to see if the title of the movie is of type string.


	def test_str(self):
		moviedata = OMDB('Finding Nemo')
		tester_movie = Movie(moviedata, moviedata['Title'], moviedata['Director'], moviedata['imdbRating'])
		self.assertTrue(type(tester_movie.__str__()), type('This should be a string too!'))   #checking to see if the __str__() method returns a string keeping in mind that this output is for users.

	def test_listactors(self):
		moviedata = OMDB('Finding Nemo')
		tester_movie = Movie(moviedata, moviedata['Title'], moviedata['Director'], moviedata['imdbRating'])
		self.assertTrue(type(tester_movie.listactors()), type([]))      #checking to see if the listactors() function actually returns a list of the actors for the movie that it was called on. 

	def test_numlanguages(self):
		moviedata = OMDB('Finding Nemo')
		tester_movie = Movie(moviedata, moviedata['Title'], moviedata['Director'], moviedata['imdbRating'])
		self.assertTrue(type(tester_movie.numlanguages()), type(1))    #testing to see if a number is returned for the numlanguages() function where we should get the number of languages that are in that movie.







## Remember to invoke all your tests....

if __name__ == "__main__":
	unittest.main(verbosity = 2)
import json
from typing import Collection
import unittest
import os
import requests

#
# Your name: Luis Solano
# Who you worked with:
#
# generating personal API key is not requested here

def read_cache(CACHE_FNAME):
    """
    This function reads from the JSON cache file and returns a dictionary from the cache data.
    If the file doesn’t exist, it returns an empty dictionary.
    """
    try:
        cache_file = open(CACHE_FNAME, 'r', encoding="utf-8") # Try to read the data from the file
        cache_contents = cache_file.read()  # If it's there, get it into a string
        CACHE_DICTION = json.loads(cache_contents) # And then load it into a dictionary (takes JSON string and returns python dictionary or list)
        cache_file.close() # Close the file, we're good, we got the data in a dictionary.
        print(CACHE_DICTION)
        return CACHE_DICTION
        
    except:
        CACHE_DICTION = {}
        return CACHE_DICTION

def write_cache(CACHE_FNAME, CACHE_DICT):
    """
    This function encodes the cache dictionary (CACHE_DICT) into JSON format and
    writes the JSON to the cache file (CACHE_FNAME) to save the search results.
    When you write cache into JSON format, you need to unpack the second item of your dictionary, which is 
    the actual content of your item. For example: 

    {'resultCount': 2, 'results': [{*INFORMATION ABOUT EACH ITEM*},{*INFORMATION ABOUT EACH ITEM*}]}

    In the above case, the resultCount is 2 because we set the limit number to be 2. For this assignment, we set resultCount to be 1. 

    """
    #source = os.path.dirname(__file__) # needed? following lecture example
    #full_path = os.path.join(source, 'com.json') # needed? following lecture ex
    #cache_file = open(full_path, "w", encoding="utf-8") 
    
    cache_file = open(CACHE_FNAME, "w") 
    #json.dumps(obj) takes python dict or string and returns JSON string
    cache_dump = json.dumps(CACHE_DICT)
    #what does "unpack" mean?
    cache_file.write(cache_dump)

    cache_file.close()
    
    


def create_request_url(term, number=1):
    """
    This function prepares and returns the request url for the API call.  
    The documentation of the API parameters is at  
    https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/

    See more details in the instructions file.

    """
    request = "https://itunes.apple.com/search?"
    attach_1 = "term=" 
    original_term = term
    list_term = original_term.split()
    new_term = '+'.join(list_term)
    final_term = attach_1 + new_term # make sure it looks right 
    
    return request + final_term + "&limit=1"
    
def get_data_with_caching(term, CACHE_FNAME):
    """
    This function uses the passed term (e.g., Billie+Eilish) to first generate a request_url (using the create_request_url function).
    It then checks if this url is in the dictionary returned by the function read_cache.
    If the request_url exists as a key in the dictionary, it should print "Using cache for <term>"
    and return the results for that request_url.

    If the request_url does not exist in the dictionary, the function should print "Fetching data for <term>"
    and make a call to the Search API to get the data for that specific term.

    If data is found for the term, it should add them to a dictionary (key is the request_url, and value is part of the results)
    and write out the dictionary to a file using write_cache.

    If the request_url is not generated correctly (e.g., for some reason the limit number is not 1) and thus returns zero or multiple items, 
    do not write this data into the cache file. Instead, print “Request not set correctly” and return None.

    If there was an exception during the search (for reasons such as no network connection, no results are returned), 
    it should print out “Exception” and return None.
    """
    #use create_request function to generate reguest URL
    generated_url = create_request_url(term) 
    dictionary = read_cache(CACHE_FNAME)
    #check if URL is in dictionary using read_cache 
    #CACHE_DICTION = {}
    
    #if read_cache(CACHE_FNAME) != CACHE_DICTION:
    if generated_url in dictionary: #checks if URL is in dictionary 
        print("Using cache for " + term) # how does term print out?? 
        return dictionary[generated_url] #return results for that request URL??    
    else:
        
        print("Fetching data for " + term) 
            #make call to the Search API to get data for that term- You should 
            #be using the create_request_url function and also implementing the
        try:    
            #requests module with that URL. (request.get()?)
            data = requests.get(generated_url)
           
            #If data is found for the term/ check key value in dict
            data_in_dictionary = json.loads(data.text) # this returns a dictionary
            #print(data_in_dictionary) 
            if data_in_dictionary['resultCount'] == 1:
                dictionary[generated_url] = data_in_dictionary['results'][0]
                #and write out dictionary to file using write_cache
                write_cache(CACHE_FNAME, dictionary)
                return dictionary[generated_url]
                #Return the cache dictionary at the request url
        
            #If the request_url is not generated correctly -> do not write this data into the cache file
            else:  
                print("Request not set correctly")
                return None

        except: #If there was an exception -> print out “Exception” and return None
            print("Exception")
            return None


def sort_collectionid (CACHE_FNAME):
    """
     This function sorts a list of items based on collectionId in ascending order and 
     returns the collection price for the item with the smallest collectionId.

    """
    #read_cache(CACHE_FNAME) #we get a cache dictionary

    #The function should grab the collection 
    #id and collection price from each request URL and then sort it by 
    # the collection id
    #sorted_list = sorted(list, ) 
    #smallest = sorted_list[0]
    #return smallest


    #use read_cache() to get a cache dictionary
    '''
    The function takes in a file as the parameter. It then should 
    read in that file (which should consist of a dictionary). The
    function should grab the collection id and collection price 
    from each request URL and then sort it by the collection id. 
    The function should return the price of the smallest collection id.
    '''

    cache_file_dictionary = read_cache(CACHE_FNAME) #It then should read in that file (which should consist of a dictionary) 
    id_price_dictionary = {} #dict for id:price
    sorted_id_ascending = {} #dict for sorted values
    for key in cache_file_dictionary: #to get each id and price per URL
        id_value = cache_file_dictionary[key]["collectionId"] #getting collection id value
        price_value = cache_file_dictionary[key]["collectionPrice"] #getting collection price value

        id_price_dictionary[id_value] = price_value #prepare dict with id as key and price as value
        
        id_price_holder = id_price_dictionary.items()
        sorted_id_ascending = sorted(id_price_holder) #sorting       
        
    return sorted_id_ascending[0][1] #should return the price of the smallest collection id


#######################################
############ EXTRA CREDIT #############
#######################################
def itunes_list():
    """
    The function calls read_cache() to get the iTunes data stored in extra_credit.json. 
    It analyzes the dictionary returned by read_cache(). 
    This function returns a tuple with two items: the first is a new dictionary with the primaryGenreName as the key and number of items with that genre as the value; 
    the second is the genre name with most items. 

    Expected results should be: 
    ({'Electronic': 1, 'Pop': 6, 'Hip-Hop/Rap': 1, 'Rock': 2, 'Alternative': 3, 'Country': 1, 'Drama': 1, 'Hip-Hop': 1, 'Biographies & Memoirs': 1, 'Dance': 1}, “Pop”)

    """
    





#######################################
#### DO NOT CHANGE AFTER THIS LINE ####
#######################################

class TestHomework6(unittest.TestCase):
    def setUp(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.CACHE_FNAME = dir_path + '/' + "cache_itunes.json"
        self.term_list = ["olivia+rodrigo", "ariana+grande", "drake", "tame+impala", "selena+gomez", "bruno+mars", "calvin+harris", "lorde", "imagine+dragons", "taylor+swift", "justin+bieber", "adele", "cage+the+elephant", "kanye+west", "britney+spears", "annavento", "ericayan"]
        self.cache = read_cache(self.CACHE_FNAME)

    def test_write_cache(self):
        write_cache(self.CACHE_FNAME, self.cache)
        dict1 = read_cache(self.CACHE_FNAME)
        self.assertEqual(dict1, self.cache)

    def test_create_request_url(self):
        for m in self.term_list:
            self.assertIn("term={}".format(m),create_request_url(m))
            self.assertIn("limit=1",create_request_url(m))
            self.assertNotIn("r=json",create_request_url(m))
            

    def test_get_data_with_caching(self):
        for m in self.term_list:
            dict_returned = get_data_with_caching(m, self.CACHE_FNAME)
            if dict_returned:
                self.assertEqual(type(dict_returned), type({}))
                self.assertIn(create_request_url(m),read_cache(self.CACHE_FNAME))
            else:
                self.assertIsNone(dict_returned)       
        self.assertEqual(json.loads(requests.get(create_request_url(self.term_list[0])).text)["results"][0],read_cache(self.CACHE_FNAME)[create_request_url(self.term_list[0])])

    def test_sort_collectionid(self):
        self.assertEqual(sort_collectionid(self.CACHE_FNAME), 3.99)
        


    ######## EXTRA CREDIT #########
    # Keep this commented out if you do not attempt the extra credit
    # Writing test case for the extra credit is not required but highly recommended.
    def test_itunes_list(self):
        pass 



def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    CACHE_FNAME = dir_path + '/' + "cache_itunes.json"

    terms = ["olivia+rodrigo", "ariana+grande", "drake", "tame+impala", "selena+gomez", "bruno+mars", "calvin+harris", "lorde", "imagine+dragons", "taylor+swift", "justin+bieber", "adele", "cage+the+elephant", "kanye+west", "britney+spears", "annavento", "ericayan"]
    [get_data_with_caching(term, CACHE_FNAME) for term in terms]
    print("________________________")
    # Fetch the data for ColdPlay!
    # The data should be requested from the API if this is the first time you are running the program
    # or if you haven't deleted the cache!
    data1 = get_data_with_caching('cold+play', CACHE_FNAME)
    data2 = get_data_with_caching('cold+play', CACHE_FNAME)
    print("________________________")

    # Getting the data for Post Malone!
    # The data should be requested from the API if this is the first time you are running the program
    # or if you haven't deleted the cache!
    data1 = get_data_with_caching('post+malone', CACHE_FNAME)
    data2 = get_data_with_caching('post+malone', CACHE_FNAME)
    print("________________________")

    # Getting the data for The Beatles
    # The data should be requested from the API if this is the first time you are running the program
    # or if you haven't deleted the cache!
    data1 = get_data_with_caching('the+beatles', CACHE_FNAME)
    data2 = get_data_with_caching('the+beatles', CACHE_FNAME)
    print("________________________")

    print("Get CollectionPrice for first 5 items")
    print(sort_collectionid(CACHE_FNAME))
    print("________________________")


    # Extra Credit
    # Keep the statements commented out if you do not attempt the extra credit
    print("EXTRA CREDIT!")
    print("Analyzing the distribution of item genres")
    # itunes_list() function does not take any parameters.
    print(itunes_list())
    print("________________________")
    
 
if __name__ == "__main__":
    main()
    # You can comment this out to test with just the main function,
    # But be sure to uncomment it and test that you pass the unittests before you submit!
    unittest.main(verbosity=2)

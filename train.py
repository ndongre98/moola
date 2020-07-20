import requests
from bs4 import BeautifulSoup
import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, KeywordsOptions
from datetime import datetime as dt
import numpy as np

from dotenv import load_dotenv
load_dotenv()
import os
api_key = os.environ.get("ALCHEMY_API_KEY")
api_url = os.environ.get("NLP_SERVICE_URL")

def get_search_results(url):
	r1 = requests.get(url)
	soup = BeautifulSoup(r1.content, 'html5lib')
	search_results = []
	for a in soup.select('.results dt a'):
		search_results.append(a["href"])
	return search_results

def compile_urls(query):
	urls = []
	for i in range(1,2):
		base = "https://www.fool.com/search/solr.aspx?dataSource=article&page={}&q={}&scope=all&sort=score&source=isesitbut0000001"
		url = base.format(i, query)
		urls.extend(get_search_results(url))
	return urls

def get_avg_scores_per_entry(json_response):
	(senti, sad, joy, fear, disgust, anger) = (0, 1, 2, 3, 4, 5)
	res = [0]*6
	num = len(json_response["keywords"])
	for entry in json_response["keywords"]:
		res[senti] += entry["sentiment"]["score"]
		res[sad] += entry["emotion"]["sadness"]
		res[joy] += entry["emotion"]["joy"]
		res[fear] += entry["emotion"]["fear"]
		res[disgust] += entry["emotion"]["disgust"]
		res[anger] += entry["emotion"]["anger"]
	return [float(res[i])/num for i in range(6)]

def get_avg_scores(avg_scores_list):
	return np.mean(avg_scores_list, axis = 0)

def conv_to_json(scores, query):
	return {
		"name" : query, 
		"date" : dt.now(),
		"sentiment" : scores[0],
		"sadness" : scores[1],
		"joy" : scores[2],
		"fear" : scores[3],
		"disgust" : scores[4],
		"anger" : scores[5]
	}

def train(query):
	url_list = compile_urls(query)
	authenticator = IAMAuthenticator(api_key)
	natural_language_understanding = NaturalLanguageUnderstandingV1(
	    version='2019-07-12',
	    authenticator=authenticator
	)

	natural_language_understanding.set_service_url(api_url)

	avg_scores_list = []
	for addr in url_list:
		response = natural_language_understanding.analyze(
		    url=addr,
		    features=Features(keywords=KeywordsOptions(sentiment=True,emotion=True,limit=2))).get_result()
		avg_scores_list.append(get_avg_scores_per_entry(response))
	overall_avg_scores = get_avg_scores(np.array(avg_scores_list))
	return conv_to_json(overall_avg_scores, query)

	
	






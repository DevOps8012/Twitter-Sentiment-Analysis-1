from senti_classifier import senti_classifier

positive=0
negative=1
neutral = 2
total=3
listSpecialTag = ['#','U','@',',','E','~','$','G']


def calculateScore(tweet, polarityDictionary):
    score = {}
    for i in range(len(tweet)):
        neutralScore=0.0
        word=tweet[i].lower()
        if word in polarityDictionary:
		    posScore = polarityDictionary[word][positive]
		    negScore = polarityDictionary[word][negative]
		    neutralScore = polarityDictionary[word][neutral]
		    score[word]=[posScore, negScore, neutralScore]
        else:
		    posScore, negScore = senti_classifier.polarity_scores(list(word))
        score[word]=[posScore, negScore, neutralScore]
    return score




def findCapitalised(tweet, token, score):

    countCap = 0
    countCapPos = 0
    countCapNeg = 0
    isCapitalised = 0
    for i in range(len(tweet)):
        if token[i]!='$':
            if tweet[i].isupper():
                word=tweet[i].lower()
                countCap += 1
                if score[word][positive]!=0.0:
                    countCapPos +=1
                if score[word][negative]!=0.0:
                    countCapNeg +=1
    percentageCapitalised = 0.0
    if len(tweet)>0:
        percentageCapitalised = float(countCap)/len(tweet)
    if percentageCapitalised!=0.0:
	    isCapitalised=1
    return [ percentageCapitalised, countCapPos, countCapNeg ,isCapitalised ]




def findNegation(tweet):
	countNegation = 0
	for i in range(len(tweet)):
		if tweet[i]=='negation':
			countNegation+=1
	return [countNegation]




def findPositiveNegativeWords(tweet, token, score):
    countPos=0
    countNeg=0
    totalScore = 0
    for i in range(len(tweet)):
        if token[i] not in listSpecialTag:
            word=tweet[i].lower()
            if score[word][positive]!=0.0:
	            countPos+=1
            if score[word][negative]!=0.0:
                countNeg+=1
            totalScore += (score[word][positive] - score[word][negative])
	return [countPos, countNeg, totalScore]
	



def findEmoticons(tweet, token):
	countEmoPos = 0
	countEmoNeg =0
	countEmoExtremePos = 0
	countEmoExtremeENeg = 0

	for i in range(len(tweet)):
	    if token[i] ==  'E':
			if tweet[i] == 'Extremely-Positive':
				countEmoExtremePos+=1
			if tweet[i] == 'Extremely-Negative':
				countEmoExtremeENeg+=1
			if tweet[i] == 'Positive':
				countEmoPos+=1
			if tweet[i] == 'Negative':
				countEmoNeg+=1

	return [countEmoPos, countEmoNeg, countEmoExtremePos, countEmoExtremeENeg]




def findHashtag( tweet, token, score):
	
    countHashPos=0
    countHashNeg=0
    for i in range(len(tweet)):
        if token[i]=='#' :
            word=tweet[i].lower()
            if score[word][positive]!=0.0:
                countHashPos+=1
            if score[word][negative]!=0.0:
                countHashNeg+=1
    return [countHashPos, countHashNeg]
		

		
def countSpecialChar(tweet):
    count={'?':0,'!':0,'*':0}
    for i in range(len(tweet)):
        word=tweet[i].lower()
        if word:
            count['?']+=word.count('?')
            count['!']+=word.count('!')
            count['*']+=word.count('*')

    return [count['?'],count['!'],count['*']]




def findFeatures(tweet, token, polarityDictionary):
    """takes as input the tweet and token and returns the feature vector"""
    
    score =calculateScore(tweet, polarityDictionary)
    featureVector=[]
    featureVector.extend(findCapitalised( tweet, token, score))
    featureVector.extend(findHashtag( tweet, token, score))
    featureVector.extend(findEmoticons(tweet, token))
    featureVector.extend(findNegation(tweet))
    featureVector.extend(findPositiveNegativeWords(tweet,token, score))
    return featureVector

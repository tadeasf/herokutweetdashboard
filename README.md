#TODO
Improve sentiment analysis: After further research, vader actually seems as perfect tool for my purpose. I still can improve the accuracy in different ways, though! Getting rid of spelling mistakes. I would love to be able to do that while I'm grabbing the twitter stream and input the process before sentiment analysis. The more I get to know, the more clear it is that threading will be necessary. Anyway, once I grab the status.text I can run it first through Regular Expression module so I will get rid of repeated alphabets (caaaar, amazzzzing etc). After this is done I can use Pyspellchecker library to correct spelling of the tweets. This should increase the accuracy of my sentiment analysis greatly.

Named entity recognition: get to know other topics the users are tweeting about. Eg my topic is uyghurs in xinjiang. What they talk about the most? China? CCP? I looked more into NER. Getting some output with spacy shouldn't be much of an issue. I don't need this to be terrible thorough. Few issues I can think of that will need solving: Where to should I push the output? Inside the SQL library? For one tweet they can be multiple terms.. How to set it up? In the end, what can I use this output for? Checking most common keyword-NER pairs? Is it gonna be useful for my analysis?


Past ideas:
I would like to introduce Flair instead of Vader and stack it with ELMo. Thus, I will need to train my own Flair model, then introduce it instead of VADER into stream. I might need to introduce threading so the script can keep up. Hopefully not.

Finished:
Push my Streamlit app to a host service so I can show my data to my friends and collegues online.
I would like to push the whole process on some external service. Thinking about Collab. MySQL hosts are plenty. I really want to collect the stream 24/7.
Change stream.py def on_status so I can collect tweet ID for further retweet gathering in the future.
Changing SQL database setup and push because of that.
setup config.py so you can set up your credentials easier. I tried to do that, run into some issues and ultimately opted to skip this. I will need to learn how to use python for that, though, haha. In the future. Maybe.

# Odkazy
APP URL: https://twiterdashboardapp.herokuapp.com/
Který jsou pro mě zcela stěžejní, protože si po tomhle hackatonu nebudu pamatovat vůbec nic.  
Running scripts on Heroku!!!!!: https://www.youtube.com/watch?v=aTSw6rXmtsM
Running Python Script 24/7 for free -> Ubuntu Server on AWS E2 -> rok zdarma -> připojování přes SSH, správa souborů přes FTP. Na žádný velký pushování to není, ale je to k mýmu účelu funkční, protože se ajpin z danýho regionu nebojí AWS RDS mysql databáze, která je pro mě stěžejní. Pro nonstop run se používá teda připojení přes SSH + ubuntu bash + screen: https://www.youtube.com/watch?v=BYvKv3kM9pk
.env alternative on Heroku: https://devcenter.heroku.com/articles/config-vars
Trochu o SA: https://towardsdatascience.com/fine-grained-sentiment-analysis-in-python-part-1-2697bb111ed4
Vizualizace. Maj fajn články, ale jsou placený. Možná si to koupím: https://towardsdatascience.com/data-visualization-using-streamlit-151f4c85c79a
Další vizualizace sentimentu: https://towardsdatascience.com/building-a-sentiment-analysis-interactive-report-using-nltk-and-altair-83cb9fcb36fe
Další vizualizace: https://altair-viz.github.io/user_guide/scale_resolve.html
Ještě více vizualizací: https://docs.streamlit.io/library/api-reference/charts/st.altair_chart
Kurňa, myslel jsem, že mě ty fucking grafíky přivedou do hrobu.
Tenhle graf jsem třeba nezprovoznil a histogram s linkou by bejval na dashboardu byl fakt hezu -> https://seaborn.pydata.org/tutorial/distributions.html
co už
Jiný vizualizace -> https://predictivehacks.com/how-to-run-sentiment-analysis-in-python-using-vader/
Poslední vizualizace -> https://itnext.io/basics-of-text-analysis-visualization-1978de48af47

## Deprecated odkazy
https://developer.twitter.com/en/docs/twitter-api/metrics
https://developer.twitter.com/en/docs/twitter-api/annotations/overview - NER?
https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/tweet
https://developer.twitter.com/en/docs/twitter-api/expansions
https://developer.twitter.com/en/docs/twitter-api/fields
https://stackoverflow.com/questions/13928155/spell-checker-for-python
https://blog.quantinsti.com/vader-sentiment/

## Deprecated shoutout
Yes, this script is super heavily inspired by https://github.com/jonathanreadshaw/streamlit-twitter-stream so shout out is due and here it goes.
It didn't work for me properly from the get go and neither it did for other git users. I made necessary changes to get rid of errors so it should be pretty easy to set up for any of you now.

Also, it broke connection frequently, so I introduced some code to combat that. It seems stable now.

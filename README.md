# FULLY AUTOMATED TWITTER STREAMLISTENER
Oh well, it sounds nice. -> hit me with an issue if you're not sure how it works. I am too tired to do english right now. Will update this readme later.
# CO TO JE?
Vážení, prezentuju vám v týhle repo výsledek mýho osobního neplánovanýho téměř 40 hodinovýho hackatonu aka Tadeáš se učí s pythonem. Každej jsme nějakej, že jo.
Někteří budou rozumět, jiní ne. Můžete to komentovat. Můžete se ptát. Můžete si ze mě i utahovat!
Ale teď už teda k věci: vo co jde a co to umí?
Python má šikovnou knihovnu - tweepy. Ta umí "poslouchat" stream novejch tweetů a tahat z něj data podle různejch kritérií. To je skvělý a vokolo toho se celej tenhle projekt teď točí.  

Víceméně jsem nastavil sadu skriptů tak, aby mi sbírala důležité informace z tweetů o Ujgurech. Takový tý utlačovaný muslimský menšině. Má v tom prsty Čína a tak.
Na tweetech je skvělý to, že bejvaj plný emocí. Python toho umí využít a má přednaučenej model vaderSentiment, kterej umí relativně velmi dobře rozpoznat, jestli chtěl tweetující sdělit něco hezkého nebo ošklivého.

Jenže teď má můj skript plnou paměť dobře zpracovanejch dat, ale nemá je kam dát. Pushovat je do jsonu, csvčka nebo něčeho podobnýho? Meh, to by bylo peklo. Chci, aby tahle věc běžela 24/7 a byla neustále aktuální.

Jak na to? 

Skript automaticky dumpuje každej tweet do SQL databáze (schématu) ve kterým si z ničeho umí vytvořit pro něj adekvátní tabulku. Je prostě šikovnej.
Na začátku jsem tenhle setup jel samozřejmě lokálně, ale nedalo mi to, fakt jsem chtěl, aby to běželo pořád. A tam začlo peklo.
Připojovat se přes python skript z externí služby na SQL servr je dost problematický. Whitelistovat IP poskytavatele serverovejch služeb si říká vo průšvih.
No, po několika hodinách zkoušení různejch věcí (dokonce jsem zkoušel zneužít i webhosting otcovo firmy od wedosu) jsem se dobral výsledku: aws RDS + jejich EC2 instance. 
Tyhle dvě služby si spolu rozumí. Aby toho nebylo málo, tak je Bezos prostě cool týpek a prvotní setup služeb s balíčkama mini je na rok zadarmo. Tweetů o ujgurech bude mít amerika uloženejch hodně. Ou jé.

Inu, jo, takže core proces, kterej jsem s datama z twitteru chtěl zatím provádět probíhal. Ale jak se jako mám pochlubit? A kontrolovat, že přibejvaj tweety do databáze přes mysql workbench asi taky není úplně ideální, že jo.

Proto se stal Dashboard, kterej tady taky vidíte. Vizualizace týhle mojí dřiny, potu (někteří víte, jak chodím oblíkanej doma) a intelektuálního vypětí.
Co v něm můžete vidět?

Nejčerstvější tweety, jaký klíčový slova sbírám a kolik kterejch je. Poměrově. Koláč nemohl chybět a čárky su taky fajne.
Ty další dva grafy rád vysvětlím komukoliv, kdo se o to bude zajímat. Už mě bolej ruce, fakt.

Jakýkoliv připomínky uvítám. Kdo máte github, hoďte je i klidně do issues. A lokálně to rozjet taky není nutně problém, nastavil jsem skrz config a .env docela jednoduchej workflow pro změnu uživatelskejch údajů. Navíc mě heroku donutilo (to je zas služba, která mi zdarma jede skript s Dashboardem, kterej IRL aktualizuje grafíky, ňam), abych řádně aktualizoval requirements.txt. Takže jo, stačí rozjet další environ a můžete si to zkusit taky. Budu rád.

# WHAT'S NEXT?!
Improve sentiment analysis: After further research, vader's library actually looks like a perfect tool for what I intend to do with this project. I will be able to improve sentiment analysis accuracy in many different ways without getting rid of what seems like a hard-to-beat library for social media.
How can I improve?
First of all, I want to get rid of spelling mistakes. I would love to be able to do that while I'm grabbing tweets from the stream and put the process before sentiment analysis itself. 
The more I get to know, the more it seems that threading is going to be necessary. Anyway, once I grab the status.text I can run it first through Regular Expression module so I will get rid of repeated alphabets (caaaar, amazzzzing etc). After this is done I can use Pyspellchecker library to correct spelling of the tweets. This should increase the accuracy of my sentiment analysis greatly.

Named entity recognition: get to know other topics the users are tweeting about. Eg my topic is uyghurs in xinjiang. What they talk about the most? China? CCP? I looked more into NER. Getting some output with spacy shouldn't be much of an issue. I don't need this to be terrible thorough. Few issues I can think of that will need solving: Where to should I push the output? Inside the SQL library? For one tweet they can be multiple terms.. How to set it up? In the end, what can I use this output for? Checking most common keyword-NER pairs? Is it gonna be useful for my analysis? - also it looks like this is implemented by Twitter itself to some extent. I have to do more research. Consult: https://developer.twitter.com/en/docs/twitter-api/annotations/overview

Finished:
Push my Streamlit app to a host service so I can show my data to my friends and collegues online and flex my brain muscles.
I would like to push the whole process on some external service. I really want to collect the stream 24/7. This was harder then expected.
Change stream.py def on_status so I can collect tweet ID for further retweet gathering in the future. -> + much more
Changing SQL database setup and push because of that. -> easy
setup config.py so you can set up your credentials easier. I tried to do that, run into some issues and ultimately opted to skip this. I will need to learn how to use python for that, though, haha. In the future. Maybe. -> done. also created external environment on Heroku where I can store my keys and database initials. In the future I'd like to implement this into my workflow: https://github.com/simoneb/ghenv 

Deprecated ideas:
I would like to introduce Flair instead of Vader and stack it with ELMo. Thus, I will need to train my own Flair model, then introduce it instead of VADER into stream. I might need to introduce threading so the script can keep up. Hopefully not. -> hahaha, I was so naive!

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

Also, it broke connection frequently, so I introduced some code to combat that. It seems stable now. And it actually is. Running 15ish hours on remote ex2 ubuntu server.

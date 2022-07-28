# Dokumentace ke sběru tweetů

Celý repozitář tvoří několik skriptů, které nabízí uživateli dvě možnosti, jakým způsobem sbírat tweety:

## sběr nových tweetů (zadarmo, bez limitu)

- o první možnost se starají skripty stream.py a run_stream.py
- sběr tweetů se spustí pomocí příkazu "python3 run_stream.py -k "klíčové slovo"
- ve skriptu stream.py definujeme funkci StreamListener. během sběru rovnou provádíme čištění textu, odstraňujeme retweety a provádíme i sentiment analýzu. možností do budoucna je využití balíčku HateSonar, jež umí rozpoznávat v textu hate speech, případně offensive speech

## hledání v archivu (je nutné zažádat o akademické API od Twitteru)

- <https://github.com/tadeasf/twitter_crawler_academic.git>
- dva jednoduché skripty nám umožní autentifikovat se vůči twitteru a následně využívat volání APIv2
- obrovské možnosti filtrace, vyhledávání v jakémkoliv časovém horizontu, limit 10mil tweetů/měsíc
- je možné vyhledávat podle klíčového slova, uživatele, stahovat profily atp.
- po zavolání na API můžeme data uložit jako soubor ve formátu JSON nebo je vložit do noSQL databáze mongo
- v tomto případě jsme data vkládali do MongoDB
- to nám umožnilo využít skvělého nástroje - mongo agregace - skrze kterou můžeme dopočítat sumy lajků, interakcí, definovat jednoduše datatypy, kombinovat jednotlivé hodnoty atp.
- z mongoDB pak pomocí balíčku mongoexport exportujeme data do csv souboru
- z něj je můžeme jednoduše pomocí příkazové řádky vložit do námi preferované SQL databáze, v našem případě jde o MariaDB
- nadefinujeme v rámci DPP datatypy a tabulka je hotová

### sentiment analýza

- v případě prohledávání archivu by byla implementace čištění textu a sentiment analýzy velmi komplikovaná
- k tomu slouží dodatečně skript vaderSentimentAnalyser.py, pomocí nějž sentiment analýzu provádíme

## Tweety máme nasbírané, co teď?

- tweety máme uložené v databázi, nejtěžší část je za námi
- databázi můžeme spojit s velkým množství analytických nástrojů, řada z nich je pro studenty volně dostupná
- např. Tableau
- v našem případě jsme zvolili nástroj Google Data Studio, ke kterému jsme připojili databázi a následně již jen "naklikali" grafy
- další možností, jež jsme využili pro kvantitativní analýzu textu, je opět využití pythonu
- existuje několik balíčků, které nám usnadňují stavění dashboardů - např. Dash, my využili Streamlit
- python se umí připojit k databázi pomocí balíčku SQLalchemy, tím dostaneme data tam, kam potřebujeme
- pak jde hlavně o práci s balíčkem pandas, pomocí kterého připravujeme data pro grafy
- další možností by bylo využít addonů pro google sheets a z nich vytvořit opět pipeline do google data studia

# Dávid Penťa - Údaje o futbalových hráčoch z hry FIFA22
Jazyk - Python
Zdroj dát - FIFA Index - https://www.fifaindex.com a enwiki-latest-pages-articles.xml.bz2 z https://dumps.wikimedia.org/enwiki/latest/

Projekt sa sústreďuje na analýzu vrcholových futbalových hráčov z celého sveta s cieľom poskytnúť nástroj, ktorý umožní skúmanie vplyvu miesta narodenia na ich fyzické a technické schopnosti. Hypotézou je, že geografické a kultúrne faktory, ako aj podmienky výchovy a tréningu v rôznych regiónoch, môžu mať zásadný dopad na rozvoj futbalistov. Projekt využíva dáta z hry FIFA22, konkrétne z edície, ktorá bola poslednou verziou dostupnou na stránke FIFA Index, ktorá o hráčoch poskytovala kompletné informácie. Táto hra poskytuje štatistiky o hráčoch ako napríklad ich výšku, váhu, rýchlosť, ovládanie lopty, presnosť prihrávania. Tieto údaje sú doplnené o informácie z článkov Wikipédie o miesta narodenia futbalistov. Spojením týchto dvoch zdrojov dát projekt umožňuje používateľom vyhodnotiť, či sú futbalisti z určitých krajín alebo regiónov v priemere rýchlejší, vyšší, ťažší alebo technicky zručnejší. Získané údaje môžu byť následne použité na identifikáciu trendov a vzorcov, ktoré by mohli byť užitočné pre trénerov, hráčov, analytikov a nadšencov, aby lepšie porozumeli a využívali geografické a kultúrne rozdiely vo futbale.

Nenašiel som žiadny nástroj, ktorý by takúto funkciu umožnoval. Jedine na wikipédii som našiel články ako napríklad https://en.wikipedia.org/wiki/Category:Footballers_by_city_or_town_in_England, v ktorom je zoznam fudbalistov z anglicka rozdelených poďla mesta, v ktorom sa narodili. Takýto zoznam ale neumožňuje robiť analýzu o hráčoch.

V projekte využívam štyri pythonovské súbory s názvami crawler.py, wiki_extractor.py, data_merger.py a search.py. Dáta sú ukladané do súborov s názvami output_crawler.tsv, output_wiki.tsv a merged_data.tsv.

Crawl stránky https://www.fifaindex.com sa vykoná v súbore crawler.py. Zároveň s crawlovaním dát sa vykonáva aj ich parsing, extrakcia a uloženie do súboru output_crawler.tsv. Presný link na každého hráča z hry FIFA22 je zo sidemapy https://www.fifaindex.com/sitemap-fifa22-players.xml

V súbore wiki_extractor.py sa spracováva dump z anglickej wikipédie a to presne zo súboru enwiki-latest-pages-articles.xml.bz2. Extrahujú sa tam pomocou sparku tie články Wikipédie, ktoré obsahujú slovo football a zároveň miesto narodenia a neobsahujú dátum úmrtia. Pre články, ktoré spĺňajú tieto kritériá, je do súboru output_wiki.tsv uložený ich názov článku a meno, miesto a dátum narodenia z tabuľky na wikipédii.

Následne sa dáta zo súborov output_crawler.tsv a output_wiki.tsv spolu spoja v data_merger.py. Dáta z crawlera sa spájajú podľa mena hráča s dátami z Wikipédie. Ak však pre nejaké meno neexistuje presná zhoda s menom z Wikipédie, tak sa nájde pomocou funkcie get_close_matches z knižnice difflib. Ak je zhoda aspoň 70% a zároveň sú zhodné roky narodenia, tak sa dáta spoja. Vďaka tomuto sa napríklad spoja údaje o hráčovi, ktorý má na stánke FIFA Index meno Neymar Jr. a na Wikipédii len Neymar. V spojených dátach sú vyšistené údaje o mieste narodenia potom sú tieto dáta uložené do súboru merged_data.tsv.

Posledný súbor search.py obsahuje CLI aplikáciu, v ktorej je možné zvoliť indexáciu súboru merged_data.tsv, spustiť testy a vyhľadávať v ňom podľa mena, miesta narodenia a popisu hráčov.


Názvy stĺpcov v tsv súboroch:

output_crawler.tsv - id, name, short_description, description, overall, potential, height, weight, preferred_foot, birth_date, age, preferred_positions, teams, traits week_foot_rating, skill_moves_rating, ball_control, dribbling, marking, slide_tackle, stand_tackle, aggression, reactions, attack_position, interceptions, vision, crossing, short_pass, long_pass, acceleration, stamina, strength, balance, sprint_speed, agility, jumping, heading, shot_power, finishing, long_shots, curve, fk_accuracy, penalties, volleys, gk_positioning, gk_diving, gk_handling, gk_kicking, gk_reflexes

output_wiki.tsv - title, name, birth_place, birth_date

merged_data.tsv - id, name, short_description, description, overall, potential, height, weight, preferred_foot, birth_date, age, preferred_positions, teams, traits week_foot_rating, skill_moves_rating, ball_control, dribbling, marking, slide_tackle, stand_tackle, aggression, reactions, attack_position, interceptions, vision, crossing, short_pass, long_pass, acceleration, stamina, strength, balance, sprint_speed, agility, jumping, heading, shot_power, finishing, long_shots, curve, fk_accuracy, penalties, volleys, gk_positioning, gk_diving, gk_handling, gk_kicking, gk_reflexes, birth_place

Počet záznamov v tsv súboroch:
output_crawler.tsv - 17431
output_wiki.tsv - 156502
merged_data.tsv - 11846 - 67.96% záznamov z output_crawler.tsv

To, že sa mi podarilo z Wikipédie získať miesta narodenia o 67.96% hráčoch z hry FIFA22 beriem ako úspech, pretože veľa menej známych hráčov nemá o sebe článok na Wikipédii. Spájanie hráčov aj s článkom, ktorý nemal presne rovnaké meno, výrazne zvýšilo počet spojených záznamov, pretože veľakrát sa líšila diakritika v mene hráča. Tiež bol výrazný problém, že na stránke FIFA Index boli častokrát zmenené mená hráčov tak, že ich nebolo možné správne identifikovať. Neviem prečo sa tam takéto chyby vyskytovali, ale zistil som to až v pokročilej fáze projektu, tak som zdroj dát už nemenil. Napríklad hráč Milan Škriniar tam má meno Milan Regalado.

Jednotkové testy ukázali, že vyhľadávanie nie je presné pokiaľ ide o viacslovný hľadaný výraz. Napríklad pri hľadaní výrazu Žiar nad Hronom našlo aj hráčov, ktorí sa narodili v obciach ako: Dubnica nad Váhom, Rychnov nad Kněžnou, Bánovce nad Bebravou a Kostrzyn nad Odrą.

Na spustenie súboru wiki_extractor.py je potrebné mať na systéme nainštalovaný Spark a na spustenie súboru search.py je potrebné mať na systéme nainštalovaný pylucine, čo som osobne riešil pomocou dockera. Ostatné knižnice je možné nainštalovať jednoducho pomocou pip.

Ukážka CLI aplikácie:
```
————————————————————-
Create index? 1 - yes, 2 - no
Enter your choice: 1
Run unit tests? 1 - yes, 2 - no
Enter your choice: 1
————————————————————-
Search field: birth_place
Test query: Bratislava
Expected names: ['Lukáš Haraslín', 'Ivan Schranz', 'Dominik Greif', 'Róbert Mak', 'Branislav Niňaj']
Result names: ['Lukáš Haraslín', 'Ivan Schranz', 'Dominik Greif', 'Róbert Mak', 'Branislav Niňaj']
True positives: 5
True negatives: 11842
False positives: 0
False negatives: 0
Accuracy: 1.0
Precision: 1.0
Recall: 1.0
————————————————————-
Search field: birth_place
Test query: Košice
Expected names: ['Marek Rodák', 'Alex Král', 'Jakub Hromada', 'Tomáš Huk', 'Filip Lesniak']
Result names: ['Marek Rodák', 'Alex Král', 'Jakub Hromada', 'Tomáš Huk', 'Filip Lesniak']
True positives: 5
True negatives: 11842
False positives: 0
False negatives: 0
Accuracy: 1.0
Precision: 1.0
Recall: 1.0
————————————————————-
Search field: birth_place
Test query: Trenčín
Expected names: ['Stanislav Lobotka', 'Jakub Holúbek', 'Peter Pokorný']
Result names: ['Stanislav Lobotka', 'Jakub Holúbek', 'Peter Pokorný']
True positives: 3
True negatives: 11844
False positives: 0
False negatives: 0
Accuracy: 1.0
Precision: 1.0
Recall: 1.0
————————————————————-
Search field: birth_place
Test query: Prievidza
Expected names: ['Dávid Hancko']
Result names: ['Dávid Hancko']
True positives: 1
True negatives: 11846
False positives: 0
False negatives: 0
Accuracy: 1.0
Precision: 1.0
Recall: 1.0
————————————————————-
Search field: birth_place
Test query: Žiar nad Hronom
Expected names: ['Milan Škriniar']
Result names: ['Martin Valjent', 'Tomáš Petrášek', 'Roman Gergel', 'Tomáš Holý', 'Kacper Michu']
True positives: 0
True negatives: 11841
False positives: 5
False negatives: 1
Accuracy: 0.9994935426690301
Precision: 0.0
Recall: 0.0
————————————————————-
Total test cases: 5
Total True Positives: 14
Total True Negatives: 59215
Total False Positives: 5
Total False Negatives: 1
Total accuracy: 0.999898708533806
Total precision: 0.7368421052631579
Total recall: 0.9333333333333333
————————————————————-
Enter 0 to exit
Where search? 1 - Name, 2 - Birth place, 3 - Description
Enter your choice: 1
————————————————————-
Enter search query: Messi
Lionel Messi, 92, Rosario, Santa Fe, Argentina, Paris Saint-Germain, Argentina
————————————————————-
Enter 0 to exit
Where search? 1 - Name, 2 - Birth place, 3 - Description
Enter your choice: 2
————————————————————-
Enter search query: Bratislava
Found 5 document(s) that matched query 'Bratislava':
————————————————————-
1 - Print stats, 2 - Print players
Enter your choice: 1
Overall avg: 71.6
Potential avg: 73.8
Height avg: 186.8
Weight avg: 77.8
Preferred foot: 
Right - 100.0%
Left - 0.0%
Age avg: 27.6
Week foot rating avg: 3.4
Skill moves rating avg: 2.4
Ball control avg: 56.6
Dribbling avg: 55.6
Marking avg: 34.8
Slide tackle avg: 37.2
Stand tackle avg: 38.0
Aggression avg: 52.0
Reactions avg: 65.8
Attack position avg: 51.6
Interceptions avg: 42.2
Vision avg: 58.6
Crossing avg: 53.4
Short pass avg: 57.2
Long pass avg: 52.2
Acceleration avg: 59.0
Stamina avg: 57.8
Strength avg: 68.6
Balance avg: 57.6
Sprint speed avg: 61.2
Agility avg: 59.4
Jumping avg: 58.2
Heading avg: 53.8
Shot power avg: 63.8
Finishing avg: 48.6
Long shots avg: 48.4
Curve avg: 49.0
Fk accuracy avg: 44.0
Penalties avg: 47.0
Volleys avg: 47.0
Gk positioning avg: 23.8
Gk diving avg: 22.6
Gk handling avg: 22.6
Gk kicking avg: 22.6
————————————————————-
Enter 0 to exit
Where search? 1 - Name, 2 - Birth place, 3 - Description
Enter your choice: 2
————————————————————-
Enter search query: Bratislava
Found 5 document(s) that matched query 'Bratislava':
————————————————————-
1 - Print stats, 2 - Print players
Enter your choice: 2
Lukáš Haraslín 76 Bratislava, Slovakia Sparta Praha
Ivan Schranz 74 Bratislava, Slovakia Slavia Praha
Dominik Greif 72 Bratislava, Slovakia RCD Mallorca
Róbert Mak 70 Bratislava, Czechoslovakia Ferencvárosi TC
Branislav Niňaj 66 Bratislava, Slovakia Sepsi OSK
————————————————————-
Enter 0 to exit
Where search? 1 - Name, 2 - Birth place, 3 - Description
Enter your choice: 0

Process finished with exit code 0
```

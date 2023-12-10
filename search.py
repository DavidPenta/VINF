import lucene

from java.nio.file import Paths
from org.apache.lucene.store import MMapDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import IndexWriterConfig, IndexWriter, IndexOptions, DirectoryReader
from org.apache.lucene.document import Document, FieldType, Field, TextField
from org.apache.lucene.queryparser.classic import QueryParser


def read_file(index):
    file_name = 'merged_data.tsv'
    file = open(file_name, 'r', encoding='utf-8')
    file.readline() # skip header

    if index: # create index if user selected to
        lucene.initVM(vmargs=['-Djava.awt.headless=true'])  # initialize lucene
        store = MMapDirectory(Paths.get('index'))
        analyzer = StandardAnalyzer()
        config = IndexWriterConfig(analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        writer = IndexWriter(store, config)

    players = {}  # dictionary of all players from file

    for line in file:
        line = line.strip().split('\t') # split line by tab
        if len(line) < 50: # skip lines with missing data
            continue

        player_id = line[0]
        name = line[1]
        short_description = line[2]
        description = line[3]
        teams = line[12]

        if index:
            document = Document()  # create document for each player
            field_type = FieldType()
            field_type.setStored(True)
            field_type.setIndexOptions(IndexOptions.NONE)

            document.add(Field("id", str(player_id), field_type))
            document.add(Field("name", name, TextField.TYPE_NOT_STORED))
            document.add(Field("short_description", short_description, TextField.TYPE_NOT_STORED))
            document.add(Field("description", description, TextField.TYPE_NOT_STORED))
            document.add(Field("teams", teams, TextField.TYPE_NOT_STORED))
            document.add(Field("birth_place", line[49], TextField.TYPE_NOT_STORED))
            writer.addDocument(document)

        players[line[0]] = {
            'id': line[0],
            'name': line[1],
            'short_description': line[2],
            'description': line[3],
            'overall': line[4],
            'potential': line[5],
            'height': line[6],
            'weight': line[7],
            'preferred_foot': line[8],
            'birth_date': line[9],
            'age': line[10],
            'preferred_positions': line[11],
            'teams': line[12],
            'traits': line[13],
            'week_foot_rating': line[14],
            'skill_moves_rating': line[15],
            'ball_control': line[16],
            'dribbling': line[17],
            'marking': line[18],
            'slide_tackle': line[19],
            'stand_tackle': line[20],
            'aggression': line[21],
            'reactions': line[22],
            'attack_position': line[23],
            'interceptions': line[24],
            'vision': line[25],
            'crossing': line[26],
            'short_pass': line[27],
            'long_pass': line[28],
            'acceleration': line[29],
            'stamina': line[30],
            'strength': line[31],
            'balance': line[32],
            'sprint_speed': line[33],
            'agility': line[34],
            'jumping': line[35],
            'heading': line[36],
            'shot_power': line[37],
            'finishing': line[38],
            'long_shots': line[39],
            'curve': line[40],
            'fk_accuracy': line[41],
            'penalties': line[42],
            'volleys': line[43],
            'gk_positioning': line[44],
            'gk_diving': line[45],
            'gk_handling': line[46],
            'gk_kicking': line[47],
            'gk_reflexes': line[48],
            'birth_place': line[49],
        }

    if index:
        writer.commit()
        writer.close()
    file.close()
    return players



def test_search(players):
    test_cases = [
        {'field': 'birth_place', 'query': 'Bratislava', 'expected_names': ['Lukáš Haraslín', 'Ivan Schranz', 'Dominik Greif', 'Róbert Mak', 'Branislav Niňaj']},
        {'field': 'birth_place', 'query': 'Košice', 'expected_names': ['Marek Rodák', 'Alex Král', 'Jakub Hromada', 'Tomáš Huk', 'Filip Lesniak']},
        {'field': 'birth_place', 'query': 'Trenčín', 'expected_names': ['Stanislav Lobotka', 'Jakub Holúbek', 'Peter Pokorný']},
        {'field': 'birth_place', 'query': 'Prievidza', 'expected_names': ['Dávid Hancko']},
        {'field': 'birth_place', 'query': 'Žiar nad Hronom', 'expected_names': ['Milan Škriniar']},

    ]
    directory = MMapDirectory(Paths.get('index'))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer()

    total_tp = 0 # total true positives
    total_tn = 0 # total true negatives
    total_fp = 0 # total false positives
    total_fn = 0 # total false negatives

    for case in test_cases: # for each test case
        search_field = case['field']
        query = QueryParser(search_field, analyzer).parse(case['query'])
        results = searcher.search(query, 20000).scoreDocs

        result_names = []

        for i in range(len(results)):
            document = searcher.doc(results[i].doc)
            player_id = document.get("id")
            player = players[player_id]
            player_name = player['name']
            result_names.append(player_name)

        #  compute values for confusion matrix
        tp = len([name for name in result_names if name in case['expected_names']])
        fp = len([name for name in result_names if name not in case['expected_names']])
        fn = len([name for name in case['expected_names'] if name not in result_names])
        tn = len(players) - tp - fp - fn

        # update total values
        total_tp += tp
        total_tn += tn
        total_fp += fp
        total_fn += fn

        print("-------------------------------------------------------------")
        print("Search field: ", search_field)
        print("Test query: ", case['query'])
        print("Expected names: ", case['expected_names'])
        print("Result names: ", result_names)
        print("True positives: ", tp)
        print("True negatives: ", tn)
        print("False positives: ", fp)
        print("False negatives: ", fn)
        accuracy = (tp + tn) / (tp + tn + fp + fn) # compute accuracy
        print("Accuracy: ", accuracy)
        if tp + fp == 0: # if division by zero, set precision to 0
            precision = 0
        else:
            precision = tp / (tp + fp) # compute precision
        print("Precision: ", precision)
        recall = tp / (tp + fn) # compute recall
        print("Recall: ", recall)

    # compute total values for confusion matrix
    total_accuracy = (total_tp + total_tn) / (total_tp + total_tn + total_fp + total_fn)
    if total_tp + total_fp == 0: # if division by zero, set precision to 0
        total_precision = 0
    else:
        total_precision = total_tp / (total_tp + total_fp)
    total_recall = total_tp / (total_tp + total_fn)
    print("-------------------------------------------------------------")
    print("Total test cases: ", len(test_cases))
    print("Total True Positives: ", total_tp)
    print("Total True Negatives: ", total_tn)
    print("Total False Positives: ", total_fp)
    print("Total False Negatives: ", total_fn)
    print("Total accuracy: ", total_accuracy)
    print("Total precision: ", total_precision)
    print("Total recall: ", total_recall)


def search():
    search_fields = ["name", "birth_place", "description"]
    print("-------------------------------------------------------------")
    print("Create index? 1 - yes, 2 - no")

    input_create_index = input("Enter your choice: ")

    if input_create_index not in ['1', '2']: # check if input is valid
        print("Wrong input")
        return

    if input_create_index == '1': # read file and create index
        players = read_file(True)

    else: # read file without creating index
        players = read_file(False)
        lucene.initVM(vmargs=['-Djava.awt.headless=true'])

    directory = MMapDirectory(Paths.get('index'))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer()

    print("Run unit tests? 1 - yes, 2 - no")

    input_tests = input("Enter your choice: ")

    if input_tests not in ['1', '2']: # check if input is valid
        print("Wrong input")
        return

    if input_tests == '1': # run unit tests
        test_search(players)

    while True:
        print("-------------------------------------------------------------")
        print("Enter 0 to exit")
        print("Where search? 1 - Name, 2 - Birth place, 3 - Description")
        input_search_field = input("Enter your choice: ")
        if input_search_field == '0' or input_search_field not in ['1', '2', '3']:  # check if input is valid
            break
        print("-------------------------------------------------------------")
        query_string = input("Enter search query: ")

        search_field = search_fields[int(input_search_field) - 1] # get search field from input
        query = QueryParser(search_field, analyzer).parse(query_string) # create query
        results = searcher.search(query, 20000).scoreDocs # search index

        if len(results) == 0: # if no results, print message and continue
            print("No results")
            continue

        if len(results) == 1: # if only one result, print player
            document = searcher.doc(results[0].doc)
            player_id = document.get("id")
            player = players[player_id]
            teams = player['teams'].strip('][').replace("'", "")
            teams = teams.replace('"', "").replace("[", "").replace("]", "")
            print(player['name'] + ', ' + player['overall'] + ', ' + player['birth_place'] + ', ' + teams)
            continue

        print("Found %d document(s) that matched query '%s':" % (len(results), query_string)) # print number of results if more than one

        print("-------------------------------------------------------------")
        print("1 - Print stats, 2 - Print players")
        input_print = input("Enter your choice: ")

        if input_print not in ['1', '2']:
            print("Wrong input")
            break

        if input_print == '1':
            overall_avg = 0
            potential_avg = 0
            height_avg = 0
            weight_avg = 0
            preferred_foot = {'left': 0, 'right': 0}
            age_avg = 0
            week_foot_rating_avg = 0
            skill_moves_rating_avg = 0
            ball_control_avg = 0
            dribbling_avg = 0
            marking_avg = 0
            slide_tackle_avg = 0
            stand_tackle_avg = 0
            aggression_avg = 0
            reactions_avg = 0
            attack_position_avg = 0
            interceptions_avg = 0
            vision_avg = 0
            crossing_avg = 0
            short_pass_avg = 0
            long_pass_avg = 0
            acceleration_avg = 0
            stamina_avg = 0
            strength_avg = 0
            balance_avg = 0
            sprint_speed_avg = 0
            agility_avg = 0
            jumping_avg = 0
            heading_avg = 0
            shot_power_avg = 0
            finishing_avg = 0
            long_shots_avg = 0
            curve_avg = 0
            fk_accuracy_avg = 0
            penalties_avg = 0
            volleys_avg = 0
            gk_positioning_avg = 0
            gk_diving_avg = 0
            gk_handling_avg = 0
            gk_kicking_avg = 0
            gk_reflexes_avg = 0

            for i in range(len(results)): # compute average values for each attribute
                document = searcher.doc(results[i].doc) # get document
                player_id = document.get("id") # get player id
                player = players[player_id] # get player from dictionary
                overall_avg += int(player['overall'])
                potential_avg += int(player['potential'])
                height_avg += int(player['height'].split(' ')[0])
                weight_avg += int(player['weight'].split(' ')[0])
                preferred_foot[player['preferred_foot']] += 1
                age_avg += int(player['age'])
                week_foot_rating_avg += int(player['week_foot_rating'])
                skill_moves_rating_avg += int(player['skill_moves_rating'])
                ball_control_avg += int(player['ball_control'])
                dribbling_avg += int(player['dribbling'])
                marking_avg += int(player['marking'])
                slide_tackle_avg += int(player['slide_tackle'])
                stand_tackle_avg += int(player['stand_tackle'])
                aggression_avg += int(player['aggression'])
                reactions_avg += int(player['reactions'])
                attack_position_avg += int(player['attack_position'])
                interceptions_avg += int(player['interceptions'])
                vision_avg += int(player['vision'])
                crossing_avg += int(player['crossing'])
                short_pass_avg += int(player['short_pass'])
                long_pass_avg += int(player['long_pass'])
                acceleration_avg += int(player['acceleration'])
                stamina_avg += int(player['stamina'])
                strength_avg += int(player['strength'])
                balance_avg += int(player['balance'])
                sprint_speed_avg += int(player['sprint_speed'])
                agility_avg += int(player['agility'])
                jumping_avg += int(player['jumping'])
                heading_avg += int(player['heading'])
                shot_power_avg += int(player['shot_power'])
                finishing_avg += int(player['finishing'])
                long_shots_avg += int(player['long_shots'])
                curve_avg += int(player['curve'])
                fk_accuracy_avg += int(player['fk_accuracy'])
                penalties_avg += int(player['penalties'])
                volleys_avg += int(player['volleys'])
                gk_positioning_avg += int(player['gk_positioning'])
                gk_diving_avg += int(player['gk_diving'])
                gk_handling_avg += int(player['gk_handling'])
                gk_kicking_avg += int(player['gk_kicking'])
                gk_reflexes_avg += int(player['gk_reflexes'])

            print("Overall avg: ", round(overall_avg / len(results), 2))
            print("Potential avg: ", round(potential_avg / len(results), 2))
            print("Height avg: ", round(height_avg / len(results), 2))
            print("Weight avg: ", round(weight_avg / len(results), 2))
            # percentage of left-footed players and right footed players
            print("Preferred foot: \n    Right - " + str(round(preferred_foot['right'] / len(results) * 100, 2)) + "%\n    Left - " + str(round(preferred_foot['left'] / len(results) * 100, 2)) + "%")
            print("Age avg: ", round(age_avg / len(results), 2))
            print("Week foot rating avg: ", round(week_foot_rating_avg / len(results), 2))
            print("Skill moves rating avg: ", round(skill_moves_rating_avg / len(results), 2))
            print("Ball control avg: ", round(ball_control_avg / len(results), 2))
            print("Dribbling avg: ", round(dribbling_avg / len(results), 2))
            print("Marking avg: ", round(marking_avg / len(results), 2))
            print("Slide tackle avg: ", round(slide_tackle_avg / len(results), 2))
            print("Stand tackle avg: ", round(stand_tackle_avg / len(results), 2))
            print("Aggression avg: ", round(aggression_avg / len(results), 2))
            print("Reactions avg: ", round(reactions_avg / len(results), 2))
            print("Attack position avg: ", round(attack_position_avg / len(results), 2))
            print("Interceptions avg: ", round(interceptions_avg / len(results), 2))
            print("Vision avg: ", round(vision_avg / len(results), 2))
            print("Crossing avg: ", round(crossing_avg / len(results), 2))
            print("Short pass avg: ", round(short_pass_avg / len(results), 2))
            print("Long pass avg: ", round(long_pass_avg / len(results), 2))
            print("Acceleration avg: ", round(acceleration_avg / len(results), 2))
            print("Stamina avg: ", round(stamina_avg / len(results), 2))
            print("Strength avg: ", round(strength_avg / len(results), 2))
            print("Balance avg: ", round(balance_avg / len(results), 2))
            print("Sprint speed avg: ", round(sprint_speed_avg / len(results), 2))
            print("Agility avg: ", round(agility_avg / len(results), 2))
            print("Jumping avg: ", round(jumping_avg / len(results), 2))
            print("Heading avg: ", round(heading_avg / len(results), 2))
            print("Shot power avg: ", round(shot_power_avg / len(results), 2))
            print("Finishing avg: ", round(finishing_avg / len(results), 2))
            print("Long shots avg: ", round(long_shots_avg / len(results), 2))
            print("Curve avg: ", round(curve_avg / len(results), 2))
            print("Fk accuracy avg: ", round(fk_accuracy_avg / len(results), 2))
            print("Penalties avg: ", round(penalties_avg / len(results), 2))
            print("Volleys avg: ", round(volleys_avg / len(results), 2))
            print("Gk positioning avg: ", round(gk_positioning_avg / len(results), 2))
            print("Gk diving avg: ", round(gk_diving_avg / len(results), 2))
            print("Gk handling avg: ", round(gk_handling_avg / len(results), 2))
            print("Gk kicking avg: ", round(gk_kicking_avg / len(results), 2))

        if input_print == '2': # print players
            players_table = []
            for i in range(len(results)):
                document = searcher.doc(results[i].doc)
                player_id = document.get("id")
                player = players[player_id]
                teams = player['teams'].strip('][').replace("'", "")
                teams = teams.replace('"', "").replace("[", "").replace("]", "")
                players_table.append([player['name'], player['overall'], player['birth_place'], teams])

            # compute longest column for each column
            longest_cols = [(max([len(str(row[i])) for row in players_table]) + 3) for i in range(len(players_table[0]))]
            # create row format
            row_format = "".join(["{:>" + str(longest_col) + "}" for longest_col in longest_cols])
            for row in players_table: # print each row based on row format
                print(row_format.format(*row))


if __name__ == '__main__':
    search()

import requests
import re
import time
import xmltodict
import html
import csv
import urllib3

urllib3.disable_warnings()

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36 bot for a semester project - mail:xpenta@stuba.sk - student of Slovak University of Technology in Bratislava'}

url = "https://www.fifaindex.com/sitemap-fifa22-players.xml" # site map of all players for FIFA 22


def crawler():
    with open('output_crawler.tsv', "w", encoding='utf-8') as tsv_file:
        writer = csv.writer(tsv_file, delimiter='\t', lineterminator='\n') # create writer
        header_row = ['id',
                      'name',
                      'short_description',
                      'description',
                      'overall',
                      'potential',
                      'height',
                      'weight',
                      'preferred_foot',
                      'birth_date',
                      'age',
                      'preferred_positions',
                      'teams',
                      'traits',
                      'week_foot_rating',
                      'skill_moves_rating',
                      'ball_control',
                      'dribbling',
                      'marking',
                      'slide_tackle',
                      'stand_tackle',
                      'aggression',
                      'reactions',
                      'attack_position',
                      'interceptions',
                      'vision',
                      'crossing',
                      'short_pass',
                      'long_pass',
                      'acceleration',
                      'stamina',
                      'strength',
                      'balance',
                      'sprint_speed',
                      'agility',
                      'jumping',
                      'heading',
                      'shot_power',
                      'finishing',
                      'long_shots',
                      'curve',
                      'fk_accuracy',
                      'penalties',
                      'volleys',
                      'gk_positioning',
                      'gk_diving',
                      'gk_handling',
                      'gk_kicking',
                      'gk_reflexes']
        writer.writerow(header_row)
        tsv_file.flush() # flush header to file
        response = requests.get(url, headers=headers, verify=False) # get xml file
        time.sleep(1) # wait 1 second to not get banned by server for too many requests in short time period
        data = response.text
        players = xmltodict.parse(data)
        for player in players['urlset']['url']:
            response = requests.get(player['loc'], headers=headers, verify=False) # get player page
            time.sleep(1)
            data = html.unescape(response.text).replace('\t', ' ')  # unescape html entities like &amp;
            player_id = player['loc'].split('https://www.fifaindex.com/player/')[1].split('/')[0]
            name = re.search('<h1>(.*) <span>', data).group(1) # get player name
            short_description = re.search('<meta name="description" content="(.*)" />', data).group(1)
            description = re.search(
                '<h2 class="card-header">Player Stats .*</h2>\n<div class="card-body">\n<p>(.*)</p>', data)
            if description is not None: # get player description
                description = description.group(1)
            else:
                description = None
            overall_rating = re.search( # get overall and potential rating
                '<h5 class="card-header">.*<span class=".*"><span class="badge badge-dark rating .*">([0-9]{2})</span> <span class="badge badge-dark rating .*">([0-9]{2})</span></span>',
                data)
            overall = overall_rating.group(1)
            potential = overall_rating.group(2)
            height = re.search( # get height and weight
                '<p class>Height\s?<span class=".*">.*<span class="data-units .*">([0-9]{3} cm)</span>',
                data).group(1)
            weight = re.search( # get weight
                '<p class>Weight\s?<span class=".*">.*<span class="data-units .*">([0-9]{2,3} kg)</span>',
                data).group(1)
            preferred_foot = re.search( # get preferred foot
                '<p class>Preferred Foot.*<span class=".*">(.*)</span></p>', data).group(
                1).lower()
            birth_date = re.search( # get birth date
                '<p class>Birth Date.*<span class=".*">(.*)</span></p>', data).group(1)
            age = re.search('<p class>Age <span class=".*">([0-9]{2})</span></p>', data).group(1)
            preferred_positions = re.search( # get preferred positions
                '<p class>Preferred Positions.*<span class=".*">.*<a href="/players/.*position=.*" title=".*" class="link-position"><span class="badge badge-dark position [a-z]{2,3}">[A-Z]{2,3}</span>',
                data)
            if preferred_positions is not None:
                preferred_positions = re.findall(
                    '<span class="badge badge-dark position [a-z]{2,3}">([A-Z]{2,3})</span>',
                    preferred_positions.group(0))

            teams = re.findall( # get teams player is playing for in the game
                '<a href="/team/.*" title=".*" class="link-team">(.*)</a>', data)
            traits = re.search( # get traits of player in the game
                '<h5 class="card-header">Traits.*</h5>\n<div class="card-body">[\s\S]*</div>', data)

            if traits is not None:
                traits = re.findall('<p>(.*)</p>', traits.group(0))

            week_foot_rating = re.search( # get week foot rating
                '<p class>Weak Foot.*<span class=".*">.*</span></p>', data)
            if week_foot_rating is not None:
                week_foot_rating = re.findall('<i class="fas fa-star fa-lg">', week_foot_rating.group(0))
                week_foot_rating = len(week_foot_rating)

            skill_moves_rating = re.search( # get skill moves rating
                '<p class>Skill Moves.*<span class=".*">.*</span></p>', data)
            if skill_moves_rating is not None:
                skill_moves_rating = re.findall('<i class="fas fa-star fa-lg">', skill_moves_rating.group(0))
                skill_moves_rating = len(skill_moves_rating)

            ball_control = re.search( # get ball control rating
                '<p class>Ball Control\s?<span class=".*"><span class=".*">(.*)</span></span></p>', data).group(1)
            dribbling = re.search(  # get dribbling rating
                '<p class>Dribbling\s?<span class=".*"><span class=".*">(.*)</span></span></p>', data).group(1)
            marking = re.search( # get marking rating
                '<p class>Marking\s?<span class=".*"><span class=".*">(.*)</span></span></p>', data).group(1)
            slide_tackle = re.search( # get slide tackle rating
                '<p class>Slide Tackle\s?<span class=".*"><span class=".*">(.*)</span></span></p>', data).group(1)
            stand_tackle = re.search( # get stand tackle rating
                '<p class>Stand Tackle\s?<span class=".*"><span class=".*">(.*)</span></span></p>', data).group(1)
            acceleration = re.search( # get acceleration rating
                '<p class>Acceleration\s?<span class=".*"><span class=".*">(.*)</span></span></p>', data).group(1)
            aggression = re.search( # get aggression rating
                '<p class>Aggression\s?<span class=".*"><span class=".*">(.*)</span></span></p>', data).group(1)
            reactions = re.search( # get reactions rating
                '<p class>Reactions\s?<span class=".*"><span class=".*">(.*)</span></span></p>', data).group(1)
            attack_position = re.search( # get attack position rating
                '<p class>Att. Position\s?<span class=".*"><span class=".*">(.*)</span></span></p>', data).group(1)
            interceptions = re.search( # get interceptions rating
                '<p class>Interceptions\s?<span class=".*"><span class=".*">(.*)</span></span></p>', data).group(1)
            vision = re.search( # get vision rating
                '<p class>Vision\s?<span class=".*"><span class=".*">(.*)</span></span></p>', data).group(1)
            crossing = re.search( # get crossing rating
                '<p class>Crossing\s?<span class=".*"><span class=".*">(.*)</span></span></p>', data).group(1)
            short_pass = re.search( # get short pass rating
                '<p class>Short Pass\s?<span class=".*"><span class=".*">(.*)</span></span></p>', data).group(1)
            long_pass = re.search( # get long pass rating
                '<p class>Long Pass\s?<span class=".*"><span class=".*">(.*)</span></span></p>', data).group(1)
            stamina = re.search( # get stamina rating
                '<p class>Stamina\s?<span class=".*"><span class=".*">(.*)</span></span></p>', data).group(1)
            strength = re.search( # get strength rating
                '<p class>Strength\s?<span class=".*"><span class=".*">(.*)</span></span></p>', data).group(1)
            balance = re.search( # get balance rating
                '<p class>Balance\s?<span class=".*"><span class=".*">(.*)</span></span></p>', data).group(1)
            sprint_speed = re.search( # get sprint speed rating
                '<p class>Sprint Speed\s?<span class=".*"><span class=".*">(.*)</span></span></p>', data).group(1)
            agility = re.search( # get agility rating
                '<p class>Agility\s?<span class=".*"><span class=".*">(.*)</span></span></p>', data).group(1)
            jumping = re.search( # get jumping rating
                '<p class>Jumping\s?<span class=".*"><span class=".*">(.*)</span></span></p>', data).group(1)
            heading = re.search( # get heading rating
                '<p class>Heading\s?<span class=".*"><span class=".*">(.*)</span></span></p>', data).group(1)
            shot_power = re.search( # get shot power rating
                '<p class>Shot Power\s?<span class=".*"><span class=".*">(.*)</span></span></p>', data).group(1)
            finishing = re.search( # get finishing rating
                '<p class>Finishing\s?<span class=".*"><span class=".*">(.*)</span></span></p>', data).group(1)
            long_shots = re.search( # get long shots rating
                '<p class>Long Shots\s?<span class=".*"><span class=".*">(.*)</span></span></p>', data).group(1)
            curve = re.search( # get curve rating
                '<p class>Curve\s?<span class=".*"><span class=".*">(.*)</span></span></p>', data).group(1)
            fk_accuracy = re.search( # get fk accuracy rating
                '<p class>FK Acc.\s?<span class=".*"><span class=".*">(.*)</span></span></p>', data).group(1)
            penalties = re.search( # get penalties rating
                '<p class>Penalties\s?<span class=".*"><span class=".*">(.*)</span></span></p>', data).group(1)
            volleys = re.search( # get volleys rating
                '<p class>Volleys\s?<span class=".*"><span class=".*">(.*)</span></span></p>', data).group(1)
            gk_positioning = re.search( # get gk positioning rating
                '<p class>GK Positioning\s?<span class=".*"><span class=".*">(.*)</span></span></p>', data).group(1)
            gk_diving = re.search( # get gk diving rating
                '<p class>GK Diving\s?<span class=".*"><span class=".*">(.*)</span></span></p>', data).group(1)
            gk_handling = re.search( # get gk handling rating
                '<p class>GK Handling\s?<span class=".*"><span class=".*">(.*)</span></span></p>', data).group(1)
            gk_kicking = re.search( # get gk kicking rating
                '<p class>GK Kicking\s?<span class=".*"><span class=".*">(.*)</span></span></p>', data).group(1)
            gk_reflexes = re.search( # get gk reflexes rating
                '<p class>GK Reflexes\s?<span class=".*"><span class=".*">(.*)</span></span></p>', data).group(1)

            line = [player_id, name, short_description, description, overall, potential, height, weight, preferred_foot, birth_date, age, preferred_positions, teams, traits, week_foot_rating, skill_moves_rating, ball_control, dribbling, marking, slide_tackle, stand_tackle, aggression, reactions, attack_position, interceptions, vision, crossing, short_pass, long_pass, acceleration, stamina, strength, balance, sprint_speed, agility, jumping, heading, shot_power, finishing, long_shots, curve, fk_accuracy, penalties, volleys, gk_positioning, gk_diving, gk_handling, gk_kicking, gk_reflexes,]
            writer.writerow(line)
    tsv_file.close()


if __name__ == '__main__':
    crawler()

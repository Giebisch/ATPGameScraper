import requests
from bs4 import BeautifulSoup
import sys
import datetime
import aiohttp
import asyncio

class Game:
    """
    Contains all the important stats about one game
    Can give back a formatted line for csv files
    """
    def __init__(self, player, tournament, round, opponent, rank, w_l, score):
        self.player = player
        self.tournament = tournament
        self.round = round
        self.opponent = opponent
        self.rank = rank
        self.w_l = w_l
        self.score = score
    def get_data(self):
        data = ";".join([self.player, self.tournament, self.round, \
            self.opponent, self.rank, self.w_l, self.score])
        return data

async def scrape_person(url, output):
    """
    Takes an url for a specific player as an input and scrapes all the games
    from the atp website
    If output == true, games will be written to csv file
    """
    games_played = []
    # get link to all games played
    url = url[:url.find("/overview")] + "/player-activity?year=all"
    # r = requests.get(url)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print(url)
            res = await response.read()
            soup = BeautifulSoup(res.decode("utf-8"), "html.parser")
            player_name = soup.find(class_="first-name").text + " " + soup.find(class_="last-name").text
            tournaments = soup.find_all("div", class_="activity-tournament-table")
            for tournament in tournaments:
                tournament_name = tournament.find(class_="tourney-title").text.strip().strip()
                content = tournament.find("table", class_="mega-table").find("tbody")
                for game in content.find_all("tr"):
                    game_stats = game.find_all("td")
                    round, rank, opponent, w_l, score = game_stats
                    opponent = opponent.find(class_="mega-player-name")
                    games_played.append(Game(player_name, tournament_name, round.text, \
                        opponent.text, rank.text.strip(), w_l.text.strip(), score.text.strip()))
            if output:
                with open("atp_" + player_name.replace(" ", "_") + "_" + \
                    datetime.datetime.now().strftime("%d_%m_%Y") + ".csv", "w") as out:
                    for game in games_played:
                        out.write(game.get_data() + "\n")
            else:
                return games_played

def scrape_top_50():
    """
    Searches on the atptour website for the top 50 players and 
    calls scrape_person for each one
    Write all collected games to csv file after
    """
    all_players = []
    url = "https://www.atptour.com/en/rankings/singles"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    content = soup.find("table", class_="mega-table").find("tbody")
    hrefs = []
    for player in content.find_all("tr"):
        href = player.find(class_="player-cell").find("a")["href"]
        player_url = "https://www.atptour.com" + href
        # all_players.append(scrape_person(player_url, False))
        hrefs.append(player_url)
        # print("Getting games for: " + all_players[-1][0].player)
    loop = asyncio.get_event_loop()
    tasks = [scrape_person(href, False) for href in hrefs]
    vars,_ = loop.run_until_complete(asyncio.wait(tasks))
    all_players = [v.result() for v in vars]
    with open("atp_top_50_" + datetime.datetime.now().strftime("%d_%m_%Y") + ".csv", "w") as out:
        for player in all_players:
            for game in player:
                out.write(game.get_data() + "\n")
        

if __name__ == "__main__":
    # example input "https://www.atptour.com/en/players/novak-djokovic/d643/overview"
    if len(sys.argv) == 1:
        scrape_top_50()
    elif len(sys.argv) == 2:
        # True, if only one person has to be scraped
        scrape_person(sys.argv[1], True)
    else:
        print("Error with argument.")
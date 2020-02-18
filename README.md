# ATPGameScraper
Python scraper for getting all games played by a specific ATP player or the top 100 players

Data is getting scraped from the Official Site of Men's Professional Tennis www.atptour.com

# Installation
Make sure to have python3 installed. Download files and run 

    pip install -r requirements.txt

or on Ubuntu

    pip3 install -r requirements.txt

# Usage
To download all the games of the top 100 players simply run the scraper with

    python scraper.py

or on Ubuntu with

    python3 scraper.py

To get only the games froma specific player, give an additional argument with link of the player, example:

    python scraper.py https://www.atptour.com/en/players/novak-djokovic/d643/overview

Get the link from the official atptour.com website.

# Result
The scraper will automatically create a *.csv* file with all the games listed. Example:

    Novak Djokovic;Tokyo;Finals;John Millman;80;W;63 62
    Novak Djokovic;Tokyo;Semi-Finals;David Goffin;15;W;63 64
    Novak Djokovic;Tokyo;Quarter-Finals;Lucas Pouille;24;W;61 62
    Novak Djokovic;Tokyo;Round of 16;Go Soeda;133;W;63 75
    Novak Djokovic;Tokyo;Round of 32;Alexei Popyrin;94;W;64 62
    Novak Djokovic;US Open;Round of 16;Stan Wawrinka;24;L;46 57 12 (RET)
    Novak Djokovic;US Open;Round of 32;Denis Kudla;111;W;63 64 62
    Novak Djokovic;US Open;Round of 64;Juan Ignacio Londero;56;W;64 763 61
    Novak Djokovic;US Open;Round of 128;Roberto Carballes Baena;76;W;64 61 64
    ...

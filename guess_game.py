# imports for scraping
import requests
from bs4 import BeautifulSoup
from random import choice
from csv import DictReader

# scapring with BeautifulSoup

base_url = 'http://quotes.toscrape.com/'

def read_quotes(filename):
    with open(filename, 'r') as file:
        csv_reader = DictReader(file)
        return list(csv_reader)

def start_game(quotes):
    quote = choice(quotes)
    remaining_guesses = 4
    print("Here is a quote: ")
    print(quote['text'])
    guess = ''

    while guess.lower() != quote['author'].lower() and remaining_guesses >0:
        guess = input(f"who said this quote? guesses remaining: {remaining_guesses}\n")
        if guess.lower() == quote['author'].lower():
            print('well done')
            break
        remaining_guesses -=1
        print_hint(quote,remaining_guesses)
        
    again = ''
    while again.lower() not in ('y', 'yes','n', 'no'):
        again = input('would you like to play again (y/n)?')
        if again.lower() in ('yes', 'y'):
            return start_game(quotes)
        else:("Ok Goodbye")
        
def print_hint(quote, remaining_guesses):
    if remaining_guesses == 3:
        res = requests.get(f"{base_url}{quote['bio-link']}")
        soup = BeautifulSoup(res.text, 'html.parser')
        birth_date = soup.find(class_='author-born-date').get_text()
        birth_place = soup.find(class_='author-born-location').get_text()
        print(f"here is a hint: the author was born on {birth_date} {birth_place}")
    elif remaining_guesses == 2:
        print(f"here is a hint: the author's first name starts wiht: {quote['author'][0]}")
    elif remaining_guesses == 1:
        last_initial =  quote['author'].split(' ')[1][0]
        print(f"here is a hint: the author's last name starts wiht: {last_initial}")
    else:
        print(f"Sorry you run out of guesses. the anwser was {quote['author']}") 
    
        
quotes = read_quotes('quotes.csv')
start_game(quotes)

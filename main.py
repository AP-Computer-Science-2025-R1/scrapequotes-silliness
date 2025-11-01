# ==================================
#      Python Quote Scraper
#
# Team: Silliness
# Members: Arshia, Pearl, Alvin, David, Svitozar (Ed), Ronny, Akib
# ==================================



# SECTION 1: IMPORTS
# All team members: Add the libraries you need for your function here.
import requests
import json
import random
import os
from bs4 import BeautifulSoup
from datetime import datetime


# ==================================
# SECTION 2: FUNCTION DEFINITIONS
# ==================================

# --- Function for Akib ---
# TODO: Put your group_introductions() function here.
# This function should print an introduction of the group, and ask the user for inputting the date.
# It should return the name of our group members and an input asking for the user to input the date.
def group_introductions():
	print("Group members and their roles")
	print("-----------------------------")
	print("Akib - group_introductions")
	print("Alvin - scrape_all_quotes")
	print("Pearl - scrape_all_quotes")
	print("Svitozar - save_quotes_to_disk")
	print("David - load_quotes_from_disk")
	print("Ronny - get_random_quote")
	print("   ")
	while True:
		date_input = input("Please enter the date you'd like to get quotes from (in YYYY-MM-DD): ")
		if len(date_input) == 10 and date_input[4] == '-' and date_input[7] == '-':
			year, month, day = date_input.split('-')
			if year.isdigit() and month.isdigit() and day.isdigit():
				return date_input
			else:
				print("Invalid input. Please enter only numbers in the format YYYY-MM-DD.")
		else:
			print("Invalid format. Please use the format YYYY-MM-DD (e.g., 2025-11-01).")

# --- Function for Alvin and Pearl ---

def scrape_all_quotes():

# Scrapes all quotes from https://quotes.toscrape.com across all pages.
# Returns a list of quote dictionaries.

	print("Scraping quotes from https://quotes.toscrape.com ...")
	base_url = "https://quotes.toscrape.com"
	next_page = "/"
	all_quotes = []

	while next_page:
		response = requests.get(base_url + next_page)
		soup = BeautifulSoup(response.text, "html.parser")
		quotes = soup.find_all("div", class_="quote")

		for q in quotes:
			text = q.find("span", class_="text").get_text()
			author = q.find("small", class_="author").get_text()
			author_link = q.find("a")["href"]
			tags = [tag.get_text() for tag in q.find_all("a", class_="tag")]
			all_quotes.append({
				"text": text,
				"author": author,
				"author_link": author_link,
				"tags": tags
			})

		next_btn = soup.find("li", class_="next")
		next_page = next_btn.find("a")["href"] if next_btn else None

	print(f"Scraped {len(all_quotes)} quotes total.")
	return all_quotes

# --- Function for Svitozar (Ed) ---
# TODO: Put your save_quotes_to_disk function here.
# This function should take the list of quotes and a filename.
# It should save the quotes to a JSON or CSV file.
def save_quotes_to_disk(quotes_list, date_str):
	filename = f"quotes_{date_str}.json"
	try:
		with open(filename, 'w', encoding='utf-8') as f:
			json.dump(quotes_list, f, indent=4, ensure_ascii=False)
		print(f"Quotes saved to {filename}")
	except IOError as e:
		print(f"Error saving quotes: {e}")
  
      
    # return data_as_a_file --valdez commented this out

# --- Function for David ---
# TODO: Put your load_quotes_from_disk function here.
# This function should take a filename.
# If the file exists, it returns the list of quotes from the file.
# If the file does not exist, it returns an empty list [].

def load_quotes_from_disk(filename):
	"""
	Loads quotes from JSON file if it exists, otherwise returns empty list.
	"""
	if not os.path.exists(filename):
		print(f"File '{filename}' not found ⚠️. Will scrape fresh data.")
		return []

	try:
		with open(filename, 'r', encoding='utf-8') as f:
			data = json.load(f)
			print(f"Loaded {len(data)} quotes from {filename}")
			return data
	except (IOError, json.JSONDecodeError) as e:
		print(f"Error reading file '{filename}': {e}")
		return []


# --- Function for Alvin and Pearl ---
# TODO: Put your get_quotes_by_tag function here.
# This function should take the list of quotes.
# It asks the user for a tag and prints any matching quotes.
def get_quotes_by_tag(quotes_list):
	tag = input("Enter a tag to search for: ").strip().lower()
	matches = [q for q in quotes_list if tag in [t.lower() for t in q.get("tags", [])]]

	if matches:
		for q in matches:
			print(f"\"{q['text']}\" — {q['author']}\n")
	else:
		print(f"No quotes found with tag '{tag}'.")



# --- Function for Ronny ---
# TODO: Put your get_random_quote function here.
# This function should take the list of quotes.
# It picks one random quote and prints it.
def get_random_quote(quotes_list):
	if not quotes_list:
		print("No quotes available.")
		return
	quote = random.choice(quotes_list)
	print(f"\nRandom Quote:\n\"{quote['text']}\" — {quote['author']}\n")

# Extra Credit: Arshia

# Getting Top 10 Tags
def get_top_tags():
	print("Fetching top 10 tags...")
	url = "https://quotes.toscrape.com"
	response = requests.get(url)
	soup = BeautifulSoup(response.text, "html.parser")
	tags = [tag.get_text() for tag in soup.select(".tag-item a")]
	print("\n Top 10 Tags:")
	for t in tags:
		print("-", t)
	print()

# Getting Author Information
def get_author_info(base_url, author_link):
	try:
		response = requests.get(base_url + author_link)
		soup = BeautifulSoup(response.text, "html.parser")
		name = soup.find("h3", class_="author-title").get_text(strip=True)
		birth_date = soup.find("span", class_="author-born-date").get_text(strip=True)
		birth_location = soup.find("span", class_="author-born-location").get_text(strip=True)
		description = soup.find("div", class_="author-description").get_text(strip=True)
		print(f"\n👤 {name}")
		print(f"Born: {birth_date} {birth_location}")
		print(f"Bio: {description[:200]}...\n")
	except Exception as e:
		print(f"Could not retrieve author info: {e}")


#Interactive Menu
def show_menu(quotes):
	base_url = "https://quotes.toscrape.com"
	while True:
		print("\nMENU")
		print("1. Find quotes by tag")
		print("2. Get random quote")
		print("3. View top 10 tags")
		print("4. Get author info (from random quote)")
		print("5. Force re-scrape quotes")
		print("6. Exit")

		choice = input("Choose an option (1-6): ")

		if choice == "1":
			get_quotes_by_tag(quotes)
		elif choice == "2":
			get_random_quote(quotes)
		elif choice == "3":
			get_top_tags()
		elif choice == "4":
			if not quotes:
				print("No quotes loaded.")
			else:
				quote = random.choice(quotes)
				print(f"Selected author: {quote['author']}")
				get_author_info(base_url, quote["author_link"])
		elif choice == "5":
			print("Re-scraping quotes...")
			quotes = scrape_all_quotes()
			print("Fresh quotes scraped.")
		elif choice == "6":
			print("Goodbye!")
			break
		else:
			print("Invalid choice. Please enter 1–6.")




# ==================================
# SECTION 3: MAIN PROGRAM
# ==================================
if __name__ == "__main__":
	date_str = group_introductions()
	filename = f"quotes_{date_str}.json"

	quotes = load_quotes_from_disk(filename)
	if not quotes:
		quotes = scrape_all_quotes()
		save_quotes_to_disk(quotes, date_str)

	show_menu(quotes)


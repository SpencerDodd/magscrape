"""
This program is a command-line application for scraping magnet links from
TPB for a search of interest.
"""

from lxml import html
import requests
import sys

result_limit = 10

""" This method formats the cli input into a TPB search url that can
be used with requests to get search results
"""
def get_search_url(search):
	search_string = "search/" + search.replace(" ", "%20") + "/0/99/0"
	search_url = "https://www.thepiratebay.org/{}".format(search_string)
	
	return search_url
	

def tpb_results(search):
	url = get_search_url(search)
	page = requests.get(url)
	magnet_links = []
	r_content = ""

	for c in page.text:
		r_content += c

	# ----------
	# now we search for magnet links
	last_hit_index = 0
	searching_for_links = True
	while searching_for_links:
		if len(magnet_links) >= result_limit:
			searching_for_links = False
			break
		else:
			try:
				# get the beginning of the magnet link
				current_hit_index = r_content.index("magnet:", last_hit_index)

				# find the end of the magnet link
				magnet_area = r_content[current_hit_index:current_hit_index + 500]
				end_of_link_index = current_hit_index + magnet_area.index('"')

				# actual magnet link string
				link_address = r_content[current_hit_index:end_of_link_index]

				# Get the title
				title_area = r_content[current_hit_index-200:current_hit_index]
				title = title_area.split('title="')[1]
				title = title.split("\"")[0]
				title = title.split("Details for ")[1]
				
				# The seeder leecher info is found after the magnet link
				seeder_index = r_content.index('<td align="right">', end_of_link_index) + len('<td align="right">')
				seeders = r_content[seeder_index:seeder_index+6]
				seeders = seeders.split("<")[0]
				# update end of link
				leecher_index = r_content.index('<td align="right">', seeder_index+5) + len('<td align="right">')
				leechers = r_content[leecher_index:seeder_index+6]
				leechers = leechers.split("<")[0]

				

				# parse out the full magnet link from the bounds
				magnet_link = {
					"link":link_address,
					"seeders":seeders,
					"leechers":leechers,
					"title":title
				}

				# add our link to the links
				magnet_links.append(magnet_link)

				# update our index
				last_hit_index = end_of_link_index

			except Exception as e:
				print ("error finding magnet links (maybe empty)")
				print (e)
				searching_for_links = False

	return magnet_links

def main():
	search = str(input("Magnet search for: "))
	results = tpb_results(search)
	print ("="*200)
	for link in results:
		print ("Title: {}\nSeeders: {}\n Magnet: {}".format(link["title"], link["seeders"], link["link"]))
		print ("-"*40)
	print ("Complete!")

if __name__ == "__main__":
	main()

















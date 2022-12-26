from ..scraper import Scraper
from requests import Session
from selectolax.parser import HTMLParser

URL = 'https://ist.mit.edu/software-hardware'

class ISTSoftwareScraper(Scraper):

	def __init__(self, session: Session) -> None:
		super().__init__(session)

	def markdown(self) -> str:

		output = "### [Software](https://ist.mit.edu/software-hardware)\n\n"
		
		starting_res = self.session.get(URL)
		starting_res.raise_for_status()

		starting_tree = HTMLParser(starting_res.text)
		software_types = [
			(option.text(), option.attributes['value'])
			for option
			in starting_tree.css('select#edit-type option')
			if option.attributes['value'] != 'All'
		]

		for type_name, type_id in software_types:
			res = self.session.get(URL, params={'type': type_id})
			res.raise_for_status()

			base_url = res.url
			output += f"#### [{type_name}]({base_url})\n\n"

			tree = HTMLParser(res.text)
			items = tree.css("table.views-table tbody tr td.views-field-title a")

			output += "\n".join(f"* {self.html_anchor_to_markdown(item, base=base_url)}" for item in items)

			output += "\n\n"

		return output

if __name__ == "__main__":
	from requests import Session
	print(ISTSoftwareScraper(Session()).markdown())

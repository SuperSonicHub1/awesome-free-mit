from ..scraper import Scraper
from requests import Session
from selectolax.parser import HTMLParser


class ISTServicesScraper(Scraper):

	def __init__(self, session: Session) -> None:
		super().__init__(session)

	def markdown(self) -> str:
		output = "### [Services](https://ist.mit.edu/services)\n\n"
		
		res = self.session.get('https://ist.mit.edu/services?qt-services_list=0')
		res.raise_for_status()

		base_url = res.url

		tree = HTMLParser(res.text)
		categories = tree.css("div.view-content > div.item-list")

		for category in categories:
			heading = category.css_first("h3 a[typeof='skos:Concept']")
			output += f"#### {self.html_anchor_to_markdown(heading, base=base_url)}\n\n"
			output += "\n".join(f"* {self.html_anchor_to_markdown(item, base=base_url)}" for item in category.css("ul li a")) + "\n\n"

		return output

if __name__ == "__main__":
	from requests import Session
	print(ISTServicesScraper(Session()).markdown())

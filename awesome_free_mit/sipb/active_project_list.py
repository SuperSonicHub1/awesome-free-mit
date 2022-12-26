from ..scraper import Scraper
from requests import Session
from selectolax.parser import HTMLParser


class SIPBActiveProjectList(Scraper):

	def __init__(self, session: Session) -> None:
		super().__init__(session)

	def markdown(self) -> str:
		output = "### [SIPB Active Project List](https://sipb-projectdb.scripts.mit.edu/projectlist.py)\n\n"
		
		res = self.session.get('https://sipb-projectdb.scripts.mit.edu/projectlist.py?filter_by=active')
		res.raise_for_status()

		base_url = res.url

		tree = HTMLParser(res.text)
		headers = tree.css("tr.header")

		for header in headers:
			project_title = header.text(strip=True)
			description = ' '.join(header.next.next.next.next.text(strip=True).split("Description:")[-1].split("\n"))
			link = header.next.next.next.next.next.next.css_first('a')

			output += f'* {self.html_anchor_to_markdown(link, text=project_title, base=base_url) if link else project_title}\n\t* {description}\n'

		return output

if __name__ == "__main__":
	from requests import Session
	print(SIPBActiveProjectList(Session()).markdown())

from ..scraper import Scraper
from requests import Session
from selectolax.parser import HTMLParser

URL = 'https://libguides.mit.edu/az.php'

class MITLibrariesAZDatabases(Scraper):
	def __init__(self, session: Session) -> None:
		super().__init__(session)

	def markdown(self) -> str:
		output = f"### [A-Z Databases]({URL})\n\n"
		
		starting_res = self.session.get(URL)
		starting_res.raise_for_status()
		base_url = starting_res.url

		starting_tree = HTMLParser(starting_res.text)
		subjects = [
			(option.text().rsplit(' ', 1)[0], option.attributes['value'])
			for option
			in starting_tree.css('select#s-lg-sel-subjects option')
			# Gets rid of "All Subject"
			if option.attributes['value']
		]

		for subject, subject_id in subjects:
			output += f"#### [{subject}]({URL + f'?s={subject_id}'})\n\n"

			res = self.session.get(
				'https://libguides.mit.edu/process/az/dblist',
				params=dict(
					search='',
					subject_id=subject_id,
					type_id='',
					vendor_id='',
					page=1,
					site_id=68,
					content_id=0,
					is_widget=0,
					bootstrap5='false'
				)
			)
			res.raise_for_status()

			tree = HTMLParser(res.json()['data']['html'])
			results = tree.css("div.s-lg-az-result")
		
			for result in results:
				title = result.css_first('div.s-lg-az-result-title a')
				description = result.css_first('div.s-lg-az-result-description').text()

				item = f"* {self.html_anchor_to_markdown(title, base=base_url)}\n"
				if description:
					item += f"	* {description}\n"
				
				output += item

			output += "\n"

		return output

if __name__ == "__main__":
	from requests import Session
	print(MITLibrariesAZDatabases(Session()).markdown())



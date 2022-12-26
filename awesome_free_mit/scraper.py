from urllib.parse import urljoin
from requests import Session
from selectolax.parser import Node

class Scraper:
	session: Session

	def __init__(self, session: Session) -> None:
		super().__init__()
		self.session = session

	def html_anchor_to_markdown(self, anchor: Node, text: str | None = None, base: str = '') -> str:
		assert anchor.tag.lower() == "a"
		return f'[{text if text else anchor.text(strip=True)}]({urljoin(base, anchor.attributes["href"])})'

	def markdown(self) -> str:
		...

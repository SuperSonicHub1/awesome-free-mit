from requests import Session
from ..scraper import Scraper
from .azdatabases import MITLibrariesAZDatabases
from pathlib import Path

class MITLibraries(Scraper):

	def __init__(self, session: Session) -> None:
		super().__init__(session)

	def markdown(self) -> str:
		azdatabases = MITLibrariesAZDatabases(self.session)

		return '\n\n'.join([
			"## [MIT Libraries](https://libraries.mit.edu/)",
			azdatabases.markdown(),
			*[path.read_text('utf-8') for path in Path(__file__).parent.glob("*.md")]
		])	
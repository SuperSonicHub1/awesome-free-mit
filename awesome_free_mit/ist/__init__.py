from requests import Session
from ..scraper import Scraper
from .services import ISTServicesScraper
from .software import ISTSoftwareScraper

class InformationSystemsTechnology(Scraper):

	def __init__(self, session: Session) -> None:
		super().__init__(session)

	def markdown(self) -> str:
		services = ISTServicesScraper(self.session)
		software = ISTSoftwareScraper(self.session)

		return '\n\n'.join([
			"## [Information Systems and Technology](https://ist.mit.edu/)",
			services.markdown(),
			software.markdown(),
		])	

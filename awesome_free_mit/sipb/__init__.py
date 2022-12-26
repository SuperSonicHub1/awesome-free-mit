from requests import Session
from ..scraper import Scraper
from .active_project_list import SIPBActiveProjectList
from pathlib import Path

class StudentInformationProcessingBoard(Scraper):

	def __init__(self, session: Session) -> None:
		super().__init__(session)

	def markdown(self) -> str:
		active_project_list = SIPBActiveProjectList(self.session)

		return '\n\n'.join([
			"## [Student Information Processing Board](https://sipb.mit.edu/)",
			active_project_list.markdown(),
			*[path.read_text('utf-8') for path in Path(__file__).parent.glob("*.md")]
		])	
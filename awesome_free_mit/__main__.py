from pathlib import Path
from requests import Session 
from .ist import InformationSystemsTechnology
from .sipb import StudentInformationProcessingBoard

parent = Path(__file__).parent

with Session() as session:
	with open('README.md', 'w') as f:
		f.write(
			"\n\n".join([
				(parent / "prelude.md").read_text(),
				InformationSystemsTechnology(session).markdown(),
				StudentInformationProcessingBoard(session).markdown(),
				(parent / "misc.md").read_text(),
			])
		)

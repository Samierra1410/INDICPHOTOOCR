# from strhub.data.module import SceneTextDataModule
# from strhub.models.utils import load_from_checkpoint
import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '/DATA/ocr_team_2/anik/github_repo/bharatSTR/bharatSTR') 
from .infer import bstr
from .infer import bstr_onImage
# some_file.py

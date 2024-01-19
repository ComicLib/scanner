from pathlib import Path

from comiclib.utils import is_image

import logging
logger = logging.getLogger(__name__)

"This scanner may merge to the internal scanners in the future."

class Scanner:
    '''Handle regular folder, all file inside should be image and without nested structure.'''
    
    def scan(self, path: Path, id: str, metadata: dict, prev_scanners: list[str]) -> bool:
        if path.is_dir() and all(p.is_file() and is_image(p) for p in path.iterdir()) and (pagecount := len(list(path.iterdir()))) > 0:
            logger.info(f' <- {path}')
            metadata["title"] = path.name
            metadata["pagecount"] = pagecount
            return True
        else:
            return False

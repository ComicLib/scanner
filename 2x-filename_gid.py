from pathlib import Path
import re

import logging
logger = logging.getLogger(__name__)

class Scanner:
    '''Extract the E-Hentai gallery gid from filenames like "[1234567] title.zip".

    Lowest priority: only fills in the source URL when no previous scanner
    provided any gid (i.e. source is still empty and the ID is still the
    path-based one starting with "00"). Filenames without
    a bracketed 5-8 digit number (e.g. "[666]" or years like "[2024]") are ignored.
    '''

    def scan(self, path: Path, id: str, metadata: dict, prev_scanners: list[str]) -> bool:
        if not path.is_dir() \
                and metadata.get("source") is None \
                and str(metadata.get("id", "")).startswith("00") \
                and prev_scanners \
                and (m := re.search(r"\[(\d{5,8})\]", path.name)) is not None:
            logger.info(f' <- {path}')
            metadata["source"] = f'https://exhentai.org/g/{m[1]}/'
            return True
        else:
            return False

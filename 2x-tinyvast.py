from pathlib import Path
import re

class Scanner:
    '''Parse the titles of the comic files downloaded from https://tinyvast.net (a.k.a. EX全汉化同人合集 and EX全汉化杂志合集)'''

    def scan(self, path: Path, id: str, metadata: dict, prev_scanners: list[str]) -> bool:
        if '10-zip' in prev_scanners and not '20-ccloli' in prev_scanners and (m := re.match(r'\d+X?\.(.+)', path.stem, re.ASCII)) is not None:
            metadata["title"] = m[1]
            return True
        else:
            return False

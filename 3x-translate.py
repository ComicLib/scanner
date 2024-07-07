from pathlib import Path
import requests

class Scanner:
    '''Translate English tags to Chinese'''

    def __init__(self) -> None:
        tag_trans_db = requests.get('https://cdn.jsdelivr.net/gh/EhTagTranslation/DatabaseReleases/db.text.json', timeout=7).json()["data"]
        self.trans_tag = {}
        self.trans_namespace = {}
        for namespace in tag_trans_db:
            self.trans_namespace[namespace["namespace"]] = namespace["frontMatters"]["name"]
            for tag in namespace["data"]:
                self.trans_tag[f'{namespace["namespace"]}:{tag}'] = f'{namespace["frontMatters"]["name"]}:{namespace["data"][tag]["name"]}'
    
    def scan(self, path: Path, id: str, metadata: dict, prev_scanners: list[str]) -> bool:
        if metadata["tags"] is None:
            return False
        old_tags = metadata["tags"]
        tags = set()
        for tag in old_tags:
            if tag.isascii() and tag in self.trans_tag:
                tags.add(self.trans_tag[tag])
            else:
                tags.add(tag)
        metadata["tags"] = tags
        return not tags == old_tags

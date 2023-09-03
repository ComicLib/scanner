from pathlib import Path
import requests

class Scanner:
    '''Translate Chinese tags back to English'''

    def __init__(self) -> None:
        tag_trans_db = requests.get('https://cdn.jsdelivr.net/gh/EhTagTranslation/DatabaseReleases/db.text.json').json()["data"]
        self.detrans_tag = {}
        self.detrans_namespace = {}
        for namespace in tag_trans_db:
            self.detrans_namespace[namespace["frontMatters"]["name"]] = namespace["namespace"]
            for tag in namespace["data"]:
                self.detrans_tag[f'{namespace["frontMatters"]["name"]}:{namespace["data"][tag]["name"]}'] = f'{namespace["namespace"]}:{tag}'
    
    def scan(self, path: Path, id: str, metadata: dict, prev_scanners: list[str]) -> bool:
        if metadata["tags"] is None:
            return False
        old_tags = metadata["tags"]
        tags = set()
        for tag in old_tags:
            if not tag.isascii():
                namespace, _, name = tag.partition(':')
                if namespace == '社团': namespace = "团队"
                if name.isascii():
                    tags.add(self.detrans_namespace[namespace] + ':' + name)
                else:
                    tags.add(self.detrans_tag[namespace + ':' + name])
            else:
                tags.add(tag)
        metadata["tags"] = tags
        return not tags == old_tags

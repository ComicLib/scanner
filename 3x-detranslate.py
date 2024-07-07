from pathlib import Path
import requests

class Scanner:
    '''Translate Chinese tags back to English'''

    def __init__(self) -> None:
        zh2en = requests.get("https://cdn.jsdelivr.net/gh/ComicLib/EhTagTranslation_rev/zh2en.json", timeout=7).json()
        self.detrans_namespace = zh2en["namespace"]
        self.detrans_tag = zh2en["tag"]
    
    def scan(self, path: Path, id: str, metadata: dict, prev_scanners: list[str]) -> bool:
        if metadata["tags"] is None:
            return False
        old_tags = metadata["tags"]
        tags = set()
        for tag in old_tags:
            if not tag.isascii():
                namespace, _, name = tag.partition(':')
                if namespace in self.detrans_namespace:
                    tag = self.detrans_namespace[namespace] + ':' + self.detrans_tag[self.detrans_namespace[namespace]].get(name, name)
            assert tag.isascii(), repr(tag)
            tags.add(tag)
        metadata["tags"] = tags
        return not tags == old_tags

import json
from pathlib import Path
from typing import Any 

class Persist:
    def __init__(self, fname: str ='db.json'):
        self.fname = fname
        fname_path = Path(fname)

        if fname_path.exists():
            with open(fname) as f:
                self.data = json.load(f)
        else:
            self.data: dict[str,list[dict[Any, Any]]]= dict()
            
    def _save(self):
        with open(self.fname, 'w') as fn:
            json.dump(self.data, fn)

    def add(self, key: str, data: dict):
        if self.data.get(key):
            self.data[key].append(data)
        else:
            self.data[key] = [data]
        self._save()

    def update(self, key: str, item_id: str, data: dict):
        """TODO: need to generalise the update logic in the future"""
        index = [ idx for idx, item in enumerate(self.data.get(key)) 
                      if item.get('id') == item_id ]
        if index:
            self.data.get(key)[index[0]] = data
        self._save()

    def delete(self, key: str, item_id: str):
        index = [ idx for idx, item in enumerate(self.data.get(key)) 
                      if item.get('id') == item_id ]
        if index:
            self.data.get(key).pop(index[0])
            self._save()

    def get(self, key: str):
        return self.data.setdefault(key, [])

    def get_all(self):
        return self.data

    def clear(self):
        self.data = {}
        self._save()


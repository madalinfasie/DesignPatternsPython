"""
You had the idea of building a new cloud storage system (similar to Google Drive or Dropbox).
In order to do that, you first need a structure of files and folders to act upon.

Build the structure for the storage system that can do the following:
- Get the size of each folder and file
- Search for a file or folder by name
- Get the path of an item
"""

import abc
import os
import random
import typing as t


class Item(abc.ABC):
    @abc.abstractmethod
    def get_size(self) -> int:
        pass

    @abc.abstractmethod
    def search(self, name: str) -> t.List['Item']:
        pass

    @abc.abstractmethod
    def get_path(self) -> str:
        pass


class File(Item):
    def __init__(self, name: str, size: int, parent: Item = None):
        self.name = name
        self.size = size
        self.parent = parent

    def get_size(self) -> int:
        return self.size

    def search(self, name: str) -> t.List[Item]:
        return [self] if self.name == name else []

    def get_path(self) -> str:
        return os.path.join(self.parent.get_path(), self.name)

    def __repr__(self):
        return f'File({self.name})'


class Folder(Item):
    def __init__(self, name: str, parent: Item = None):
        self.name = name
        self.parent = parent
        self.items = []

    def add(self, item: Item):
        print(f'Creating item {item}...')
        item.parent = self
        self.items.append(item)

    def remove(self, item: Item):
        for component in self.items:
            if component.name == item.name:
                print(f'Removing the item {item}...')
                component.parent = None
                self.items.remove(component)

    def list_content(self) -> t.List[Item]:
        return self.items

    def get_size(self) -> int:
        return sum(item.get_size() for item in self.items)

    def search(self, name: str) -> t.List[Item]:
        results = []
        if self.name == name:
            results.append(self)

        for item in self.items:
            results.extend(item.search(name))

        return results

    def get_path(self) -> str:
        if not self.parent:
            return self.name

        return os.path.join(self.parent.get_path(), self.name)

    def __repr__(self):
        return f'Folder({self.name})'


def load_structure():
    """ The structure looks like this:
    root/
    ├── file01
    ├── file02
    ├── folder1
    │   └── file11
    └── folder2
        ├── file21
        └── folder21
            └── file22
    """
    root = Folder('root')

    folder1 = Folder('folder1')
    folder2 = Folder('folder2')
    folder21 = Folder('folder21')

    folder1.add(File('file11', size=10))
    folder2.add(File('file21', size=20))
    folder2.add(folder21)
    folder21.add(File('file22', size=30))

    root.add(File('file01', size=40))
    root.add(File('file02', size=50))
    root.add(folder1)
    root.add(folder2)

    return root


if __name__ == '__main__':
    root = load_structure()
    print('root.get_size', root.get_size())
    print('root content:', root.list_content())

    found_files = root.search('file11')
    file11 = found_files[0]
    print('Found items for name "file11": ', found_files)

    found_folders = root.search('folder21')
    folder21 = found_folders[0]
    print('folder21 content:', folder21.list_content())
    print('Size of folder21:', folder21.get_size())

    found_folders = root.search('folder21')
    print('folder21 content:', found_folders[0].get_path())

    file22 = root.search('file22')[0]
    print('file22 path:', file22.get_path())
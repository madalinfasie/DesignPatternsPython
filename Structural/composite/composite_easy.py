"""
You had the idea of building a new cloud storage system (similar to Google Drive or Dropbox).
In order to do that, you first need a structure of files and folders to act upon.

Build the structure for the storage system that can do the following:
- Get the size of each folder and file
- Search for a file or folder by name
"""

import abc
import typing as t


class Item(abc.ABC):
    @abc.abstractmethod
    def get_size(self) -> int:
        pass

    @abc.abstractmethod
    def search(self, name: str) -> t.List['Item']:
        pass


class File(Item):
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size  # This can be read from the file in real life

    def get_size(self) -> int:
        return self.size

    def search(self, name: str) -> t.List[Item]:
        return [self] if self.name == name else []

    def __repr__(self) -> str:
        return f'File({self.name})'


class Folder(Item):
    def __init__(self, name: str):
        self.name = name
        self.children = []

    def add(self, item: Item) -> None:
        print(f'Creating item {item}...')
        self.children.append(item)

    def remove(self, item: Item) -> None:
        for child in self.children:
            if child.name == item.name:
                print(f'Removing the item {item}...')
                self.children.remove(child)

    def list_content(self) -> t.List[Item]:
        return self.children

    def get_size(self) -> int:
        return sum(child.get_size() for child in self.children)

    def search(self, name: str) -> t.List[Item]:
        results = []
        if self.name == name:
            results.append(self)

        for child in self.children:
            results.extend(child.search(name))

        return results

    def __repr__(self) -> str:
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
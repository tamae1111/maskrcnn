import os

def printFileCount(dir):
    initial_count = 0
    for path in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, path)):
            initial_count += 1
    print("in printFileCount")
    print("file count is",initial_count)
    print("in dir ",dir)


if __name__ == '__main__':
    dir = "./"
    printFileCount(dir)
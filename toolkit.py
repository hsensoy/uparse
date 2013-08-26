__author__ = 'husnusensoy'


class FileLike(file):
    def __init__(self, filelike,strip=True):
        self.stripped = strip

        if type(filelike) == str:
            if filelike.endswith('.gz'):    #   gzip file
                import gzip
                self.fd = gzip.open(filelike, "r")
            else:
                self.fd = open(filelike,"r")
        elif type(filelike) == file:
                self.fd = filelike
        else:
            raise Exception("Unknown file like object")

    def __iter__(self):
        return self

    def next(self):
        if self.stripped:
            return self.fd.next().strip()
        else:
            return self.fd.next()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fd.close()


def readonlyopen(filelike):
    return FileLike(filelike)

if __name__ == "__main__":
    with open("german.embeddings.similarity.gz") as fp:
        with readonlyopen(fp) as ffp:
            for line in ffp:
                print line

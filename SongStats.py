import csv

with open('new_output.csv', 'r') as InputFile:
    FileReader = csv.DictReader(InputFile)
    TitleList = []
    ArtistList = []
    LyricList = []
    GenreList = []

    # title, artist, lyrics, genre
    for row in FileReader:
        TitleList.append(row['title'])
        ArtistList.append(row['artist'])
        LyricList.append(row['lyrics'][0:(len(row['lyrics']) - 1)].replace("\n", ""))
        GenreList.append(row['genre'])

    # Output totals.
    print("Total song titles: " + str(len(TitleList)))
    print("Total artists: " + str(len(ArtistList)))
    print("Total genres: " + str(len(GenreList)))

    # Output unique totals.
    print("\nTotal unique song titles: " + str(len(set(TitleList))))
    print("Total unique artists: " + str(len(set(ArtistList))))
    print("Total unique genres: " + str(len(set(GenreList))) + "\n")

    # Count number of songs per genre.
    for genre in set(GenreList):
        print("Total songs in " + str(genre) + " genre: " + str(GenreList.count(genre)))

        GenreTokens = []

        for g in range(len(GenreList)):
            if GenreList[g] == genre:
                for t in LyricList[g].split(" "):
                    GenreTokens.append(t)

        print("Total tokens: " + str(len(GenreTokens)))
        print("Total types: " + str(len(set(GenreTokens))))
        print("")

    # Count number of tokens
    tokens = []

    for song in LyricList:
        pieces = song.split(" ")

        for piece in pieces:
            tokens.append(piece)

    print("\nTotal number of tokens: " + str(len(tokens)))

    # Count number of types
    types = {}

    for t in tokens:
        if t in types:
            types[t] = types[t] + 1
        else:
            types[t] = 1

    print("Total number of types: " + str(len(types)))

    # Output average number of words per song.
    print("Average number of words per song: " + str(len(tokens) / len(TitleList)) + "\n")

    # Output top ten types.
    stypes = sorted(types, key=types.get, reverse=True)

    print("Top ten types: ")
    print("\tType\tCount")

    for i in range(10):
        print(str(i + 1) + "\t" + str(stypes[i]) + "\t" + str(types[stypes[i]]))

    ########################################
    # Most popular bigrams.

    import nltk
    from nltk.collocations import *

    bigram_measures = nltk.collocations.BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(tokens)

    print("\nTop ten bigrams:")
    print(sorted(finder.nbest(bigram_measures.raw_freq, 10)))

    print()

    print(sorted(finder.ngram_fd.items(), key=lambda t: (-t[1], t[0]))[:10])
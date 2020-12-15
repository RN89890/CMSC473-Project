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
        
"""
Total song titles: 1158
Total artists: 1158
Total genres: 1158

Total unique song titles: 1149
Total unique artists: 1007
Total unique genres: 15

Total songs in country genre: 48
Total tokens: 5083
Total types: 1607

Total songs in folk genre: 29
Total tokens: 2751
Total types: 1150

Total songs in new age genre: 3
Total tokens: 230
Total types: 133

Total songs in blues genre: 15
Total tokens: 1498
Total types: 596

Total songs in jazz genre: 35
Total tokens: 2890
Total types: 1059

Total songs in rap genre: 52
Total tokens: 14566
Total types: 5092

Total songs in latin genre: 18
Total tokens: 1602
Total types: 853

Total songs in reggae genre: 18
Total tokens: 3593
Total types: 1234

Total songs in metal genre: 88
Total tokens: 7816
Total types: 2848

Total songs in rock genre: 539
Total tokens: 53015
Total types: 8261

Total songs in electronic genre: 66
Total tokens: 6013
Total types: 1818

Total songs in pop genre: 160
Total tokens: 21850
Total types: 4305

Total songs in rnb genre: 52
Total tokens: 7841
Total types: 1801

Total songs in world genre: 5
Total tokens: 691
Total types: 368

Total songs in punk genre: 30
Total tokens: 2696
Total types: 1185


Total number of tokens: 132135
Total number of types: 17089
Average number of words per song: 114.10621761658031

Top ten types:
        Type    Count
1       im      1716
2       love    1369
3       know    1277
4       like    1104
5       get     869
6       got     840
7       oh      816
8       never   751
9       one     716
10      see     698
"""

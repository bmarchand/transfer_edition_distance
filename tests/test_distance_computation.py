from ted_module import transfer_edition_distance, transfer_edition_distance_unordered

def test_identical_small_networks():
    L = ["1 2 tree",
         "2 4 tree",
         "2 3 tree",
         "3 5 tree",
         "1 7 tree",
         "7 6 tree",
         "3 7 transfer"]

    d = transfer_edition_distance(L,L)

    assert(d == 0)

def test_small_networks1():
    L1 = ["1 2 tree",
          "2 4 tree",
          "2 3 tree",
          "3 5 tree",
          "1 7 tree",
          "7 6 tree",
          "3 7 transfer"]

    L2 = ["1 2 tree",
          "2 4 tree",
          "2 5 tree",
          "1 6 tree"]

    d = transfer_edition_distance(L1,L2)

    assert(d == 1)

def test_small_networks2():
    L1 = ["5 6 tree",
          "5 10 tree",
          "6 7 tree",
          "7 1 tree",
          "6 8 tree",
          "8 9 tree",
          "9 2 tree",
          "10 11 tree",
          "11 3 tree",
          "11 4 tree",
          "7 8 transfer",
          "9 10 transfer"
            ]
    
    L2 = ["5 6 tree",
          "6 8 tree",
          "8 1 tree",
          "6 11 tree",
          "11 9 tree",
          "9 2 tree",
          "5 7 tree",
          "7 10 tree",
          "10 3 tree",
          "10 4 tree",
          "8 9 transfer",
          "11 7 transfer"]

    d = transfer_edition_distance(L1,L2)

    assert(d == 2)

def test_small_networks3():
    L1 = ["1 2 tree",
          "2 3 tree",
          "3 4 tree",
          "4 5 tree",
          "5 6 tree",
          "6 7 tree",
          "1 8 tree",
          "8 9 tree",
          "9 10 tree",
          "10 11 tree",
          "11 12 tree",
          "12 13 tree",
          "2 9 transfer",
          "3 11 transfer",
          "4 12 transfer",
          "6 10 transfer"
          ]

    L2 = ["1 2 tree",
          "2 3 tree",
          "3 4 tree",
          "4 5 tree",
          "5 6 tree",
          "6 7 tree",
          "1 8 tree",
          "8 9 tree",
          "9 10 tree",
          "10 11 tree",
          "11 12 tree",
          "12 13 tree",
          "2 12 transfer",
          "3 9 transfer",
          "4 11 transfer",
          "6 8 transfer"
          ]

    d = transfer_edition_distance(L1,L2)

    assert(d == 2)

def test_small_unordered_networks1():
    L1 = ["1 2 tree",
          "2 3 tree",
          "2 4 tree",
          "1 5 tree",
          "5 6 tree",
          "5 7 tree",
          "2 5 transfer"]

    L2 = ["1 2 tree",
          "2 3 tree",
          "2 4 tree",
          "1 5 tree",
          "5 6 tree",
          "5 7 tree"]

    d = transfer_edition_distance_unordered(L1,L2)

    assert(d==1)

def test_small_unordered_networks2():
    
    L1 = ["7 5 tree",
          "5 1 tree",
          "5 2 tree",
          "7 6 tree",
          "6 3 tree",
          "6 4 tree",
          "5 6 transfer",
          "5 3 transfer"]

    L2 = ["7 6 tree",
          "6 5 tree",
          "5 1 tree",
          "5 2 tree",
          "6 3 tree",
          "7 4 tree",
          "5 3 transfer",
          "3 4 transfer"]

    d  = transfer_edition_distance_unordered(L1,L2)
    assert(d==3)

def test_small_unordered_networks3():
    
    L1 = open("tests/K00135_fitch.gr").readlines()[1:]
    L2 = open("tests/K00135_sankoff.gr").readlines()[1:]

    relabel = {}
    cnt = 0

    for line in L1+L2:
         u = line.split(' ')[0]
         v = line.split(' ')[1].rstrip('\n')
         try:
             relabel[u]
         except KeyError:
             relabel[u] = str(cnt)
         cnt += 1
         try:
             relabel[v]
         except KeyError:
             relabel[v] = str(cnt)
         cnt += 1

    L1 = [l.rstrip('\n') for l in L1] 
    L2 = [l.rstrip('\n') for l in L2] 

    L1 = [" ".join([relabel[l.split(" ")[0]], relabel[l.split(" ")[1]], l.split(" ")[2]]) for l in L1]
    L2 = [" ".join([relabel[l.split(" ")[0]], relabel[l.split(" ")[1]], l.split(" ")[2]]) for l in L2]

    d  = transfer_edition_distance_unordered(L1,L2)
    assert(d==13)

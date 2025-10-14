from ted_module import transfer_edition_distance

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

    assert(d == 1)

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

    assert(d == 4)

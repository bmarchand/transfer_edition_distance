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

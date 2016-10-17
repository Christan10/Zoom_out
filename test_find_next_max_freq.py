def find_next_max_freq(Hmat,k):
    """This function finds the tr_id which: has the maximum frequency, but doesn't exceeds the threshold k."""
    for r in range(len(Hmat)):
        row = Hmat[r]
        # we want to start with a row that has frequency lower than the threshold k
        if row[1] < k:
            max_freq = row[1]
            tr_id = row[0]
            for r in range(len(Hmat)):
                # we want to compare the row we started with every row in HMat in order to find the row with the maximum
                # frequency but also < k
                new_row = Hmat[r]
                if new_row[1] > max_freq and new_row[1] < k:
                    max_freq = new_row[1]
                    tr_id = new_row[0]
        return tr_id


H = [[1, 2], [2, 4], [3, 1], [7, 3], [5, 5]]
print (find_next_max_freq(H,4))

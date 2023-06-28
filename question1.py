def maximize_points(num_markers, markers):
    markers.sort(reverse=True)  # Sort marker values in descending order
    JamesScore = 0
    BobScore = 0
    turn = 0  # 0 for James, 1 for Bob

    while markers:
        if turn == 0:  # James' turn
            if markers[0] >= markers[-1]:
                JamesScore += markers.pop(0)
            else:
                JamesScore += markers.pop()
            turn = 1  # Bob's turn
        else:  # Bob's turn
            if markers[0] >= markers[-1]:
                BobScore += markers.pop(0)
            else:
                BobScore += markers.pop()
            turn = 0  # James' turn

    return JamesScore

# Reading input
num_markers = int(input())
markers = []
for _ in range(num_markers):
    markers.append(int(input()))

# Calling the function and printing the result
max_points = maximize_points(num_markers, markers)
print(max_points)

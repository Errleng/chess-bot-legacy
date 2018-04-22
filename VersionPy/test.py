def bin2dec(binary):
    num = 0
    for i in range(8):
        num += int(binary[i]) * (2 ** (7 - i))
    return num

input_sequences = []
for i in range(20):
    input_sequences.append(input())

# Valid ASCII
start_ASCII = 65
end_ASCII = 90
space_ASCII = 32

solutions = []

for seq_count in range(1, len(input_sequences), 2):
    input_sequence = input_sequences[seq_count]
    # print("Input sequence:", input_sequence)
    # print()

    sequence1, sequence2 = "", ""
    for letter in input_sequence:
        if letter == "C" or letter == "G":
            sequence1 += "1"
            sequence2 += "0"
        else:
            sequence1 += "0"
            sequence2 += "1"

    # print(sequence1)
    # print(sequence2)

    start_index = 0

    # print("FIRST SEQUENCE")

    for loop in range(7):
        current_sequence = sequence1[start_index:]
        # print("Current sequence:", current_sequence)
        # print("Sequence length:", len(current_sequence))
        binary_ASCII = []

        for i in range(len(current_sequence)):
            index = i + 1
            if index % 8 == 0 and i > 0:
                binary_ASCII.append(current_sequence[index - 8:index])
        # print(binary_ASCII)

        ASCII = []

        found_solution = True
        for binary in binary_ASCII:
            decimal = bin2dec(binary)
            if decimal == space_ASCII or start_ASCII <= decimal <= end_ASCII:
                ASCII.append(chr(bin2dec(binary)))
            else:
                # print("Invalid sequence", current_sequence)
                def R1_P2_2014():
                    def bin2dec(binary):
                        num = 0
                        for i in range(8):
                            num += int(binary[i]) * (2 ** (7 - i))
                        return num

                    input_sequences = []
                    for i in range(20):
                        input_sequences.append(input())

                    # Valid ASCII
                    start_ASCII = 65
                    end_ASCII = 90
                    space_ASCII = 32

                    solutions = []

                    for seq_count in range(1, len(input_sequences), 2):
                        input_sequence = input_sequences[seq_count]
                        # print("Input sequence:", input_sequence)
                        # print()

                        sequence1, sequence2 = "", ""
                        for letter in input_sequence:
                            if letter == "C" or letter == "G":
                                sequence1 += "1"
                                sequence2 += "0"
                            else:
                                sequence1 += "0"
                                sequence2 += "1"

                        # print(sequence1)
                        # print(sequence2)

                        start_index = 0

                        # print("FIRST SEQUENCE")

                        for loop in range(7):
                            current_sequence = sequence1[start_index:]
                            # print("Current sequence:", current_sequence)
                            # print("Sequence length:", len(current_sequence))
                            binary_ASCII = []

                            for i in range(len(current_sequence)):
                                index = i + 1
                                if index % 8 == 0 and i > 0:
                                    binary_ASCII.append(current_sequence[index - 8:index])
                            # print(binary_ASCII)

                            ASCII = []

                            found_solution = True
                            for binary in binary_ASCII:
                                decimal = bin2dec(binary)
                                if decimal == space_ASCII or start_ASCII <= decimal <= end_ASCII:
                                    ASCII.append(chr(bin2dec(binary)))
                                else:
                                    # print("Invalid sequence", current_sequence)
                                    found_solution = False
                                    break
                            if found_solution:
                                solutions.append(ASCII)
                            # if ASCII != []:
                            # print(ASCII)
                            start_index += 1

                        start_index = 0

                        # print("SECOND SEQUENCE")

                        for loop in range(7):
                            current_sequence = sequence2[start_index:]
                            # print("Current sequence:", current_sequence)
                            # print("Sequence length:", len(current_sequence))
                            binary_ASCII = []

                            for i in range(len(current_sequence)):
                                index = i + 1
                                if index % 8 == 0 and i > 0:
                                    binary_ASCII.append(current_sequence[index - 8:index])
                            # print(binary_ASCII)

                            ASCII = []

                            found_solution = True
                            for binary in binary_ASCII:
                                decimal = bin2dec(binary)
                                if decimal == space_ASCII or start_ASCII <= decimal <= end_ASCII:
                                    ASCII.append(chr(bin2dec(binary)))
                                else:
                                    # print("Invalid sequence", current_sequence)
                                    found_solution = False
                                    break
                            if found_solution:
                                solutions.append(ASCII)

                            # if ASCII != []:
                            # print(ASCII)
                            start_index += 1

                    # print("SOLUTIONS")
                    for solution in solutions:
                        print("".join(solution))

                found_solution = False
                break
        if found_solution:
            solutions.append(ASCII)
        # if ASCII != []:
        # print(ASCII)
        start_index += 1

    start_index = 0

    # print("SECOND SEQUENCE")

    for loop in range(7):
        current_sequence = sequence2[start_index:]
        # print("Current sequence:", current_sequence)
        # print("Sequence length:", len(current_sequence))
        binary_ASCII = []

        for i in range(len(current_sequence)):
            index = i + 1
            if index % 8 == 0 and i > 0:
                binary_ASCII.append(current_sequence[index - 8:index])
        # print(binary_ASCII)

        ASCII = []

        found_solution = True
        for binary in binary_ASCII:
            decimal = bin2dec(binary)
            if decimal == space_ASCII or start_ASCII <= decimal <= end_ASCII:
                ASCII.append(chr(bin2dec(binary)))
            else:
                # print("Invalid sequence", current_sequence)
                found_solution = False
                break
        if found_solution:
            solutions.append(ASCII)

        # if ASCII != []:
        # print(ASCII)
        start_index += 1

# print("SOLUTIONS")
for solution in solutions:
    print("".join(solution))

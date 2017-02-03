with open('rankg.test', 'r') as infile:
    with open('rankg2.test', 'w') as outfile:
        for line in infile:
            for i in range(3):
                newline = ''
                for char in line.strip():
                    if char != '\n':
                        for j in range(3):
                            newline += char
                newline += '\n'
                outfile.write(newline)

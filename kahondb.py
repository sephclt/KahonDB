import sys
import os
import re

option = ""
destination = ""
program_filepath = ""

if len(sys.argv) > 2:
    option = sys.argv[1]
    destination = sys.argv[2]
    program_filepath = sys.argv[3]
else:
    program_filepath = sys.argv[1]

if program_filepath == "--help":
    print("kahonpapel.py [option] [destination] [program]")
    print("Options:")
    print("\t-d: Create directories and files in destination")
    sys.exit(0)

if program_filepath.endswith(".kdb") is False:
    print("Error: Invalid File Extension")
    sys.exit(1)

# read arguments from command line
program_lines = []
with open(program_filepath, "r") as program_file:
    program_lines = [line.strip() for line in program_file.readlines()]


program = []
kahons = {}
aparadors = {}
memory = []

line_counter = 0
token_counter = 0

for line in program_lines:
    parts = re.split(r'\s+(?=(?:[^"]*"[^"]*")*[^"]*$)', line)
    opcode = parts[0]

    # if opcode is a comment ignore the line
    if opcode == "--":
        line = ""
        line_counter += 1
        continue

    # check if line is empty
    if opcode == "":
        line_counter += 1
        continue

    # store opcode token
    # program.append(opcode)
    line_counter += 1
    token_counter += 1

    if opcode == "[=]":
        aparador = parts[1]

        # check if aparador already exists
        for cab in aparadors:
            if aparador == cab:
                print(
                    "Error at line " + str(line_counter) + ": aparador Already Exists"
                )
                sys.exit(1)

        aparadors[aparador] = set()

        # check if followed by an action
        if len(parts) > 2:
            action = parts[2]

            if action == "=>":
                kahon = parts[2]

                if kahon not in kahons:
                    print("Error at line " + str(line_counter) + ": kahon Not Found")
                    sys.exit(1)

    if opcode == "[]":
        kahon = parts[1]

        # check if kahon already exists
        for cont in kahons:
            if kahon == cont:
                print("Error at line " + str(line_counter) + ": kahon Already Exists")
                sys.exit(1)

        if len(parts) <= 2:
            print("Error at line " + str(line_counter) + ": No Action Specified")
            sys.exit(1)

        action = parts[2]

        if action == "=>":
            for val in parts[3:]:
                if val == "|":
                    val = ""
                else:
                    memory.append(val)

            kahons[kahon] = memory
            memory = []

    if opcode in aparadors:
        action = parts[1]

        if len(parts) <= 1:
            print("Error at line " + str(line_counter) + ": No kahon Specified")
            sys.exit(1)

        if action not in ["=>", "->", "~>"]:
            print("Error at line " + str(line_counter) + ": Invalid Action")
            sys.exit(1)

        # Insert action
        for kahon in parts[2:]:
            if kahon == "|":
                kahon = ""
            else:
                if kahon in aparadors:
                    print(
                        "Error at line "
                        + str(line_counter)
                        + ": Cannot Insert aparador into Cabinet"
                    )
                    sys.exit(1)

                if kahon not in kahons:
                    print("Error at line " + str(line_counter) + ": kahon Not Found")
                    sys.exit(1)

                # Check if kahon is already in aparador
                if action == "=>":
                    for existing_kahon in aparadors[opcode]:
                        if existing_kahon == kahon:
                            print(
                                "Warning at line "
                                + str(line_counter)
                                + ": Performed a double insert"
                            )
                            continue

                    aparadors[opcode].add(kahon)
                elif action == "->":
                    aparadors[opcode] = set()
                    aparadors[opcode].add(kahon)

                elif action == "~>":
                    if kahon not in aparadors[opcode]:
                        print(
                            "Error at line "
                            + str(line_counter)
                            + ": kahon Not Found in aparador"
                        )
                        sys.exit(1)
                    else:
                        aparadors[opcode].remove(kahon)

    if opcode in kahons:
        action = parts[1]

        if len(parts) <= 1:
            print("Error at line " + str(line_counter) + ": No kahon Specified")
            sys.exit(1)

        if action not in ["=>", "->", "~>"]:
            print("Error at line " + str(line_counter) + ": Invalid Action")
            sys.exit(1)

        if action == "=>":
            for val in parts[2:]:
                if val == "|":
                    val = ""
                else:
                    if val in aparadors:
                        print(
                            "Error at line "
                            + str(line_counter)
                            + ": Cannot Insert aparador into kahon"
                        )
                        sys.exit(1)

                    if val in kahons:
                        print(
                            "Error at line "
                            + str(line_counter)
                            + ": Cannot Insert kahon into kahon"
                        )
                        sys.exit(1)

                    if val in kahons[opcode]:
                        print(
                            "Warning at line "
                            + str(line_counter)
                            + ": Duplicate Value Inserted into kahon"
                        )

                    kahons[opcode].append(val)

        elif action == "->":
            kahons[opcode] = []
            for val in parts[2:]:
                if val == "|":
                    val = ""
                else:
                    if val in aparadors:
                        print(
                            "Error at line "
                            + str(line_counter)
                            + ": Cannot Insert aparador into kahon"
                        )
                        sys.exit(1)

                    if val in kahons:
                        print(
                            "Error at line "
                            + str(line_counter)
                            + ": Cannot Insert kahon into kahon"
                        )
                        sys.exit(1)

                    if val in kahons[opcode]:
                        print(
                            "Warning at line "
                            + str(line_counter)
                            + ": Duplicate Value Inserted into kahon"
                        )

                    kahons[opcode].append(val)

        elif action == "~>":
            for val in parts[2:]:
                if val == "|":
                    val = ""
                elif val not in kahons[opcode]:
                    print(
                        "Error at line "
                        + str(line_counter)
                        + ": Value Not Found in kahon"
                    )
                    sys.exit(1)
                else:
                    kahons[opcode].remove(val)

    if opcode == "==":
        if aparadors == {} and kahons == {}:
            print(
                "Error at line " + str(line_counter) + ": No aparadors or kahons Found"
            )
            sys.exit(1)

        if aparadors != {}:
            print("aparadors: " + str(aparadors))

        if kahons != {}:
            print("kahons: " + str(kahons))

    if (
        opcode not in aparadors
        and opcode not in kahons
        and opcode not in ["[]", "[=]", "=="]
    ):
        print("Error at line " + str(line_counter) + ": Invalid Opcode")
        sys.exit(1)

filename = os.path.splitext(program_filepath)[0] + ".kahon"

if option == "-d":
    for aparador in aparadors:
        os.mkdir(destination + "/" + aparador)
        for kahon in aparadors[aparador]:
            os.mkdir(destination + "/" + aparador + "/" + kahon)
            for val in kahons[kahon]:
                with open(
                    destination + "/" + aparador + "/" + kahon + "/" + val, "w"
                ) as file:
                    file.write(val)
    sys.exit(0)


with open(filename, "w") as program_file:
    for aparador in aparadors:
        program_file.write(aparador + " {\n")
        for kahon in sorted(aparadors[aparador]):
            program_file.write("\t" + kahon + ":\n")
            for val in kahons[kahon]:
                program_file.write("\t\t- " + val + ",\n")
        program_file.write("},\n")
    sys.exit(0)

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
# read arguments from command line

program_lines = []
with open(program_filepath, 'r') as program_file:
    program_lines = [line.strip() for line in program_file.readlines()]


program = []
containers = {}
cabinets = {}
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
        cabinet = parts[1]

        # check if cabinet already exists
        for cab in cabinets:
            if cabinet == cab:
                print("Error at line " + str(line_counter) + ": Container Already Exists")
                sys.exit(1)

        cabinets[cabinet] = set()

        # check if followed by an action
        if len(parts) > 2:
            action = parts[2]

            if action == "=>":
                container = parts[2]

                if container not in containers:
                    print("Error at line " + str(line_counter) + ": Container Not Found")
                    sys.exit(1)

    if opcode == "[]":
        container = parts[1]

        # check if container already exists
        for cont in containers:
            if container == cont:
                print("Error at line " + str(line_counter) + ": Container Already Exists")
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

            containers[container] = memory
            memory = []

    if opcode in cabinets:
        if len(parts) <= 1:
            print("Error at line " + str(line_counter) + ": No Container Specified")
            sys.exit(1)

        for container in parts[2:]:
            if container == "|":
                container = ""
            else:
                if container in cabinets:
                    print("Error at line " + str(line_counter) + ": Cannot Insert Cabinet into Cabinet")
                    sys.exit(1)

                if container not in containers:
                    print("Error at line " + str(line_counter) + ": Container Not Found")
                    sys.exit(1)

                # Check if container is already in cabinet
                for existing_container in cabinets[opcode]:
                    if existing_container == container:
                        print("Warning at line " + str(line_counter) + ": Performed a double insert")

                cabinets[opcode].add(container)

    if opcode in containers:
        action = parts[1]

        if len(parts) <= 1:
            print("Error at line " + str(line_counter) + ": No Container Specified")
            sys.exit(1)

        if action not in ["=>", "->"]:
            print("Error at line " + str(line_counter) + ": Invalid Action")
            sys.exit(1)

        for val in parts[2:]:
            if val == "|":
                val = ""
            else:
                if val in cabinets:
                    print("Error at line " + str(line_counter) + ": Cannot Insert Cabinet into Container")
                    sys.exit(1)

                if val not in containers[opcode]:
                    print("Warning at line " + str(line_counter) + ": Performed a double insert")

                containers[opcode].append(val)

    if opcode == "==":
        cab = parts[1]

        if cab not in cabinets:
            print("Error at line " + str(line_counter) + ": Cabinet Not Found")
            sys.exit(1)

filename = os.path.splitext(program_filepath)[0] + ".kahon"

if option == "-d":
    for cabinet in cabinets:
        os.mkdir(destination + "/" + cabinet)
        for container in cabinets[cabinet]:
            os.mkdir(destination + "/" + cabinet + "/" + container)
            for val in containers[container]:
                with open(destination + "/" + cabinet + "/" + container + "/" + val, 'w') as file:
                    file.write(val)
    sys.exit(0)


with open(filename, 'w') as program_file:
    for cabinet in cabinets:
        program_file.write(cabinet + " {\n")
        for container in cabinets[cabinet]:
            program_file.write("\t" + container + ":\n")
            for val in containers[container]:
                program_file.write("\t\t- " + val + ",\n")
        program_file.write("},\n")
    sys.exit(0)

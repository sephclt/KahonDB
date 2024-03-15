# KahonDB
KahonDB is a simple database implementation in python. Created as a finals project for the course Automata Theory and Formal Languages
## Installation
Simple clone the repository to your local machine
```bash
git clone https://github.com/sephclt/KahonDB
```
## Usage
The database is simple to use. A sample code is provided.
### How to run
```bash
python3 kahondb.py <filename>
```
#### Example
```bash
python3 kahondb.py sample-code.ist
```
### Filetype
The database uses `.kdb` as its file extension. The database produces `.kahon` files as its output.
### Keywords
- `--` : comment
- `[=]` : create a cabinet
- `[]` : create container
- `=>` : insert symbol
- `->` : replace symbol
- `==` : display symbol
- `|` : AND symbol

## Todo
- [x] make cabinets hold multiple containers
- [ ] prevent containers from holding containers
- [ ] implement replace action
- [ ] display cabinets and container in alphabetical order

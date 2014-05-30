from pyparsing import LineEnd, oneOf, Word, nums, Combine, restOfLine, \
    alphanums, Suppress, empty, originalTextFor, OneOrMore, alphas, \
    Group

fin = open('uData.txt', 'r')
data = fin.read()
fin.close()

fout = open('sData.txt', 'w')


NL = LineEnd().suppress()  # LineEnd.suppress()
gender = oneOf("M F")      # Sets the possible genders
integer = Word(nums)       # Define what integer is
date = Combine(integer + '/' + integer + '/' + integer)

# Define the line definitions
gender_line = gender("sex") + NL
dob_line = date("DOB") + NL
name_line = restOfLine("name") + NL
id_line = Word(alphanums + '-')("ID") + NL
recnum_line = integer("recnum") + NL

# Define forms of address lines
first_addr_line = Suppress('.') + empty + restOfLine + NL
# Subsequent address line is not gender
subsq_addr_line = ~(gender_line) + restOfLine + NL

# a line with a name and a recnum combined, if no ID
name_recnum_line = originalTextFor(OneOrMore(Word(alphas + ',')))("name") + \
    integer("recnum") + NL

# Defining the form of an overall record, either with or without an ID
record = Group((first_addr_line + ZeroOrMore(subsq_addr_line))("address") + \
    gender_line + dob_line + ((name_line + id_line + recnum_line) | \
    name_recnum_line))

# Parse Data
records = OneOrMore(record).parseString(data)

# output the desired results (note that address is actually a list of lines)

for rec in records:
    if rec.ID:
        fout.write("%(name)s, %(ID)s, %(address)s, %(sex)s, %(DOB)s\n" % rec)
    else:
        fout.write("%(name)s, , %(address)s, %(sex)s, %(DOB)s\n" % rec)
print

# how to access the individual fields of the parsed record
for rec in records:
    print rec.dump()
    print rec.name, 'is', rec.sex
    print
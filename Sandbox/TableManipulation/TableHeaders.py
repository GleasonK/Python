__author__ = 'Kevin Gleason'

### ORIGINAL INPUT
# fin = open("table060614.csv",'rb').readline()
#
# labels = fin.split(",")
#
# print labels
# shorts = ["aid","p","","tstamp","e","evn","eid","tid","tna","tv","","","uid","","","","","","","","","","","","url","",
#           "refr"]

### POST PROCESSED INPUT
fin = open("tableRelation.csv", 'rb').read()
fsplit = fin.rsplit()
zipListA=[]
zipListB=[]
for item in fsplit:
    tmp=item.split(",")
    zipListA.append(tmp[0])
    zipListB.append(tmp[1])
print zipListA
print zipListB
zList = zip(zipListA,zipListB)

table_map = []
for sh,lo in zList:
    if sh is not "":
        table_map.append(sh+"="+lo)
print table_map

fout = open('propMap','wb')
for item in table_map:
    fout.write(item + "\n")




# for x,y in fin.rsplit():
#     print x + ":" + y



### SAMPLE OUTPUT
# out = open ("tableRelation.csv", 'wb')
# for item in labels:
#     out.write(item + "\n")
#
# out.close()
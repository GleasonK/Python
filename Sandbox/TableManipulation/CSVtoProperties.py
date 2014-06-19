__author__ = 'Kevin Gleason'

### TABLE OF RELATED INPUT
class CSVtoProperties(object):
    '''
    Given an excel CSV of relations between the shorthand notation of the keys from
    and HTTP GET request and their full names as stored in the database table in the order
    [shorthand, fullname], returns a propMap file that can be loaded to a map in Java using
    the Properties class.
    '''
    def makeProperties(self, file_in_name="tableRelation.csv", file_out_name="propMap"):
        '''
        The main function. Returns nothing, makes a file in current directory of map properties.
        '''
        fin = open(file_in_name, 'rb').read().rsplit()
        fout = open(file_out_name+".properties", "wb")
        for item in fin:
            tmp=item.split(",")
            if tmp[0] is not "":
                fout.write(tmp[0]+"="+tmp[1]+"\n")

if __name__=="__main__":
    propWriter = CSVtoProperties()
    propWriter.makeProperties()
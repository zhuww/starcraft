import numpy
from numpy import double
def tofile(filename,*args):
        f = open(filename,"w")
        length=[]
        #print args
        for col in args:
                #print col
                length.append(len(col))
        def ithitem(i,*pargs):
                items=[]
                for table in pargs:
                        for col in table:
                                #print i,col[i]
                                items.append(col[i])
                return items
        for i in range(min(length)):
                outputline=''
                for item in ithitem(i,args):
                        outputline=outputline+"%s " % item
                print >> f, outputline
                #f.write(formatstr % ithitem(i,args))
        f.close()
        return len(length)

def readcol(file,n):
        res=[]
        infile = open(file,"r")
        array = infile.readlines()
        for line in array:
                line = line.split()
                try:
                    res.append(int(line[n]))
                except ValueError:
                    res.append(line[n])

        return numpy.array(res)

if __name__ == '__main__':
    print "supported functions:"
    print "readcol(filename,N)"
    print "tofile(filename,*arrays)"

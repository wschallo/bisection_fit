def writeToFile(to_write,path):
    with open(path,'a') as f:
        f.write("{}\n".format(to_write))
    f.close()
        

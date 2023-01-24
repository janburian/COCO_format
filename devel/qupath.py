import javaobj.v1 as javaobj

def read_file(filename:str):
    file = open(filename, "rb")
    data = file.read()
    file.close()
    return data

if __name__ == '__main__':
    filename = "data.qpdata"
    jobj = read_file(filename)
    pobj = javaobj.loads(jobj)
    print(pobj)


from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?
message = b'gAAAAABb93ETA72nThi2COXNl0EJwqnJ01Gr3HAtkY0RY3NwhFHo2Zg2QreKjlPDF6uhElUzKeNXusrb0G-V3PE3ckSmmUdTjgWcO5wFQw99E02cTZXF2sXjG1Z5MrlvBfodYaZlgty4mxUfqy0hZdlweBH3_Wfh8j_9VMiq12xs90oFWoJ4n5dlZ6Jyg35xi7b-3xGCX-cg'

def main():
    f = Fernet(key)
    print(f.decrypt(message))


if __name__ == "__main__":
    main()

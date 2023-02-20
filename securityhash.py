import bcrypt


class Hash:
    def hash(self, x):
        # converting password to array of bytes
        bytes = x.encode("utf-8")

        # generating the salt
        salt = bcrypt.gensalt()

        # Hashing the password
        hashed = bcrypt.hashpw(bytes, salt)

        return hashed.decode("utf-8")

#The code below is me testing the security implementation of bcrypt

#x = Hash()

#password = "password1".encode("utf-8")
#hashDecoded = x.hash("password1")
#hashEncoded1 = hashDecoded.encode("utf-8")
#hashEncoded2 = x.hash("password1").encode("utf-8")
#storedindatabase1 = hashEncoded1
#storedindatabase2 = hashEncoded2


#print(password)
#print("Decoded:")
#print(hashDecoded)
#print("Encoded 1 : ")  
#print(hashEncoded1 )
#print("Encoded 2 : ")  
#print(hashEncoded2)
#print(bcrypt.checkpw("password1".encode("utf-8"), storedindatabase1))
#rint(bcrypt.checkpw("password1".encode("utf-8"), storedindatabase2))
      







        

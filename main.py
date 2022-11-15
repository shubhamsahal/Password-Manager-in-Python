from cryptography.fernet import Fernet


class PasswordManager:

    def __init__(self):
        self.key = None
        self.password_file = None                       # This make encrypted key of your password
        self.password_dict = {}            # this is the password dictionary

    def create_key(self, path):
        self.key = Fernet.generate_key()
        with open(path, 'wb') as f:                        # This will create our key and store into file
            f.write(self.key)

    def load_key(self , path):
        with  open(path,'rb') as f:
            self.key = f.read()

    def create_password_file(self, path , initial_values=None):
        self.password_file = path

        if initial_values is not None:                                    #list of tuples key value
            for key, value in initial_values.items():
                self.add_password(key, value)

    def load_password_file(self, path):
        self.password_file = path

        with open(path, 'r') as f:
            for line in f:
                site, encrypted = line.split(":")
                self.password_dict[site] = Fernet(self.key).decrypt(encrypted.encode()).decode()


    def add_password(self, site, password):
        self.password_dict[site] = password

        if self.password_file is not None:
           with open(self.password_file,'a+') as f:
            encrypted = Fernet(self.key).encrypt(password.encode())
            f.write(site + ":"+ encrypted.decode() + "\n")

    def get_password(self, site):
        return self.password_dict[site]

def main():
    password = {
        "email": "1234567",
        "facebook": "myfbpassword",
        "youtube": "helloworld123",
        "something": "myfavouritepassword_123"
    }

    pm = PasswordManager()

    print(""" What Do You Want To  Do ?
    (1) Create a New Key
    (2) Load and existing Key
    (3) Create New Password File
    (4) Load existing Password File
    (5) Add a New Password
    (6) Get a Password
    (7) Quit
    """)

    done = False

    while not done:

        choice = input("Enter  Your Choice : ")
        if choice == "1":
            path = input("Enter Path : ")
            pm.create_key(path)
        elif choice == "2":
            path  = input ("Enter Path :")
            pm.load_key(path)
        elif choice == "3":
            path = input ("Enter path :")
            pm.create_password_file(path, password)
        elif choice == "4":
            path = input ("Enter Path :")
            pm.load_password_file(path)
        elif choice == "5":
            site = input ("Enter  the Site : ")
            password = input ("Enter the Password : ")
            pm.add_password(site,password)
        elif choice == "6":
            site = input ("What Site do you want : ")
            print(f"password  for {site} is {pm.get_password(site)}")
        elif choice == "q":
            done = True
            print(" BYE ")
        else:
            print("Invalid Choice ! ")



if __name__=="__main__":
    main()
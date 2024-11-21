#File integrity checker
import pandas as pd
import os, hashlib, argparse,datetime
from colorama import init, Fore

#initializing colorama
init()

database_file_path = r"C:\Users\USER\Desktop\python\intergrity_databaase.xlsx"

#Create an excel file that will be used as the database
if not os.path.exists(database_file_path):
    df = pd.DataFrame({
        "Filename":[],
        "Hash":[],
        "Size":[],
        "Alogrithm":[],
        "File Path": [],
        "Date Added":[]
    })
    df.to_excel(database_file_path, engine='openpyxl', index=False)
    print(Fore.Green+ f"{database_file_path} File created")
        
#initializing the parser      
parser = argparse.ArgumentParser(description="File intergrity checker")

#required flags
parser.add_argument("path", type=str, help="File path")

#optional flags 
parser.add_argument("-a","--add", action="store_true", help="Add file hash to database")
parser.add_argument("-c","--check", action="store_true", help="Checks for file intergrity on the database")

args = parser.parse_args()
file_path = args.path

#Create the file hash of the path given by the user
def open_file(file_path):
    filename = ""
    hash_value = ""
   
    if os.path.exists(file_path):
        #Checking for file size
        file_bytes = os.path.getsize(file_path)
        file_kilobytes =  f"{file_bytes / 1024:.2f} KB"
        file_megabytes = f"{file_bytes / 1000000:.2f} MB"
        file_size = f"{file_megabytes if file_bytes >= 1000000 else file_kilobytes}"
        
        with open(file_path, "rb") as file:
            content = file.read()
            path = file.name
            filename = path.split('\\')[-1]
            md5 = hashlib.md5()
            md5.update(content)
            hash_value = md5.hexdigest()
            
        return {"filename":filename,"hash_value":hash_value,"file_size":file_size}
    else:
        print(Fore.RED + "File does not exit on this pc")
        exit()


#checks if the file given exists in the database
def check_file_exits(database_file_path,filename):
    df = pd.read_excel(database_file_path)
    index = df[df["Filename"] == filename].index
    if not index.empty:
        return True
    else:
        return False

#Adding new filename and hash to the database
def add_new_hash(database_file_path,filename,hash_value,file_path,file_size):
    current_datetime = datetime.datetime.now()
    current_date = current_datetime.strftime("%d-%m-%Y %H:%M:%S")
    
    #Data format stored in the database
    data = {
        "Filename":[filename],
        "Hash":[hash_value],
        "Size":[file_size],
        "Alogrithm":["md5"],
        "File Path": [file_path],
        "Date Added":[current_date]
    }

    #initializing the DataFrame from Pandas with the data above
    df = pd.DataFrame(data)
    
    if not check_file_exits(database_file_path,filename):
        #Reading the existing data from the database and adding the new data and putting it back into the excel file
        existing_df = pd.read_excel(database_file_path)
        combined_df = pd.concat([existing_df,df])
        combined_df.to_excel(database_file_path,index=False)
        
        print(f"Filename: {filename} Hash: {hash_value} File Path: {file_path} Date Added: {current_date}")
        print(Fore.GREEN + "Data Added succesfully!!!")
    else:
        print(Fore.RED + f"{filename} already exits in the database!!!")


#Comparing the file hash in the database to see if the file has been modified
def check_file_intergrity(database_file_path,filename,hash_value,file_path):
    
    if check_file_exits(database_file_path,filename):
        df = pd.read_excel(database_file_path)
        index = df[df["Filename"] == filename].index
        existing_hash = df.at[index[0], "Hash"]
        compared_hash = existing_hash == hash_value
        
        print(f"Filename: {filename} || Filename in Database: {df.at[index[0],"Filename"]}")
        print(f"File Hash: {hash_value} || File Hash in Database: {df.at[index[0],"Hash"]}")
        
        #checking if the compared hash doesn't match
        if compared_hash:
            print(Fore.GREEN + "File has not been changed")
        else:
            print(Fore.RED + "File has been tampared with or changed")

    else:
        print(Fore.RED + f"\"{filename}\" does not exits in the Database!!!\n Please use --add / -a to add  or use --help / -h for help instead.")



if args.add:
    #Checking if the file path given is a directory
    isDirectory = os.path.isdir(file_path)
    if isDirectory:
        #Getting the content of the Directory
        dir_content = os.listdir(file_path)
        
        #Tracking the number of files in the directory
        files_in_directory = 0
        
        #Geting all the files in the directory and adding it to the database
        for file in range(0, len(dir_content)):
            new_file_path = f"{file_path}\\{dir_content[file]}"
            
            #Getting only the files in the directory
            if os.path.isfile(new_file_path):
                files_in_directory += 1
                opened_file = open_file(new_file_path)
                filename,hash_value,file_size = opened_file["filename"],opened_file["hash_value"],opened_file["file_size"]
                add_new_hash(database_file_path,filename,hash_value,new_file_path,file_size)
        print(Fore.BLUE + f"{files_in_directory} files found!")
    else:
        filename,hash_value,file_size = open_file(file_path)["filename"],open_file(file_path)["hash_value"],open_file(file_path)["file_size"]
        add_new_hash(database_file_path,filename,hash_value,file_path,file_size)
    
elif args.check:
    filename,hash_value = open_file(file_path)["filename"],open_file(file_path)["hash_value"]
    check_file_intergrity(database_file_path,filename,hash_value,file_path)


    

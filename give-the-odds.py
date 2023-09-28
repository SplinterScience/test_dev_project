import sys
from test_dev_app.Logic.main import main

if __name__ == "__main__":
    # sys.path.append('./')
    if len(sys.argv)!=3:
        print("Incorrect number of arguments, please provide the path for millennium_falcon json then the path of the empire json file")
    
    file1_path = str(sys.argv[1])
    file2_path = str(sys.argv[2])

    sucess_proba=main(file2_path,file1_path)

    print("The survival probability is "+str(sucess_proba))
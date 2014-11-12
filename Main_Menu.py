from Prescription import Prescription
from Medical_Test import Medical_Test
from Patient_Info_Update import Patient_Info_Update
from Search_Engine import SearchEngine

# takes a boolean first, if it is being run after a failed attempt
def display(first):
    print()
    print("[1] Prescribe a medical test.")
    print("[2] Enter medical test information.")
    print("[3] Update patient information.")
    print("[4] Perform searches.")
    print("[5] Exit.")
    if first:
        return
    else:
        print("INVALID INPUT.")
        return
    
# returns 0 on an invalid input, returns int of the input if valid
def input_check(input):
    try:
        check = eval(input)    
        if check not in [1,2,3,4,5]:
            return 0
        else:
            return check
    except:
        return 0
    
# takes an int input 1-4    
def run(input):
    if input == 1:
        pres = Prescription()
        success = pres.main()
    elif input == 2:
        medt = Medical_Test()
        success = medt.main()
    elif input == 3:
        piu = Patient_Info_Update()
        success = piu.main()
    elif input == 4:
        search = Search_Engine()
        success = search.main()
    return success
        
    
def main():
    first = 1
    
    while 1:
        display(first)
        selection = input("Enter an option (1-5): ")
        check = input_check(selection)
        if check == 0: 
            first = 0
            print(chr(27) + "[2J")
        elif check == 5:
            print("Program closing, thank you.")
            return
        else:
            first = run(eval(selection))

if __name__ == "__main__":
    main()
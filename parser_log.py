import sys, json, datetime

general_fields = {
    "ProjectName": '',
    "Frameworks": '',
    "Source_files": '',
    "Lines_of_code": '',
}

def get_general_fields(line):
    if "ProjectName is" in line:
        general_fields["ProjectName"] = line.split()[-1]
    if "The following frameworks were found" in line:
        general_fields["Frameworks"] = line.split("[")[-1].split("]")[0]
    if "The following source files were identified" in line:
        general_fields["Source_files"] = line.split(":")[-1].split("\n")[0]
    if "Scanning or Auditing Project type code is" in line:
        general_fields["Lines_of_code"] = line.split("has")[1].split()[0]

def get_elements_gqs():
    flag = 0
    file = open(sys.argv[1], "r", encoding='windows-1252')
    lines = file.readlines()
    for line in lines:
        if "End General Queries Summary" in line:
            flag = 0
        elif  "General Queries Summary" in line:
            flag = 1
            continue
        elif "\n" == line:
            flag = 0
        if flag == 1:
            general_fields["_".join(line.split()[0].split("_")[:-1])] = line.split()[8]
    file.close()
        
def get_elements_query():
    file = open(sys.argv[1], "r", encoding='windows-1252')
    lines = file.readlines()
    for line in lines:
        if line.startswith("Query") and "Java.Test_team.Java_High_Risk" in line:
            general_fields[line.split()[2]] = [" ".join(line.split()[6:8]), " ".join(line.split()[8:11])]
    file.close()
    
def json_to_file():
    file = open(f'{datetime.datetime.now()}-output.json', "w+")
    file.write(json.dumps(general_fields))
    file.close()
    

def logger():
    with open(sys.argv[1], "r", encoding='windows-1252') as file:
        for line in file:
            get_general_fields(line)
    get_elements_gqs()
    get_elements_query()
    json_to_file()


if __name__ == '__main__':
    logger()
import re
import jsonlines
import random

def add_indentation(level):
    res = str()
    for i in range(level):
        res += "    "
    return res

def process_judge(judge):
    judge = judge.strip()
    res = str()
    judge = judge.split(";")
    if len(judge) < 2:
        raise SyntaxError("Invalid syntax")
    
    if len(judge) == 2:
        if judge[0] != "0":
            res += "simu_sleep(" + judge[0] + ")\n"
        
        assert_element = re.split(r'(&|\|)', judge[1])
        res += "simu_assert("
        for element in assert_element:
            if element == "&":
                res += " and "
            elif element == "|":
                res += " or "
            else:
                element = re.split(r'(@|<=|>=|=|<|>|∈)', element)
                if element[3] == "∈":
                    get_value = "simu_get_port_value({model=" + "\'" + element[0] + "\'," + "port=" + "\'" + element[2] + "\'" + ",})"
                    limitation = re.split(r'(\[|\]|,)', element[4])
                    lower = limitation[2]
                    upper = limitation[4]
                    res += "(" + get_value + ">=" + lower + " and " + get_value + "<=" + upper + ")"
                else:
                    get_value = "simu_get_port_value({model=" + "\'" + element[0] + "\'," + "port=" + "\'" + element[2] + "\'" + ",})"
                    if element[3] == "=":
                        element[3] = "=="
                    res += get_value + element[3] + element[4]
        res += ")\n"

    if len(judge) > 2:
        if judge[0] != "0":
            res += "simu_sleep(" + judge[0] + ")\n"

        addition_dic = dict()
        for i in range(2, len(judge)):
            addition = judge[i].split(":")
            if len(addition) != 2:
                raise SyntaxError("Invalid syntax")
            
            if addition[0] == "condition":
                addition_dic["condition"] = addition[1]
            elif addition[0] == "overtime":
                addition_dic["overtime"] = addition[1]
            elif addition[0] == "duration":
                addition_dic["duration"] = addition[1]
            else:
                raise SyntaxError("Invalid syntax")

        if "condition" in addition_dic:
            res += "while true do\n" + add_indentation(1) + "if "
            condition_element = re.split(r'(&|\|)', addition_dic["condition"])
            for element in condition_element:
                if element == "&":
                    res += " and "
                elif element == "|":
                    res += " or "
                else:
                    element = re.split(r'(@|<=|>=|=|<|>|∈)', element)
                    if element[3] == "∈":
                        get_value = "simu_get_port_value({model=" + "\'" + element[0] + "\'," + "port=" + "\'" + element[2] + "\'" + ",})"
                        limitation = re.split(r'(\[|\]|,)', element[4])
                        lower = limitation[2]
                        upper = limitation[4]
                        res += "(" +  get_value + ">=" + lower + " and " + get_value + "<=" + upper + ")"
                    else:
                        get_value = "simu_get_port_value({model=" + "\'" + element[0] + "\'," + "port=" + "\'" + element[2] + "\'" + ",})"
                        if element[3] == "=":
                            element[3] = "=="
                        res += get_value + element[3] + element[4]
            res += " then\n"
            res += add_indentation(2) + "break\n"
            res += add_indentation(1) + "end\n"
            res += "end\n"
        
        if "overtime" in addition_dic and "duration" not in addition_dic:
            res += "overtime_t = simu_get_current_time()\n"
            res += "while true do\n"
            res += add_indentation(1) + "if simu_get_current_time() - overtime_t >= " + addition_dic["overtime"] + " then\n"
            res += add_indentation(2) + "simu_assert(false)\n"
            res += add_indentation(1) + "end\n"
            res += add_indentation(1) + "if "
            
            assert_element = re.split(r'(&|\|)', judge[1])
            for element in assert_element:
                if element == "&":
                    res += " and "
                elif element == "|":
                    res += " or "
                else:
                    element = re.split(r'(@|<=|>=|=|<|>|∈)', element)
                    if element[3] == "∈":
                        get_value = "simu_get_port_value({model=" + "\'" + element[0] + "\'," + "port=" + "\'" + element[2] + "\'" + ",})"
                        limitation = re.split(r'(\[|\]|,)', element[4])
                        lower = limitation[2]
                        upper = limitation[4]
                        res += "(" + get_value + ">=" + lower + " and " + get_value + "<=" + upper + ")"
                    else:
                        get_value = "simu_get_port_value({model=" + "\'" + element[0] + "\'," + "port=" + "\'" + element[2] + "\'" + ",})"
                        if element[3] == "=":
                            element[3] = "=="
                        res += get_value + element[3] + element[4]
            res += " then\n"
            res += add_indentation(2) + "break\n"
            res += add_indentation(1) + "end\n"
            res += "end\n"
        
        elif "overtime" in addition_dic and "duration" in addition_dic:
            res += "overtime_t = simu_get_current_time()\n"
            res += "duration_t = nil\n"
            res += "while true do\n"
            res += add_indentation(1) + "if simu_get_current_time() - overtime_t >= " + addition_dic["overtime"] + " then\n"
            res += add_indentation(2) + "simu_assert(false)\n"
            res += add_indentation(1) + "end\n"
            res += add_indentation(1) + "if "

            assert_element = re.split(r'(&|\|)', judge[1])
            for element in assert_element:
                if element == "&":
                    res += " and "
                elif element == "|":
                    res += " or "
                else:
                    element = re.split(r'(@|<=|>=|=|<|>|∈)', element)
                    if element[3] == "∈":
                        get_value = "simu_get_port_value({model=" + "\'" + element[0] + "\'," + "port=" + "\'" + element[2] + "\'" + ",})"
                        limitation = re.split(r'(\[|\]|,)', element[4])
                        lower = limitation[2]
                        upper = limitation[4]
                        res += "(" + get_value + ">=" + lower + " and " + get_value + "<=" + upper + ")"
                    else:
                        get_value = "simu_get_port_value({model=" + "\'" + element[0] + "\'," + "port=" + "\'" + element[2] + "\'" + ",})"
                        if element[3] == "=":
                            element[3] = "=="
                        res += get_value + element[3] + element[4]
            res += " then\n"
            res += add_indentation(2) + "if duration_t == nil then\n"
            res += add_indentation(3) + "duration_t = simu_get_current_time()\n"
            res += add_indentation(2) + "else\n"
            res += add_indentation(3) + "if simu_get_current_time() - duration_t >= " + addition_dic["duration"] + " then\n"
            res += add_indentation(4) + "break\n"
            res += add_indentation(3) + "end\n"
            res += add_indentation(2) + "end\n"
            res += add_indentation(1) + "else\n"
            res += add_indentation(2) + "duration_t = nil\n"
            res += add_indentation(1) + "end\n"
            res += "end\n"

        elif "overtime" not in addition_dic and "duration" in addition_dic:
            res += "duration_t = simu_get_current_time()\n"
            res += "while simu_get_current_time() - duration_t < " + addition_dic["duration"] + " do\n"
            res += add_indentation(1) + "if not ("

            assert_element = re.split(r'(&|\|)', judge[1])
            for element in assert_element:
                if element == "&":
                    res += " and "
                elif element == "|":
                    res += " or "
                else:
                    element = re.split(r'(@|<=|>=|=|<|>|∈)', element)
                    if element[3] == "∈":
                        get_value = "simu_get_port_value({model=" + "\'" + element[0] + "\'," + "port=" + "\'" + element[2] + "\'" + ",})"
                        limitation = re.split(r'(\[|\]|,)', element[4])
                        lower = limitation[2]
                        upper = limitation[4]
                        res += "(" + get_value + ">=" + lower + " and " + get_value + "<=" + upper + ")"
                    else:
                        get_value = "simu_get_port_value({model=" + "\'" + element[0] + "\'," + "port=" + "\'" + element[2] + "\'" + ",})"
                        if element[3] == "=":
                            element[3] = "=="
                        res += get_value + element[3] + element[4]
            res += ") then\n"
            res += add_indentation(2) + "simu_assert(false)\n"
            res += add_indentation(1) + "end\n"
            res += "end\n"

        elif "overtime" not in addition_dic and "duration" not in addition_dic:
            assert_element = re.split(r'(&|\|)', judge[1])
            res += "if not ("
            for element in assert_element:
                if element == "&":
                    res += " and "
                elif element == "|":
                    res += " or "
                else:
                    element = re.split(r'(@|<=|>=|=|<|>|∈)', element)
                    if element[3] == "∈":
                        get_value = "simu_get_port_value({model=" + "\'" + element[0] + "\'," + "port=" + "\'" + element[2] + "\'" + ",})"
                        limitation = re.split(r'(\[|\]|,)', element[4])
                        lower = limitation[2]
                        upper = limitation[4]
                        res += "(" + get_value + ">=" + lower + " and " + get_value + "<=" + upper + ")"
                    else:
                        get_value = "simu_get_port_value({model=" + "\'" + element[0] + "\'," + "port=" + "\'" + element[2] + "\'" + ",})"
                        if element[3] == "=":
                            element[3] = "=="
                        res += get_value + element[3] + element[4]
            res += ") then\n"
            res += add_indentation(1) + "simu_assert(false)\n"
            res += "end\n"

        else:
            pass

    return res

def process_simset(simset):
    simset = simset.strip()
    res = str()
    simset = simset.split(";")

    if len(simset) < 2:
        raise SyntaxError("Invalid syntax")
    
    if len(simset) == 2:
        if simset[0] != "0":
            res += "simu_sleep(" + simset[0] + ")\n"
        
        simset_element = re.split(r'(@|=)', simset[1])
        res += "simu_set_port_value({" + "model=" + "\'" + simset_element[0] + "\'," + "port=" + "\'" + simset_element[2] + "\'," + "value=" + simset_element[4] + ",})\n"

    if len(simset) > 2:
        if simset[0] != "0":
            res += "simu_sleep(" + simset[0] + ")\n"

        addition_dic = dict()
        for i in range(2, len(simset)):
            addition = simset[i].split(":")
            if len(addition) != 2:
                raise SyntaxError("Invalid syntax")
            
            if addition[0] == "condition":
                addition_dic["condition"] = addition[1]
            else:
                raise SyntaxError("Invalid syntax")
            
        if "condition" in addition_dic:
            res += "while true do\n" + add_indentation(1) + "if "
            condition_element = re.split(r'(&|\|)', addition_dic["condition"])
            for element in condition_element:
                if element == "&":
                    res += " and "
                elif element == "|":
                    res += " or "
                else:
                    element = re.split(r'(@|<=|>=|=|<|>|∈)', element)
                    if element[3] == "∈":
                        get_value = "simu_get_port_value({model=" + "\'" + element[0] + "\'," + "port=" + "\'" + element[2] + "\'" + ",})"
                        limitation = re.split(r'(\[|\]|,)', element[4])
                        lower = limitation[2]
                        upper = limitation[4]
                        res += "(" + get_value + ">=" + lower + " and " + get_value + "<=" + upper + ")"
                    else:
                        get_value = "simu_get_port_value({model=" + "\'" + element[0] + "\'," + "port=" + "\'" + element[2] + "\'" + ",})"
                        if element[3] == "=":
                            element[3] = "=="
                        res += get_value + element[3] + element[4]
            res += " then\n"
            res += add_indentation(2) + "break\n"
            res += add_indentation(1) + "end\n"
            res += "end\n"

        simset_element = re.split(r'(@|=)', simset[1])
        res += "simu_set_port_value({" + "model=" + "\'" + simset_element[0] + "\'," + "port=" + "\'" + simset_element[2] + "\'," + "value=" + simset_element[4] + ",})\n"

    return res

def process_line(line):
    res = str()
    pattern = r"(\w+)\((.+)\)"
    match = re.match(pattern, line)
    if not match:
         raise SyntaxError("Invalid syntax")
    
    res = {"content": "/generate\n" + line + "/generate_end\n" + "/script\n"}    
    if match.groups()[0] == "JUDGE":
        res["content"] += process_judge(match.groups()[1])
    elif match.groups()[0] == "SIMSET":
        res["content"] += process_simset(match.groups()[1])
    res["content"] += "/script_end\n"
    return res

def process_data(data):
    res = list()
    data = data.split("--------Test_Cases--------:\n")
    for line in data:
        if line == "":
            continue
        res.append(process_line(line))
    return res

case_num_list = [100, 250, 500, 1000, 2500, 5000, 10000, 25000, 50000, 100000]
for case_num in case_num_list:

    wb = jsonlines.open("generate_data/train/generate_train_" + str(case_num) + ".jsonl", mode = "w")

    with open("generate_data/train/generate_train_" + str(case_num) + ".txt", encoding="utf-8") as f:
        data = f.read()
        res = process_data(data)
    
    wb.write_all(res)
    wb.close()
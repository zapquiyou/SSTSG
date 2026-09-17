import jsonlines
import re
import subprocess
import random
from nltk.corpus import words
import string

word_list = words.words()
keyword = ['JUDGE', 'SIMSET', 'simu_start', 'simu_stop', 'simmu_sleep', 'simu_assert', 'simu_get_port_value', 'simu_set_port_value', 'simu_get_current_time', 'overtime', 'duration', 'condition']
all_chars = string.digits + '_.-' + string.ascii_letters
operator_list = ['@', '<=', '>=', '=', '<', '>', '∈']

def random_change_string_case(string):
    res = str()
    for char in string:
        if char.isalpha():
            if char.islower():
                if random.randint(0, 20) < 2:
                    res += char.upper()
                else:
                    res += char
            else:
                if random.randint(0, 20) < 2:
                    res += char.lower()
                else:
                    res += char
        else:
            res += char
    return res

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

def process_error_judge(judge):
    error_list = ["sleep", "simset", "model", "port", "value", "no_condition", "no_overtime", "no_duration", "mess_overtime", "overtime", "duration", "condition", "delete"]
    num_error = random.randint(1, 3)
    judge = judge.strip()
    res = str()
    simset_error_flag = False
    judge = judge.split(";")
    if len(judge) < 2:
        raise SyntaxError("Invalid syntax")
    
    if len(judge) == 2:
        error_list.remove("no_condition")
        error_list.remove("no_overtime")
        error_list.remove("no_duration")
        error_list.remove("mess_overtime")
        error_list.remove("overtime")
        error_list.remove("duration")
        error_list.remove("condition")
    
    addition_dic = dict()
    if len(judge) > 2:
        for i in range(2, len(judge)):
            addition = judge[i].split(":")
            if len(addition) != 2:
                raise SyntaxError("Invalid syntax")
            
            if addition[0] == "condition":
                addition_dic["condition"] = addition[1]
                addition_dic["condition_index"] = i
            elif addition[0] == "overtime":
                addition_dic["overtime"] = addition[1]
                addition_dic["overtime_index"] = i
            elif addition[0] == "duration":
                addition_dic["duration"] = addition[1]
                addition_dic["duration_index"] = i
            else:
                raise SyntaxError("Invalid syntax")
        if "condition" not in addition_dic:
            error_list.remove("no_condition")
            error_list.remove("condition")
        if "overtime" not in addition_dic:
            error_list.remove("no_overtime")
            if "mess_overtime" in error_list:
                error_list.remove("mess_overtime")
            error_list.remove("overtime")
        if "duration" not in addition_dic:
            error_list.remove("no_duration")
            error_list.remove("duration")
            if "mess_overtime" in error_list:
                error_list.remove("mess_overtime")

    loop_index = 0
    while loop_index < num_error:
        if len(error_list) == 0:
            break

        error = random.choice(error_list)
        if error == "sleep":
            if judge[0] == "0":
                random_time = random.uniform(0.1, 50)
                judge[0] = "{:.3f}".format(random_time)
            else:
                is_modify_time = random.random()
                if is_modify_time < 0.5:
                    random_time = judge[0]
                    while random_time == judge[0]:
                        random_time = random.uniform(0, 50)
                    judge[0] = "{:.3f}".format(random_time)
                else:
                    judge[0] = "0"
            error_list.remove("sleep")
            loop_index += 1

        elif error == "simset":
            assert_element = re.split(r'(&|\|)', judge[1])
            num_judge = len(assert_element)
            odd_num_list = [i for i in range(num_judge + 1) if i % 2 == 1]
            random_judge_num = random.choice(odd_num_list)
            element = re.split(r'(@|<=|>=|=|<|>|∈)', assert_element[random_judge_num - 1])
            if element[3] == "∈":
                element[3] = "="
                element[4] = element[4].replace("[", "")
                element[4] = element[4].replace("]", "")
                value = element[4].split(",")
                element[4] = random.choice(value)
            else:
                element[3] = "="
            judge[1] = "".join(element)
            res = process_simset(";".join(judge[:2])) 
            simset_error_flag = True
            break

        elif error == "model":
            assert_element = re.split(r'(&|\|)', judge[1])
            num_judge = len(assert_element)
            odd_num_list = [i for i in range(num_judge + 1) if i % 2 == 1]
            random_judge_num = random.choice(odd_num_list)
            element = re.split(r'(@|<=|>=|=|<|>|∈)', assert_element[random_judge_num - 1])
            random_model_name = element[0]
            if random.random() < 0.5:
                while random_model_name == element[0]:
                    random_model_name_len = random.randint(1, 5)
                    random_word_num = random.randint(1, min(2, random_model_name_len))
                    if random_word_num == 2:
                        random_word2_index = random.randint(1, random_model_name_len - 1)
                    else:
                        random_word2_index = -1
                    random_model = str()
                    for j in range(random_model_name_len):
                        if j == 0:
                            random_keyword_num = random.randint(1, 1000)
                            if random_keyword_num == 1:
                                random_model += random.choice(keyword)
                            else:
                                random_model += random.choice(word_list)
                        elif j == random_word2_index:
                            random_keyword_num = random.randint(1, 1000)
                            if random_keyword_num == 1:
                                random_model += random.choice(keyword)
                            else:
                                random_model += random.choice(word_list)
                            random_model += random.choice(word_list)
                        else:
                            random_model += random.choice(all_chars)
                    random_model_name = random_model
            else:
                while random_model_name == element[0]:
                    random_model_name = random_change_string_case(element[0])
            element[0] = random_model_name
            assert_element[random_judge_num - 1] = "".join(element)
            judge[1] = "".join(assert_element)
            loop_index += 1
                
        elif error == "port":
            assert_element = re.split(r'(&|\|)', judge[1])
            num_judge = len(assert_element)
            odd_num_list = [i for i in range(num_judge + 1) if i % 2 == 1]
            random_judge_num = random.choice(odd_num_list)
            element = re.split(r'(@|<=|>=|=|<|>|∈)', assert_element[random_judge_num - 1])
            random_port_name = element[2]
            if random.random() < 0.5:
                while random_port_name == element[2]:
                    random_port_name_len = random.randint(1, 5)
                    random_word_num = random.randint(1, min(2, random_port_name_len))
                    if random_word_num == 2:
                        random_word2_index = random.randint(1, random_port_name_len - 1)
                    else:
                        random_word2_index = -1
                    random_port = str()
                    for j in range(random_port_name_len):
                        if j == 0:
                            random_keyword_num = random.randint(1, 1000)
                            if random_keyword_num == 1:
                                random_port += random.choice(keyword)
                            else:
                                random_port += random.choice(word_list)
                        elif j == random_word2_index:
                            random_keyword_num = random.randint(1, 1000)
                            if random_keyword_num == 1:
                                random_port += random.choice(keyword)
                            else:
                                random_port += random.choice(word_list)
                            random_port += random.choice(word_list)
                        else:
                            random_port += random.choice(all_chars)
                    random_port_name = random_port
            else:
                while random_port_name == element[2]:
                    random_port_name = random_change_string_case(element[2])
            element[2] = random_port_name
            assert_element[random_judge_num - 1] = "".join(element)
            judge[1] = "".join(assert_element)
            loop_index += 1

        elif error == "value":
            assert_element = re.split(r'(&|\|)', judge[1])
            num_judge = len(assert_element)
            odd_num_list = [i for i in range(num_judge + 1) if i % 2 == 1]
            random_judge_num = random.choice(odd_num_list)
            element = re.split(r'(@|<=|>=|=|<|>|∈)', assert_element[random_judge_num - 1])
            if random.random() < 0.5:
                random_value = element[4]
                if element[3] == "∈":
                    is_int = random.random()
                    if is_int < 0.5:
                        value1 = random.randint(-100000, 100000)
                    else:
                        value1 = random.uniform(-100000, 100000)
                    is_int = random.random()
                    if is_int < 0.5:
                        value2 = random.randint(-100000, 100000)
                    else:
                        value2 = random.uniform(-100000, 100000)
                    element[4] = "[" + str(min(value1, value2)) + "," + str(max(value1, value2)) + "]"
                else:
                    while random_value == element[4]:
                        is_int = random.random()
                        if is_int < 0.5:
                            random_value = random.randint(-100000, 100000)
                        else:
                            random_value = random.uniform(-100000, 100000)
                    element[4] = str(random_value)
            else:
                random_operator = element[3]
                if random_operator == "∈":
                    element[4] = element[4].replace("[", "")
                    element[4] = element[4].replace("]", "")
                    value = element[4].split(",")
                    element[4] = random.choice(value)
                while random_operator == element[3]:
                    random_operator = random.choice(operator_list)
                element[3] = random_operator
                if random_operator == "∈":
                    upper_value = random.uniform(float(element[4]), 100000)
                    element[4] = "[" + element[4] + "," + str(upper_value) + "]"
            judge[1] = "".join(element)
            error_list.remove("value")
            loop_index += 1

        elif error == "no_condition":
            judge.pop(addition_dic["condition_index"])
            error_list.remove("no_condition")
            error_list.remove("condition")
            if "overtime_index" in addition_dic:
                if addition_dic["overtime_index"] > addition_dic["condition_index"]:
                    addition_dic["overtime_index"] -= 1
            if "duration_index" in addition_dic:
                if addition_dic["duration_index"] > addition_dic["condition_index"]:
                    addition_dic["duration_index"] -= 1
            addition_dic.pop("condition")
            addition_dic.pop("condition_index")
            loop_index += 1

        elif error == "no_overtime":
            judge.pop(addition_dic["overtime_index"])
            error_list.remove("no_overtime")
            if "overtime" in error_list:
                error_list.remove("overtime")
            if "overtime" not in error_list and "duration" not in error_list:
                if "mess_overtime" in error_list:
                    error_list.remove("mess_overtime")
            if "duration_index" in addition_dic:
                if addition_dic["duration_index"] > addition_dic["overtime_index"]:
                    addition_dic["duration_index"] -= 1
            if "condition_index" in addition_dic:
                if addition_dic["condition_index"] > addition_dic["overtime_index"]:
                    addition_dic["condition_index"] -= 1
            addition_dic.pop("overtime")
            addition_dic.pop("overtime_index")
            loop_index += 1

        elif error == "no_duration":
            judge.pop(addition_dic["duration_index"])
            error_list.remove("no_duration")     
            if "duration" in error_list:
                error_list.remove("duration")
            if "overtime" not in error_list and "duration" not in error_list:
                if "mess_overtime" in error_list:
                    error_list.remove("mess_overtime")
            if "condition_index" in addition_dic:
                if addition_dic["condition_index"] > addition_dic["duration_index"]:
                    addition_dic["condition_index"] -= 1
            if "overtime_index" in addition_dic:
                if addition_dic["overtime_index"] > addition_dic["duration_index"]:
                    addition_dic["overtime_index"] -= 1
            addition_dic.pop("duration")
            addition_dic.pop("duration_index")
            loop_index += 1

        elif error == "mess_overtime":
            if "overtime" in addition_dic and "duration" not in addition_dic:
                judge[addition_dic["overtime_index"]] = judge[addition_dic["overtime_index"]].replace("overtime:", "duration:")
                addition_dic["duration"] = addition_dic["overtime"]
                addition_dic["duration_index"] = addition_dic["overtime_index"]
                addition_dic.pop("overtime")
                addition_dic.pop("overtime_index")
                if "overtime" in error_list:
                    error_list.remove("overtime")
                if "no_overtime" in error_list:
                    error_list.remove("no_overtime")
            elif "overtime" not in addition_dic and "duration" in addition_dic:
                judge[addition_dic["duration_index"]] = judge[addition_dic["duration_index"]].replace("duration:", "overtime:")
                addition_dic["overtime"] = addition_dic["duration"]
                addition_dic["overtime_index"] = addition_dic["duration_index"]
                addition_dic.pop("duration")
                addition_dic.pop("duration_index")
                if "duration" in error_list:
                    error_list.remove("duration")
                if "no_duration" in error_list:
                    error_list.remove("no_duration")
            elif "overtime" in addition_dic and "duration" in addition_dic:
                judge[addition_dic["overtime_index"]] = judge[addition_dic["overtime_index"]].replace("overtime:", "duration:")
                judge[addition_dic["duration_index"]] = judge[addition_dic["duration_index"]].replace("duration:", "overtime:")
                temp = addition_dic["overtime"]
                addition_dic["overtime"] = addition_dic["duration"]
                addition_dic["duration"] = temp
                temp = addition_dic["overtime_index"]
                addition_dic["overtime_index"] = addition_dic["duration_index"]
                addition_dic["duration_index"] = temp

            error_list.remove("mess_overtime")
            loop_index += 1

        elif error == "overtime":
            overtime_value = addition_dic["overtime"]
            while overtime_value == addition_dic["overtime"]:
                overtime_value = random.uniform(0.1, 50)
            judge[addition_dic["overtime_index"]] = "overtime:" + "{:.3f}".format(overtime_value)
            if "overtime" in error_list:
                error_list.remove("overtime")
            loop_index += 1

        elif error == "duration":
            duration_value = addition_dic["duration"]
            while duration_value == addition_dic["duration"]:
                duration_value = random.uniform(0.1, 50)
            judge[addition_dic["duration_index"]] = "duration:" + "{:.3f}".format(duration_value)
            if "duration" in error_list:
                error_list.remove("duration")
            loop_index += 1
            
        elif error == "condition":
            condition_element = re.split(r'(&|\|)', addition_dic["condition"])
            num_condition = len(condition_element)
            odd_num_list = [i for i in range(num_condition + 1) if i % 2 == 1]
            random_condition_num = random.choice(odd_num_list)
            element = re.split(r'(@|<=|>=|=|<|>|∈)', condition_element[random_condition_num - 1])
            condition_error_list = ["model", "port", "value", "delete"]
            if num_condition == 1:
                condition_error_list.remove("delete")
            condition_error = random.choice(condition_error_list)
            if condition_error == "model":
                random_model_name = element[0]
                if random.random() < 0.5:
                    while random_model_name == element[0]:
                        random_model_name_len = random.randint(1, 5)
                        random_word_num = random.randint(1, min(2, random_model_name_len))
                        if random_word_num == 2:
                            random_word2_index = random.randint(1, random_model_name_len - 1)
                        else:
                            random_word2_index = -1
                        random_model = str()
                        for j in range(random_model_name_len):
                            if j == 0:
                                random_keyword_num = random.randint(1, 1000)
                                if random_keyword_num == 1:
                                    random_model += random.choice(keyword)
                                else:
                                    random_model += random.choice(word_list)
                            elif j == random_word2_index:
                                random_keyword_num = random.randint(1, 1000)
                                if random_keyword_num == 1:
                                    random_model += random.choice(keyword)
                                else:
                                    random_model += random.choice(word_list)
                                random_model += random.choice(word_list)
                            else:
                                random_model += random.choice(all_chars)
                        random_model_name = random_model
                else:
                    while random_model_name == element[0]:
                        random_model_name = random_change_string_case(element[0])
                element[0] = random_model_name
                condition_element[random_condition_num - 1] = "".join(element)
                addition_dic["condition"] = "".join(condition_element)
            elif condition_error == "port":
                random_port_name = element[2]
                if random.random() < 0.5:
                    while random_port_name == element[2]:
                        random_port_name_len = random.randint(1, 5)
                        random_word_num = random.randint(1, min(2, random_port_name_len))
                        if random_word_num == 2:
                            random_word2_index = random.randint(1, random_port_name_len - 1)
                        else:
                            random_word2_index = -1
                        random_port = str()
                        for j in range(random_port_name_len):
                            if j == 0:
                                random_keyword_num = random.randint(1, 1000)
                                if random_keyword_num == 1:
                                    random_port += random.choice(keyword)
                                else:
                                    random_port += random.choice(word_list)
                            elif j == random_word2_index:
                                random_keyword_num = random.randint(1, 1000)
                                if random_keyword_num == 1:
                                    random_port += random.choice(keyword)
                                else:
                                    random_port += random.choice(word_list)
                                random_port += random.choice(word_list)
                            else:
                                random_port += random.choice(all_chars)
                        random_port_name = random_port
                else:
                    while random_port_name == element[2]:
                        random_port_name = random_change_string_case(element[2])
                element[2] = random_port_name
                condition_element[random_condition_num - 1] = "".join(element)
                addition_dic["condition"] = "".join(condition_element)
            elif condition_error == "value":
                if random.random() < 0.5:
                    random_value = element[4]
                    if element[3] == "∈":
                        is_int = random.random()
                        if is_int < 0.5:
                            value1 = random.randint(-100000, 100000)
                        else:
                            value1 = random.uniform(-100000, 100000)
                        is_int = random.random()
                        if is_int < 0.5:
                            value2 = random.randint(-100000, 100000)
                        else:
                            value2 = random.uniform(-100000, 100000)
                        element[4] = "[" + str(min(value1, value2)) + "," + str(max(value1, value2)) + "]"
                    else:
                        while random_value == element[4]:
                            is_int = random.random()
                            if is_int < 0.5:
                                random_value = random.randint(-100000, 100000)
                            else:
                                random_value = random.uniform(-100000, 100000)
                        element[4] = str(random_value)
                else:
                    random_operator = element[3]
                    if random_operator == "∈":
                        element[4] = element[4].replace("[", "")
                        element[4] = element[4].replace("]", "")
                        value = element[4].split(",")
                        element[4] = random.choice(value)
                    while random_operator == element[3]:
                        random_operator = random.choice(operator_list)
                    element[3] = random_operator
                    if random_operator == "∈":
                        upper_value = random.uniform(float(element[4]), 100000)
                        element[4] = "[" + element[4] + "," + str(upper_value) + "]"
            elif condition_error == "delete":
                condition_element.pop(random_condition_num - 1)
                if random_condition_num == 1:
                    condition_element.pop(0)
                elif random_condition_num == num_condition:
                    condition_element.pop(-1)
                else:
                    condition_element.pop(random_condition_num - 1)
                addition_dic["condition"] = "".join(condition_element)
            loop_index += 1
        
        elif error == "delete":
            assert_element = re.split(r'(&|\|)', judge[1])
            num_judge = len(assert_element)
            odd_num_list = [i for i in range(num_judge + 1) if i % 2 == 1]
            random_judge_num = random.choice(odd_num_list)
            if num_judge == 1:
                error_list.remove("delete")
                continue
            else:
                assert_element.pop(random_judge_num - 1)
                if random_judge_num == 1:
                    assert_element.pop(0)
                elif random_judge_num == num_judge:
                    assert_element.pop(-1)
                else:
                    assert_element.pop(random_judge_num - 1)
                judge[1] = "".join(assert_element)
            loop_index += 1

    if simset_error_flag == False:
        res = process_judge(";".join(judge))
    return res

def process_error_simset(simset):
    error_list = ["sleep", "judge", "model", "port", "value", "condition"]
    num_error = random.randint(1, 3)
    simset = simset.strip()
    res = str()
    simset = simset.split(";")
    simset_error_flag = False

    if len(simset) < 2:
        raise SyntaxError("Invalid syntax")
    
    if len(simset) == 2:
        if "condition" in error_list:
            error_list.remove("condition")
    
    if len(simset) > 2:
        addition_dic = dict()
        for i in range(2, len(simset)):
            addition = simset[i].split(":")
            if len(addition) != 2:
                raise SyntaxError("Invalid syntax")
            
            if addition[0] == "condition":
                addition_dic["condition"] = addition[1]
            else:
                raise SyntaxError("Invalid syntax")
        if "condition" not in addition_dic:
            error_list.remove("condition")

    loop_index = 0
    while loop_index < num_error:
        if len(error_list) == 0:
            break

        error = random.choice(error_list)
        if error == "sleep":
            if simset[0] == "0":
                random_time = random.uniform(0.1, 50)
                simset[0] = "{:.3f}".format(random_time)
            else:
                is_modify_time = random.random()
                if is_modify_time < 0.5:
                    random_time = simset[0]
                    while random_time == simset[0]:
                        random_time = random.uniform(0, 50)
                    simset[0] = "{:.3f}".format(random_time)
                else:
                    simset[0] = "0"
            error_list.remove("sleep")
            loop_index += 1

        elif error == "judge":
            assert_element = re.split(r'(@|=)', simset[1])
            judge_char_list = ["@","<=",">=","=","<",">","∈"]
            random_judge_char = assert_element[3]
            while random_judge_char == assert_element[3]:
                random_judge_char = random.choice(judge_char_list)
            assert_element[3] = random_judge_char
            if assert_element[3] == "∈":
                upper_value = random.uniform(float(assert_element[4]), 100000)
                assert_element[4] = "[" + assert_element[4] + "," + str(upper_value) + "]"
            simset[1] = "".join(assert_element)
            res = process_judge(";".join(simset[:2])) 
            simset_error_flag = True
            break

        elif error == "model":
            assert_element = re.split(r'(@|=)', simset[1])
            random_model_name = assert_element[0]
            if random.random() < 0.5:
                while random_model_name == assert_element[0]:
                    random_model_name_len = random.randint(1, 5)
                    random_word_num = random.randint(1, min(2, random_model_name_len))
                    if random_word_num == 2:
                        random_word2_index = random.randint(1, random_model_name_len - 1)
                    else:
                        random_word2_index = -1
                    random_model = str()
                    for j in range(random_model_name_len):
                        if j == 0:
                            random_keyword_num = random.randint(1, 1000)
                            if random_keyword_num == 1:
                                random_model += random.choice(keyword)
                            else:
                                random_model += random.choice(word_list)
                        elif j == random_word2_index:
                            random_keyword_num = random.randint(1, 1000)
                            if random_keyword_num == 1:
                                random_model += random.choice(keyword)
                            else:
                                random_model += random.choice(word_list)
                            random_model += random.choice(word_list)
                        else:
                            random_model += random.choice(all_chars)
                    random_model_name = random_model
            else:
                while random_model_name == assert_element[0]:
                    random_model_name = random_change_string_case(assert_element[0])
            assert_element[0] = random_model_name
            simset[1] = "".join(assert_element)
            loop_index += 1

        elif error == "port":
            assert_element = re.split(r'(@|=)', simset[1])
            random_port_name = assert_element[2]
            if random.random() < 0.5:
                while random_port_name == assert_element[2]:
                    random_port_name_len = random.randint(1, 5)
                    random_word_num = random.randint(1, min(2, random_port_name_len))
                    if random_word_num == 2:
                        random_word2_index = random.randint(1, random_port_name_len - 1)
                    else:
                        random_word2_index = -1
                    random_port = str()
                    for j in range(random_port_name_len):
                        if j == 0:
                            random_keyword_num = random.randint(1, 1000)
                            if random_keyword_num == 1:
                                random_port += random.choice(keyword)
                            else:
                                random_port += random.choice(word_list)
                        elif j == random_word2_index:
                            random_keyword_num = random.randint(1, 1000)
                            if random_keyword_num == 1:
                                random_port += random.choice(keyword)
                            else:
                                random_port += random.choice(word_list)
                            random_port += random.choice(word_list)
                        else:
                            random_port += random.choice(all_chars)
                    random_port_name = random_port
            else:
                while random_port_name == assert_element[2]:
                    random_port_name = random_change_string_case(assert_element[2])
            assert_element[2] = random_port_name
            simset[1] = "".join(assert_element)
            loop_index += 1

        elif error == "value":
            assert_element = re.split(r'(@|=)', simset[1])
            random_value = assert_element[4]
            while random_value == assert_element[4]:
                is_int = random.random()
                if is_int < 0.5:
                    random_value = random.randint(-100000, 100000)
                else:
                    random_value = random.uniform(-100000, 100000)
            assert_element[4] = str(random_value)
            simset[1] = "".join(assert_element)
            error_list.remove("value")
            loop_index += 1

        elif error == "condition":
            condition_element = re.split(r'(&|\|)', addition_dic["condition"])
            num_condition = len(condition_element)
            odd_num_list = [i for i in range(num_condition + 1) if i % 2 == 1]
            random_condition_num = random.choice(odd_num_list)
            assert_element = re.split(r'(@|<=|>=|=|<|>|∈)', condition_element[random_condition_num - 1])
            condition_error_list = ["model", "port", "value", "delete"]
            if num_condition == 1:
                condition_error_list.remove("delete")
            condition_error = random.choice(condition_error_list)
            if condition_error == "model":
                random_model_name = assert_element[0]
                if random.random() < 0.5:
                    while random_model_name == assert_element[0]:
                        random_model_name_len = random.randint(1, 5)
                        random_word_num = random.randint(1, min(2, random_model_name_len))
                        if random_word_num == 2:
                            random_word2_index = random.randint(1, random_model_name_len - 1)
                        else:
                            random_word2_index = -1
                        random_model = str()
                        for j in range(random_model_name_len):
                            if j == 0:
                                random_keyword_num = random.randint(1, 1000)
                                if random_keyword_num == 1:
                                    random_model += random.choice(keyword)
                                else:
                                    random_model += random.choice(word_list)
                            elif j == random_word2_index:
                                random_keyword_num = random.randint(1, 1000)
                                if random_keyword_num == 1:
                                    random_model += random.choice(keyword)
                                else:
                                    random_model += random.choice(word_list)
                                random_model += random.choice(word_list)
                            else:
                                random_model += random.choice(all_chars)
                        random_model_name = random_model
                else:
                    while random_model_name == assert_element[0]:
                        random_model_name = random_change_string_case(assert_element[0])
                assert_element[0] = random_model_name
                condition_element[random_condition_num - 1] = "".join(assert_element)
                addition_dic["condition"] = "".join(condition_element)
            elif condition_error == "port":
                random_port_name = assert_element[2]
                if random.random() < 0.5:
                    while random_port_name == assert_element[2]:
                        random_port_name_len = random.randint(1, 5)
                        random_word_num = random.randint(1, min(2, random_port_name_len))
                        if random_word_num == 2:
                            random_word2_index = random.randint(1, random_port_name_len - 1)
                        else:
                            random_word2_index = -1
                        random_port = str()
                        for j in range(random_port_name_len):
                            if j == 0:
                                random_keyword_num = random.randint(1, 1000)
                                if random_keyword_num == 1:
                                    random_port += random.choice(keyword)
                                else:
                                    random_port += random.choice(word_list)
                            elif j == random_word2_index:
                                random_keyword_num = random.randint(1, 1000)
                                if random_keyword_num == 1:
                                    random_port += random.choice(keyword)
                                else:
                                    random_port += random.choice(word_list)
                                random_port += random.choice(word_list)
                            else:
                                random_port += random.choice(all_chars)
                        random_port_name = random_port
                else:
                    while random_port_name == assert_element[2]:
                        random_port_name = random_change_string_case(assert_element[2])
                assert_element[2] = random_port_name
                condition_element[random_condition_num - 1] = "".join(assert_element)
                addition_dic["condition"] = "".join(condition_element)
            elif condition_error == "value":
                if random.random() < 0.5:
                    random_value = assert_element[4]
                    while random_value == assert_element[4]:
                        is_int = random.random()
                        if is_int < 0.5:
                            random_value = random.randint(-100000, 100000)
                        else:
                            random_value = random.uniform(-100000, 100000)
                    assert_element[4] = str(random_value)
                else:
                    random_operator = assert_element[3]
                    if random_operator == "∈":
                        assert_element[4] = assert_element[4].replace("[", "")
                        assert_element[4] = assert_element[4].replace("]", "")
                        value = assert_element[4].split(",")
                        assert_element[4] = random.choice(value)
                    while random_operator == assert_element[3]:
                        random_operator = random.choice(operator_list)
                    assert_element[3] = random_operator
                    if random_operator == "∈":
                        upper_value = random.uniform(float(assert_element[4]), 100000)
                        assert_element[4] = "[" + assert_element[4] + "," + str(upper_value) + "]"
            elif condition_error == "delete":
                condition_element.pop(random_condition_num - 1)
                if random_condition_num == 1:
                    condition_element.pop(0)
                elif random_condition_num == num_condition:
                    condition_element.pop(-1)
                else:
                    condition_element.pop(random_condition_num - 1)
                addition_dic["condition"] = "".join(condition_element)
            loop_index += 1

    if simset_error_flag == False:
        res = process_simset(";".join(simset))
    return res

def process_line(line, is_random_error):
    res = str()
    pattern = r"(\w+)\((.+)\)"
    match = re.match(pattern, line)
    if not match:
         raise SyntaxError("Invalid syntax")
    
    error_flag = False
    garbled_flag = False
    special_error_flag = False
    if is_random_error == True:
        if random.random() < 0.25:
            error_flag = False
        else:
            if random.random() < 0.80:
                error_flag = True
            else:
                if random.random() < 0.05:
                    special_error_flag = True
                else:
                    garbled_flag = True
            

    if garbled_flag == True:
        error_flag = True
        random_line_num = random.randint(3,6)
        for i in range(random_line_num):
            random_garbled_num = random.randint(10, 20)
            for j in range(random_garbled_num):
                if random.random() < 0.5:
                    random_garbled = random.choice(string.ascii_letters + string.digits)
                else:
                    random_garbled = random.choice(word_list)
                res += random_garbled
            res += "\n"
    
    elif special_error_flag == True:
        error_flag = True
        res = "ERROR!\n"

    else:
        if error_flag == False:
            if match.groups()[0] == "JUDGE":
                res = process_judge(match.groups()[1])
            elif match.groups()[0] == "SIMSET":
                res = process_simset(match.groups()[1])
        else:
            if match.groups()[0] == "JUDGE":
                res = process_error_judge(match.groups()[1])
            elif match.groups()[0] == "SIMSET":
                res = process_error_simset(match.groups()[1])
    
    return res, error_flag

num_case_list = [100, 250, 500, 1000, 2500, 5000, 10000, 25000, 50000, 100000]
for num_case in num_case_list:
    formal_case_file = open("verify_data/train/verify_train_" + str(num_case) + ".txt", "r", encoding="utf-8")
    formal_case = formal_case_file.read()
    cases = formal_case.split("--------Test_Cases--------:\n")

    prompt_file = jsonlines.open("verify_data/train/verify_train_" + str(num_case) + ".jsonl", mode = "w")

    index = 0
    for case in cases:
        if case == "":
            continue
        
        (correct_script,error_flag) = process_line(case, False)
        (verify_script,error_flag) = process_line(case, True)
        jsonl_data = dict()
        jsonl_data["content"] = ""
        jsonl_data["content"] += "/verify\n"
        jsonl_data["content"] += "//case\n" + case + "//case_end\n"
        jsonl_data["content"] += "//script\n" + verify_script + "//script_end\n"
        jsonl_data["content"] += "/verify_end\n"
        jsonl_data["content"] += "/verified_script\n"
        if error_flag == False:
            is_correct = "Correct\n"
            jsonl_data["content"] += "//result\n" + is_correct + "//result_end\n"
        else:
            is_correct = "Incorrect\n"
            jsonl_data["content"] += "//result\n" + is_correct + "//result_end\n"
            jsonl_data["content"] += "//correct_script\n" + correct_script + "//correct_script_end\n"
        jsonl_data["content"] += "/verified_script_end\n"
        prompt_file.write(jsonl_data)
        index += 1
        print("original: " + case)
        print("correct_script: " + correct_script)
        print("index: " + str(index)+ " done!!")
        
    formal_case_file.close()
    prompt_file.close()
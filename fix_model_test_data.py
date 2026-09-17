import jsonlines
import re
import subprocess
import random
from nltk.corpus import words
import string

word_list = words.words()

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
    
    if match.groups()[0] == "JUDGE":
        res = process_judge(match.groups()[1])
    elif match.groups()[0] == "SIMSET":
        res = process_simset(match.groups()[1])
    
    return res

def remove_ansi_escape_codes(input_str):
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', input_str)

def run_lua_script(script):
    function_def_str = "function  simu_start()\nend\nfunction  simu_sleep(a)\nend\nfunction  simu_assert(a)\nend\nfunction simu_get_port_value(a)\n    return 3.14\nend\nfunction simu_set_port_value(a)\nend\nfunction simu_get_current_time()\n    return 3.35\nend\nfunction  simu_stop()\nend\n"
    script = function_def_str + script
    with open("test.lua", "w") as f:
        f.write(script)
    try:
        output = subprocess.check_output(['luacheck', "test.lua"], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        start_str = "/ "
        end_str = " error"
        num_error = re.search(f"{start_str}(.*?){end_str}", e.output.decode())
        if remove_ansi_escape_codes(num_error.group(1)) == "0":
            print(f"No syntax errors in test.lua.")
            return True, "No syntax errors in test.lua."
        else:
            return False, remove_ansi_escape_codes(e.output.decode())
    else:
        print(f"No syntax errors in test.lua.")
        return True, "No syntax errors in test.lua."

def insert_random_error(script, is_undefine, is_condition):
    error_list = ['"','(', '{', '==', '=', '((', '))', 'changefunc']
    if is_undefine:
        error_list.append('undefine')
        error_list.append('end')
        error_list.append('then')
    else:
        if is_condition:
            error_list.append('end')
            error_list.append('then')
    function_list = ['simu_start', 'simu_sleep', 'simu_assert', 'simu_get_port_value', 'simu_set_port_value', 'simu_get_current_time', 'simu_stop']

    undefine_info = []
    insert_error_list = []
    changefunc_info = []
    num_error = random.randint(1, 3)
    loop_index = 0
    while loop_index < num_error:
        error = random.choice(error_list)
        if error == '"':
            parts = script.split("'")
            if len(parts) <= 1:
                continue
            insert_index = random.randint(0, len(parts) - 2)
            parts[insert_index] += parts.pop(insert_index + 1)
            script = "'".join(parts)
            if '"' in error_list:
                error_list.remove('"')
            loop_index += 1
            insert_error_list.append(error)

        elif error == '(':
            parenthese = ['(', ')']
            delete_parenthese = random.choice(parenthese)
            parts = script.split(delete_parenthese)
            if len(parts) <= 1:
                continue
            insert_index = random.randint(0, len(parts) - 2)
            parts[insert_index] += parts.pop(insert_index + 1)
            script = delete_parenthese.join(parts)
            if '((' in error_list:
                error_list.remove('((')
            if '))' in error_list:
                error_list.remove('))')
            if '(' in error_list:
                error_list.remove('(')
            loop_index += 1
            insert_error_list.append(error)

        elif error == '{':
            brace = ['{', '}']
            delete_brace = random.choice(brace)
            parts = script.split(delete_brace)
            if len(parts) <= 1:
                continue
            insert_index = random.randint(0, len(parts) - 2)
            parts[insert_index] += parts.pop(insert_index + 1)
            script = delete_brace.join(parts)
            loop_index += 1
            insert_error_list.append(error)

        elif error == 'end':
            parts = script.split('end\n')
            if len(parts) <= 1:
                continue
            insert_index = random.randint(0, len(parts) - 2)
            parts[insert_index] += parts.pop(insert_index + 1)
            script = 'end\n'.join(parts)
            loop_index += 1
            insert_error_list.append(error)

        elif error == 'deletepar':
            pattern = re.compile(r'\((.*?)\)')
            matches = list(pattern.finditer(script))
            if not matches:
                if 'deletepar' in error_list:
                    error_list.remove('deletepar')
                continue
            attemps = 0
            while attemps < 10:
                match = random.choice(matches)
                params = re.split(r',(?={)', match.group(1))
                params = [param.strip() for param in params if param.strip() != '']
                if len(params) > 0:
                    params.pop(random.randint(0, len(params) - 1))
                    new_match = '(' + ', '.join(params) + ')'
                    script = script[:match.start()] + new_match + script[match.end():]
                    break
                attemps += 1
            if attemps == 10:
                if 'deletepar' in error_list:
                    error_list.remove('deletepar')
                continue
            loop_index += 1
            insert_error_list.append(error)
                
        elif error == '==':
            parts = script.split('==')
            if len(parts) <= 1:
                if '==' in error_list:
                    error_list.remove('==')
                continue
            attemps = 0
            while attemps < 10:
                replace_index = random.randint(0, len(parts) - 2)
                if re.search(r'(model|port|value)\s*$', parts[replace_index].strip()):
                    attemps += 1
                    continue
                parts[replace_index] += '=' + parts.pop(replace_index + 1)
                script = '=='.join(parts)
                break
            if attemps == 10:
                if '==' in error_list:
                    error_list.remove('==')
                continue
            if '=' in error_list:
                error_list.remove('=')
            loop_index += 1
            insert_error_list.append(error)

        elif error == '=':
            parts = script.split('=')
            if len(parts) <= 1:
                if '=' in error_list:
                    error_list.remove('=')
                continue
            attempts = 0
            while attempts < 10:
                replace_index = random.randint(0, len(parts) - 2)
                if re.search(r'(model|port|value)\s*$', parts[replace_index].strip()):
                    attempts += 1
                    continue
                parts[replace_index] += '==' + parts.pop(replace_index + 1)
                script = '='.join(parts)
                break
            if attempts == 10:
                if '=' in error_list:
                    error_list.remove('=')
                continue
            if '==' in error_list:
                error_list.remove('==')
            loop_index += 1
            insert_error_list.append(error)

        elif error == 'addpar':
            pattern = re.compile(r'\((.*?)\)')
            matches = list(pattern.finditer(script))
            if not matches:
                if 'addpar' in error_list:
                    error_list.remove('addpar')
                continue
            match = random.choice(matches)
            if match.group(1):
                new_match = '(' + match.group(1) + ', ' + random.choice(word_list) + ')'
            else:
                new_match = '(' + random.choice(word_list) + ')'
            script = script[:match.start()] + new_match + script[match.end():]
            loop_index += 1
            insert_error_list.append(error)

        elif error == 'undefine':
            targets = ['overtime_t =', 'duration_t =']
            target = random.choice(targets)
            lines = script.split('\n')
            check_flag = False
            for line in lines:
                if bool(re.match(f'^{target}', line.strip())):
                    if random.random() < 0.5:
                        lines.remove(line)
                    else:
                        lines[lines.index(line)] = line.replace(target, random.choice(word_list) + ' =')
                    undefine_info_obj = {}
                    undefine_info_obj["target"] = target.replace(' =', '')
                    undefine_info.append(undefine_info_obj)
                    check_flag = True
                    break
            if check_flag == False:
                targets_copy = ['overtime_t =', 'duration_t =']
                targets_copy.remove(target)
                target = random.choice(targets_copy)
                for line in lines:
                    if bool(re.match(f'^{target}', line.strip())):
                        if random.random() < 0.5:
                            lines.remove(line)
                        else:
                            lines[lines.index(line)] = line.replace(target, random.choice(word_list) + ' =')
                        undefine_info_obj = {}
                        undefine_info_obj["target"] = target.replace(' =', '')
                        undefine_info.append(undefine_info_obj)
                        break
            script = '\n'.join(lines)
            if 'undefine' in error_list:
                error_list.remove('undefine')
            if len(undefine_info) == 2:
                print("[script]:" + script)
            loop_index += 1
            insert_error_list.append(error)

        elif error == 'then':
            parts = script.split('then')
            if len(parts) <= 1:
                continue
            insert_index = random.randint(0, len(parts) - 2)
            parts[insert_index] += parts.pop(insert_index + 1)
            script = 'then'.join(parts)
            loop_index += 1
            insert_error_list.append(error)

        elif error == '((':
            parts = script.split('(')
            if len(parts) <= 1:
                continue
            replace_index = random.randint(0, len(parts) - 2)
            parts[replace_index] += '((' + parts.pop(replace_index + 1)
            script = '('.join(parts)
            if '(' in error_list:
                error_list.remove('(')
            if '))' in error_list:
                error_list.remove('))')
            
            loop_index += 1
            insert_error_list.append(error)

        elif error == '))':
            parts = script.split(')')
            if len(parts) <= 1:
                continue
            replace_index = random.randint(0, len(parts) - 2)
            parts[replace_index] += '))' + parts.pop(replace_index + 1)
            script = ')'.join(parts)
            if '(' in error_list:
                error_list.remove('(')
            if '((' in error_list:
                error_list.remove('((')
            loop_index += 1
            insert_error_list.append(error)

        elif error == 'changefunc':
            pattern = re.compile('|'.join(function_list))
            matches = list(pattern.finditer(script))
            if not matches:
                if 'changefunc' in error_list:
                    error_list.remove('changefunc')
                continue
            match = random.choice(matches)
            operation = random.choice(['delete', 'modify'])
            if operation == 'delete':
                changefunc_info_obj = {}
                delete_range = random.randint(1, min(5, len(match.group())))
                changefunc_info_obj['func'] = match.group()[:delete_range]
                changefunc_info.append(changefunc_info_obj)
                script = script[:match.start()] + match.group()[delete_range:] + script[match.end():]
            else:
                changefunc_info_obj = {}
                modify_range = random.randint(1, min(5, len(match.group())))
                random_chars = ''.join(random.choice(string.ascii_letters) for _ in range(modify_range))
                changefunc_info_obj['func'] = match.group()[:modify_range] + random_chars + match.group()[modify_range:]
                changefunc_info.append(changefunc_info_obj)
                script = script[:match.start()] + match.group()[:modify_range] + random_chars + match.group()[modify_range:] + script[match.end():]
            loop_index += 1
            insert_error_list.append(error)

    return script, insert_error_list, undefine_info, changefunc_info


num_case_list = [1000]
for num_case in num_case_list:
    formal_case_file = open("fix_data/test/fix_test_" + str(num_case) + ".txt", "r", encoding="utf-8")
    formal_case = formal_case_file.read()
    cases = formal_case.split("--------Test_Cases--------:\n")

    prompt_file = jsonlines.open("fix_data/test/fix_test_" + str(num_case) + ".jsonl", mode = "w")

    index = 0
    for case in cases:
        if case == "":
            continue
        
        correct_script = process_line(case)
        is_condition = False
        is_undefine = False
        if "condition:" in case:
            is_condition = True
        if "duration:" in case or "overtime:" in case:
            is_undefine = True

        (error_script, insert_error_list, undefine_info, changefunc_info) = insert_random_error(correct_script, is_undefine, is_condition)
        execute_result, error_info = run_lua_script(error_script)
        undefine_info_index = 0
        for error in insert_error_list:
            if error == 'undefine':
                target = undefine_info[undefine_info_index]["target"]
                if error_info == "No syntax errors in test.lua.":
                    error_info = "Checking test.lua                                 1 error\r\n\r\n    test.lua attempt to perform arithmetic on a nil value (global '" + target +"')\r\n\r\nTotal: 0 warnings / 1 error in 1 file\r\n"
                else:
                    start_str = "/ "
                    end_str = " error"
                    num_error = re.search(f"{start_str}(.*?){end_str}", error_info)
                    num_error = int(num_error.group(1))
                    error_infos = error_info.split("\r\n")
                    error_infos.insert(2, "    test.lua attempt to perform arithmetic on a nil value (global '" + target +"')")
                    error_info = "\r\n".join(error_infos)
                    if num_error == 1:
                        error_info = error_info.replace("1 error", "2 errors")
                    else:
                        error_info = error_info.replace(str(num_error) + " errors", str(num_error + 1) + " errors")

                undefine_info_index += 1
        
        changefunc_info_index = 0
        for error in insert_error_list:
            if error == 'changefunc':
                func = changefunc_info[changefunc_info_index]["func"]
                if error_info == "No syntax errors in test.lua.":
                    error_info = "Checking test.lua                                 1 error\r\n\r\n    test.lua attempt to perform arithmetic on a nil value (global '" + func +"')\r\n\r\nTotal: 0 warnings / 1 error in 1 file\r\n"
                else:
                    start_str = "/ "
                    end_str = " error"
                    num_error = re.search(f"{start_str}(.*?){end_str}", error_info)
                    num_error = int(num_error.group(1))
                    error_infos = error_info.split("\r\n")
                    error_infos.insert(2, "    test.lua attempt to perform arithmetic on a nil value (global '" + func +"')")
                    error_info = "\r\n".join(error_infos)
                    if num_error == 1:
                        error_info = error_info.replace("1 error", "2 errors")
                    else:
                        error_info = error_info.replace(str(num_error) + " errors", str(num_error + 1) + " errors")

                changefunc_info_index += 1
                

        error_info = error_info.replace("\r\n", "\n")
        fix_data = dict()
        content = "/fix\n//case\n" + case + "//case_end\n//error_script\n" + error_script + "//error_script_end\n//error_log\n" + error_info + "//error_log_end\n/fix_end\n/correct_script\n" + correct_script + "/correct_script_end\n"

        fix_data["content"] = content
        fix_data["insert_error_list"] = insert_error_list
        prompt_file.write(fix_data)

    formal_case_file.close()
    prompt_file.close()

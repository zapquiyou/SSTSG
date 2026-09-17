import jsonlines
import re
import subprocess
import json

def remove_ansi_escape_codes(input_str):
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', input_str)

def verify_lua_script(script):
    function_def_str = "function  simu_start()\nend\nfunction  simu_sleep()\nend\nfunction  simu_assert(a)\nend\nfunction simu_get_port_value(a)\n    return 3.14\nend\nfunction simu_set_port_value(a)\nend\nfunction simu_get_current_time()\n    return 3.35\nend\nfunction  simu_stop()\nend\n"
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
            return True
        else:
            return False
    else:
        print(f"No syntax errors in test.lua.")
        return True

def check_indentation(str1, str2):
    lines1 = str1.split('\n')
    lines2 = str2.split('\n')
    if "" in lines1:
        lines1.remove("")
    if "" in lines2:
        lines2.remove("")
    print(lines1)
    print(lines2)
    if len(lines1) != len(lines2):
        print("Error: Different number of lines.")
        return False
    for line1, line2 in zip(lines1, lines2):
        if len(line1) - len(line1.lstrip()) != len(line2) - len(line2.lstrip()):
            print("Error: Different indentation.")
            return False
    return True

num_case_model_train_list = [100, 250, 500, 1000, 2500, 5000, 10000, 25000, 50000, 100000]
for num_case_model_train in num_case_model_train_list:
    correct_result_json = jsonlines.open("fix_data/test/fix_test_1000.jsonl", mode = "r")
    fix_result_json = jsonlines.open("fix_data/test/fix_test_" + str(num_case_model_train) + "_result.jsonl", mode = "r")

    start_str = "/correct_script\n"
    end_str = "/correct_script_end\n"
    index = 0
    num_correct = 0
    num_error_char = 0
    num_error_check = 0
    result_dic = {}
    result_dic["result"] = []


    for fix, correct in zip(fix_result_json, correct_result_json):
        result_obj = {}
        result_obj["fix"] = fix["output"][0]

        fix_result_char = re.sub(r'\s', '',fix["output"][0])
        correct_result = re.search(f"{start_str}(.*?){end_str}", correct["content"], re.DOTALL)
        print(correct_result.group(1))
        result_obj["correct"] = correct_result.group(1)
        correct_result_char = re.sub(r'\s', '',correct_result.group(1))

        if fix_result_char != correct_result_char:
            print("Error")
            num_error_char += 1
            result_obj["char_result"] = False
            verify_result = verify_lua_script(fix["output"][0])
            if verify_result == False:
                result_obj["verify_result"] = False
            else:
                if check_indentation(fix["output"][0], correct_result.group(1)):
                    result_obj["verify_result"] = True
                else:
                    result_obj["verify_result"] = False
                    result_obj["error"] = "Indentation error"
        else:
            result_obj["char_result"] = True
            verify_result = verify_lua_script(fix["output"][0])
            if verify_result == False:
                result_obj["verify_result"] = False
            else:
                if check_indentation(fix["output"][0], correct_result.group(1)):
                    num_correct += 1
                    result_obj["verify_result"] = True
                else:
                    result_obj["verify_result"] = False
                    result_obj["error"] = "Indentation error"

        result_dic["result"].append(result_obj)

        index += 1

    result_dic["total"] = index
    result_dic["correct_rate"] = num_correct / index
    with open("fix_data/test/fix_check_" + str(num_case_model_train) + ".json", "w", encoding='utf-8') as f:
        json.dump(result_dic, f, ensure_ascii=False, indent=4)
    correct_result_json.close()
    fix_result_json.close()
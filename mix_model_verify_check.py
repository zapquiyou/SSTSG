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

num_case_model_train_list = [300, 750, 1500, 3000, 7500, 15000, 30000, 75000, 150000, 300000]
for num_case_model_train in num_case_model_train_list:
    correct_result_json = jsonlines.open("mix_data/test/verify_test_1000.jsonl", mode = "r")
    verify_result_json = jsonlines.open("mix_data/test/mix_test_verify_" + str(num_case_model_train) + "_result.jsonl", mode = "r")

    start_str = "/verified_script\n"
    end_str = "/verified_script_end\n"
    result_str = "//result\n"
    result_end_str = "//result_end\n"
    verified_str = "//correct_script\n"
    verified_end_str = "//correct_script_end\n"
    index = 0
    num_correct = 0
    num_error_char = 0
    num_error_check = 0
    result_dic = {}
    result_dic["result"] = []

    for verify, correct in zip(verify_result_json, correct_result_json):
        result_obj = {}
        result_obj["verify"] = verify["output"][0]
        result_obj["correct"] = re.search(f"{start_str}(.*?){end_str}", correct["content"], re.DOTALL).group(1)
        verify_result = re.search(f"{result_str}(.*?){result_end_str}", verify["output"][0], re.DOTALL)
        if verify_result == None:
            result_obj["result"] = False
        else:
            verify_result_str = verify_result.group(1)
            correct_result_str = re.search(f"{result_str}(.*?){result_end_str}", correct["content"], re.DOTALL).group(1)
            if verify_result_str != correct_result_str:
                result_obj["result"] = False
            else:
                result_obj["result"] = True
                if verify_result_str == "Correct\n":
                    num_correct += 1
                else:
                    verify_script = re.search(f"{verified_str}(.*?){verified_end_str}", verify["output"][0], re.DOTALL)
                    if verify_script == None:
                        result_obj["char_result"] = False
                        result_obj["verify_result"] = False
                    else:
                        verify_script_str = verify_script.group(1)
                        verify_script_char = re.sub(r'\s', '',verify_script_str)
                        correct_script = re.search(f"{verified_str}(.*?){verified_end_str}", correct["content"], re.DOTALL)
                        correct_script_str = correct_script.group(1)
                        correct_script_char = re.sub(r'\s', '',correct_script_str)

                        if verify_script_char != correct_script_char:
                            print("Error")
                            num_error_char += 1
                            result_obj["char_result"] = False
                            run_lua_result = verify_lua_script(verify_script_str)
                            if run_lua_result == False:
                                result_obj["verify_result"] = False
                            else:
                                if check_indentation(verify_script_str, correct_script_str):
                                    result_obj["verify_result"] = True
                                else:
                                    result_obj["verify_result"] = False
                                    result_obj["error"] = "Indentation error"
                        else:
                            result_obj["char_result"] = True
                            run_lua_result = verify_lua_script(verify_script_str)
                            if run_lua_result == False:
                                result_obj["verify_result"] = False
                            else:
                                if check_indentation(verify_script_str, correct_script_str):
                                    num_correct += 1
                                    result_obj["verify_result"] = True
                                else:
                                    result_obj["verify_result"] = False
                                    result_obj["error"] = "Indentation error"
                        
        result_dic["result"].append(result_obj)

        index += 1

    result_dic["total"] = index
    result_dic["correct_rate"] = num_correct / index
    with open("mix_data/test/mix_verify_check_" + str(num_case_model_train) + ".json", "w", encoding='utf-8') as f:
        json.dump(result_dic, f, ensure_ascii=False, indent=4)
    correct_result_json.close()
    verify_result_json.close()
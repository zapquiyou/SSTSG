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

num_temperature_list = [0.1, 0.2, 0.25, 0.5]
for num_temperature in num_temperature_list:
    correct_rate_list = []
    case_correct_list = [False] * 1000
    for times in range(10):
        correct_result_json = jsonlines.open("mix_data/test/generate_test_1000.jsonl", mode = "r")
        generate_result_json = jsonlines.open("mix_data/test/test_mix_generate_15000_temperature_" + str(num_temperature) + "_" + str(times) + "_result.jsonl", mode = "r")

        start_str = "/script\n"
        end_str = "/script_end\n"
        index = 0
        num_correct = 0
        num_error_char = 0
        num_error_check = 0
        result_dic = {}
        result_dic["result"] = []


        for generate, correct in zip(generate_result_json, correct_result_json):
            result_obj = {}
            result_obj["generate"] = generate["output"][0]

            generate_result_char = re.sub(r'\s', '',generate["output"][0])
            correct_result = re.search(f"{start_str}(.*?){end_str}", correct["content"], re.DOTALL)
            print(correct_result.group(1))
            result_obj["correct"] = correct_result.group(1)
            correct_result_char = re.sub(r'\s', '',correct_result.group(1))

            if generate_result_char != correct_result_char:
                print("Error")
                num_error_char += 1
                result_obj["char_result"] = False
                verify_result = verify_lua_script(generate["output"][0])
                if verify_result == False:
                    result_obj["verify_result"] = False
                else:
                    if check_indentation(generate["output"][0], correct_result.group(1)):
                        result_obj["verify_result"] = True
                    else:
                        result_obj["verify_result"] = False
                        result_obj["error"] = "Indentation error"
            else:
                result_obj["char_result"] = True
                verify_result = verify_lua_script(generate["output"][0])
                if verify_result == False:
                    result_obj["verify_result"] = False
                else:
                    if check_indentation(generate["output"][0], correct_result.group(1)):
                        num_correct += 1
                        result_obj["verify_result"] = True
                        case_correct_list[index] = True
                    else:
                        result_obj["verify_result"] = False
                        result_obj["error"] = "Indentation error"

            result_dic["result"].append(result_obj)

            index += 1

        result_dic["total"] = index
        result_dic["correct_rate"] = num_correct / index
        correct_rate_list.append(num_correct / index)
        correct_result_json.close()
        generate_result_json.close()

    final_dic = {}
    final_dic["correct_rate"] = correct_rate_list
    final_dic["max_correct_rate"] = max(correct_rate_list)
    final_dic["min_correct_rate"] = min(correct_rate_list)
    final_dic["mean_correct_rate"] = sum(correct_rate_list) / len(correct_rate_list)
    total_correct = case_correct_list.count(True)
    final_dic["total_correct"] = total_correct

    with open("mix_data/test/test_generate_sampling_" + str(num_temperature) + "_check.json", "w", encoding='utf-8') as f:
        json.dump(final_dic, f, ensure_ascii=False, indent=4)
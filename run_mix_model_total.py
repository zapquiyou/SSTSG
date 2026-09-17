from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, AutoConfig
import jsonlines
import re
import subprocess


num_test_case_list = [300000]
num_test_case_list.reverse()
generate_start_str = "/script\n"
generate_end_str = "/script_end\n"
fix_input_start_str = "/fix\n"
fix_input_end_str = "/fix_end\n"
fix_output_start_str = "/correct_script\n"
fix_output_end_str = "/correct_script_end\n"
verify_input_start_str = "/verify\n"
verify_input_end_str = "/verify_end\n"
verify_output_start_str = "/verified_script\n"
verify_output_end_str = "/verified_script_end\n"
result_str = "//result\n"
result_end_str = "//result_end\n"
verified_str = "//correct_script\n"
verified_end_str = "//correct_script_end\n"

num_correct_generate = 0

for num_test_case in num_test_case_list:

    checkpoint = "finetune_starcoder2_mix_" + str(num_test_case) + "/final_checkpoint"
    model = "bigcode/starcoder2-3b"
    device = "cuda" # for GPU usage or "cpu" for CPU usage
    quantization_config = BitsAndBytesConfig(load_in_8bit=True)

    tokenizer = AutoTokenizer.from_pretrained(model)
    model = AutoModelForCausalLM.from_pretrained(checkpoint).to(device)

    with open("mix_data/test/generate_test_1000.txt", encoding="utf-8") as f:
        formal_test_case = f.read()
    cases = formal_test_case.split("--------Test_Cases--------:\n")

    wf = jsonlines.open("mix_data/test/test_mix_total_generate_" + str(num_test_case) + "_result.jsonl", mode = "w")

    index = 0

    for case_str in cases:
        if case_str == "":
            continue
        case_lines = case_str.split("\n")
        generate_script = []
        # generate_script.append("simu_start()\n")
        formal_case = []
        for line in case_lines:
            exception_flag = False
            if line == "":
                continue
            inputs = tokenizer.encode("/generate\n" + line + "\n/generate_end\n", return_tensors="pt").to(device)
            eos_token_id = tokenizer.eos_token_id
            pad_token_id = tokenizer.pad_token_id
            outputs = model.generate(inputs, max_length=750, eos_token_id=eos_token_id, pad_token_id=pad_token_id, do_sample=False, temperature=0.75)
            script = tokenizer.decode(outputs[0])
            script_line = script.split("\n")
            if  script_line[3] != "/script":
                exception_flag = True
            else:
                script = re.search(f"{generate_start_str}(.*?){generate_end_str}", script, re.DOTALL)
                if script == None:
                    outputs = model.generate(inputs, max_length=1000, eos_token_id=eos_token_id, pad_token_id=pad_token_id, do_sample=False, temperature=0.75)
                    script = tokenizer.decode(outputs[0])
                    script = re.search(f"{generate_start_str}(.*?){generate_end_str}", script, re.DOTALL)
                    if script == None:
                        outputs = model.generate(inputs, max_length=1250, eos_token_id=eos_token_id, pad_token_id=pad_token_id, do_sample=False, temperature=0.75)
                        script = tokenizer.decode(outputs[0])
                        script = re.search(f"{generate_start_str}(.*?){generate_end_str}", script, re.DOTALL)
                        if script == None:
                            print("Error: script is None")
                            exception_flag = True
            if exception_flag == True:
                script = "ERROR!\n"
            else:
                script = script.group(1)
            generate_script.append(script)
            formal_case.append(line)

        # generate_script.append("simu_stop()\n")
        wf.write({"input": formal_case, "output": generate_script})
        index += 1
        print(str(index) + " done!")

        # if index == 1:
        #     break

    wf.close()

def remove_ansi_escape_codes(input_str):
    # 定义ANSI转义码的正则表达式模式
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    # 使用正则表达式替换功能移除ANSI转义码
    return ansi_escape.sub('', input_str)

def verify_lua_script(script):
    function_def_str = "function  simu_start()\nend\nfunction  simu_sleep()\nend\nfunction  simu_assert(a)\nend\nfunction simu_get_port_value(a)\n    return 3.14\nend\nfunction simu_set_port_value(a)\nend\nfunction simu_get_current_time()\n    return 3.35\nend\nfunction  simu_stop()\nend\n"
    script = function_def_str + script
    with open("test.lua", "w") as f:
        f.write(script)
    try:
        # 运行luacheck并获取输出
        output = subprocess.check_output(['luacheck', "test.lua"], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        # 如果luacheck返回非零退出状态，那么就打印出错误信息
        start_str = "/ "
        end_str = " error"
        num_error = re.search(f"{start_str}(.*?){end_str}", e.output.decode())
        print(f"Syntax errors in test.lua: {num_error.group(1)}")
        if remove_ansi_escape_codes(num_error.group(1)) == "0":
            print(f"No syntax errors in test.lua.")
            return True, "No syntax errors in test.lua."
        else:
            return False, remove_ansi_escape_codes(e.output.decode())
    else:
        # 如果luacheck返回零退出状态，那么就表示语法正确
        print(f"No syntax errors in test.lua.")
        return True, "No syntax errors in test.lua."

num_test_case_list = [300000]
num_test_case_list.reverse()

for num_test_case in num_test_case_list:
    checkpoint = "finetune_starcoder2_mix_" + str(num_test_case) + "/final_checkpoint"
    model = "bigcode/starcoder2-3b"
    device = "cuda" # for GPU usage or "cpu" for CPU usage
    quantization_config = BitsAndBytesConfig(load_in_8bit=True)

    tokenizer = AutoTokenizer.from_pretrained(model)
    model = AutoModelForCausalLM.from_pretrained(checkpoint).to(device)

    final_result_file = jsonlines.open("mix_data/test/test_mix_total_" + str(num_test_case) + "_result.jsonl", mode = "w")

    generate_file = jsonlines.open("mix_data/test/test_mix_total_generate_" + str(num_test_case) + "_result.jsonl", mode = "r")
    for generate_script in generate_file:
        script_str = generate_script["output"][0]
        case_str = generate_script["input"][0]
        final_result_obj = {}

        max_try = 20
        try_times = 0
        while True:
            if try_times > max_try:
                final_result_obj["case"] = case_str
                final_result_obj["script"] = script_str
                final_result_obj["result"] = False
                final_result_obj["reason"] = "try times is max"
                break
            
            (verify_result, error_log) = verify_lua_script(script_str)
            try_times += 1
            if verify_result == True:
                input_str = "/verify\n//case\n" + generate_script["input"][0] + "//case_end\n//script\n" + script_str + "//script_end\n/verify_end\n"
                inputs = tokenizer.encode(input_str, return_tensors="pt").to(device)
                eos_token_id = tokenizer.eos_token_id
                pad_token_id = tokenizer.pad_token_id
                outputs = model.generate(inputs, max_length=int(inputs.shape[1] * 1.5), eos_token_id=eos_token_id, pad_token_id=pad_token_id, do_sample=True, temperature=0.25)
                script = tokenizer.decode(outputs[0])
                print(script)
                exception_flag = False
                script_line = script.split("\n")
                inputs_str_line_num = len(input_str.split("\n"))
                if len(script_line) < inputs_str_line_num:
                    exception_flag = True
                else:
                    if script_line[inputs_str_line_num - 1] != "/verified_script":
                        exception_flag = True
                    else:
                        script = re.search(f"{verify_output_start_str}(.*?){verify_output_end_str}", script, re.DOTALL)
                        if script == None:
                            outputs = model.generate(inputs, max_length=int(inputs.shape[1] * 2), eos_token_id=eos_token_id, pad_token_id=pad_token_id, do_sample=True, temperature=0.25)
                            script = tokenizer.decode(outputs[0])
                            script = re.search(f"{verify_output_start_str}(.*?){verify_output_end_str}", script, re.DOTALL)
                            if script == None:
                                outputs = model.generate(inputs, max_length=int(inputs.shape[1] * 2.5), eos_token_id=eos_token_id, pad_token_id=pad_token_id, do_sample=True, temperature=0.25)
                                script = tokenizer.decode(outputs[0])
                                script = re.search(f"{verify_output_start_str}(.*?){verify_output_end_str}", script, re.DOTALL)
                                if script == None:
                                    print("Error: script is None")
                                    exception_flag = True
                if exception_flag == True:
                    final_result_obj["case"] = generate_script["input"][0]
                    final_result_obj["script"] = script_str
                    final_result_obj["result"] = False
                    final_result_obj["reason"] = "verify generate failed"
                    break
                else:
                    script = script.group(1)
                    verify_result = re.search(f"{result_str}(.*?){result_end_str}", script, re.DOTALL)
                    if verify_result == None:
                        final_result_obj["case"] = generate_script["input"][0]
                        final_result_obj["script"] = script_str
                        final_result_obj["result"] = False
                        final_result_obj["reason"] = "verify result is None"
                        break
                    else:
                        verify_result = verify_result.group(1)
                        if verify_result == "Correct\n":
                            final_result_obj["case"] = generate_script["input"][0]
                            final_result_obj["script"] = script_str
                            final_result_obj["result"] = True
                            final_result_obj["reason"] = "verify success"
                            num_correct_generate += 1
                            break
                        else:
                            verified_script = re.search(f"{verified_str}(.*?){verified_end_str}", script, re.DOTALL)
                            if verified_script == None:
                                final_result_obj["case"] = generate_script["input"][0]
                                final_result_obj["script"] = script_str
                                final_result_obj["result"] = False
                                final_result_obj["reason"] = "verified script is None"
                                break
                            else:
                                verified_script = verified_script.group(1)
                                script_str = verified_script

            else:
                input_str = "/fix\n//case\n" + case_str + "//case_end\n//error_script\n" + script_str + "//error_script_end\n//error_log\n" + error_log + "//error_log_end\n/fix_end\n"
                inputs = tokenizer.encode(input_str, return_tensors="pt").to(device)
                eos_token_id = tokenizer.eos_token_id
                pad_token_id = tokenizer.pad_token_id
                outputs = model.generate(inputs, max_length=int(inputs.shape[1] * 1.5), eos_token_id=eos_token_id, pad_token_id=pad_token_id, do_sample=True, temperature=0.25)
                script = tokenizer.decode(outputs[0])
                print(script)
                exception_flag = False
                script_line = script.split("\n")
                inputs_str_line_num = len(input_str.split("\n"))
                if len(script_line) < inputs_str_line_num:
                    exception_flag = True
                    print("Error: script_line is less than inputs_str_line_num")
                else:
                    print("[line]",script_line[inputs_str_line_num - 1])
                    if script_line[inputs_str_line_num - 1] != "/correct_script":
                        exception_flag = True
                        print("Error: script_line is not /correct_script")
                    else:
                        script = re.search(f"{fix_output_start_str}(.*?){fix_output_end_str}", script, re.DOTALL)
                        if script == None:
                            outputs = model.generate(inputs, max_length=int(inputs.shape[1] * 2), eos_token_id=eos_token_id, pad_token_id=pad_token_id, do_sample=True, temperature=0.25)
                            script = tokenizer.decode(outputs[0])
                            script = re.search(f"{fix_output_start_str}(.*?){fix_output_end_str}", script, re.DOTALL)
                            if script == None:
                                outputs = model.generate(inputs, max_length=int(inputs.shape[1] * 2.5), eos_token_id=eos_token_id, pad_token_id=pad_token_id, do_sample=True, temperature=0.25)
                                script = tokenizer.decode(outputs[0])
                                script = re.search(f"{fix_output_start_str}(.*?){fix_output_end_str}", script, re.DOTALL)
                                if script == None:
                                    print("Error: script is None")
                                    exception_flag = True
                if exception_flag == True:
                    final_result_obj["case"] = generate_script["input"][0]
                    final_result_obj["script"] = script_str
                    final_result_obj["result"] = False
                    final_result_obj["reason"] = "fix generate failed"
                    break
                else:
                    script = script.group(1)
                    script_str = script
        
        final_result_file.write(final_result_obj)

    final_result_file.close()
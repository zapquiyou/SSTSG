from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, AutoConfig
import jsonlines
import re

num_test_case_list = [100, 250, 500, 1000, 2500, 5000, 10000, 25000, 50000, 100000]

for num_test_case in num_test_case_list:

    checkpoint = "finetune_starcoder2_verify_" + str(num_test_case) + "/final_checkpoint"
    model = "bigcode/starcoder2-3b"
    device = "cuda"
    quantization_config = BitsAndBytesConfig(load_in_8bit=True)

    tokenizer = AutoTokenizer.from_pretrained(model)
    model = AutoModelForCausalLM.from_pretrained(checkpoint).to(device)

    cj = jsonlines.open("verify_data/test/verify_test_1000.jsonl", mode = "r")
    wf = jsonlines.open("verify_data/test/verify_test_" + str(num_test_case) + "_result.jsonl", mode = "w")

    index = 0
    input_start_str = "/verify\n"
    input_end_str = "/verify_end\n"
    output_start_str = "/verified_script\n"
    output_end_str = "/verified_script_end\n"
    for input_scripts in cj:

        fixed_script = []
        error_script = []
        exception_flag = False
        input_str = re.search(f"{input_start_str}(.*?){input_end_str}", input_scripts["content"], re.DOTALL)
        if input_str == None:
            print("Error: input_str is None")
            raise Exception("Error: input_str is None")
        input_str = input_str.group(1)

        inputs = tokenizer.encode(input_start_str + input_str + input_end_str, return_tensors="pt").to(device)
        eos_token_id = tokenizer.eos_token_id
        pad_token_id = tokenizer.pad_token_id
        outputs = model.generate(inputs, max_length=int(inputs.shape[1] * 1.5), eos_token_id=eos_token_id, pad_token_id=pad_token_id, do_sample=False, temperature=0.75)
        script = tokenizer.decode(outputs[0])
        print(script)
        script_line = script.split("\n")
        inputs_str_line_num = len(input_str.split("\n"))
        if len(script_line) < inputs_str_line_num:
            exception_flag = True
        else:
            if script_line[inputs_str_line_num + 1] != "/verified_script":
                exception_flag = True
            else:
                script = re.search(f"{output_start_str}(.*?){output_end_str}", script, re.DOTALL)
                if script == None:
                    outputs = model.generate(inputs, max_length=int(inputs.shape[1] * 2), eos_token_id=eos_token_id, pad_token_id=pad_token_id, do_sample=False, temperature=0.75)
                    script = tokenizer.decode(outputs[0])
                    script = re.search(f"{output_start_str}(.*?){output_end_str}", script, re.DOTALL)
                    if script == None:
                        outputs = model.generate(inputs, max_length=int(inputs.shape[1] * 2.5), eos_token_id=eos_token_id, pad_token_id=pad_token_id, do_sample=False, temperature=0.75)
                        script = tokenizer.decode(outputs[0])
                        script = re.search(f"{output_start_str}(.*?){output_end_str}", script, re.DOTALL)
                        if script == None:
                            print("Error: script is None")
                            exception_flag = True
        if exception_flag == True:
            script = "ERROR!\n"
        else:
            script = script.group(1)
        fixed_script.append(script)
        error_script.append(input_str)

        wf.write({"input": error_script, "output": fixed_script})
        index += 1
        print(str(index) + " done!")

    wf.close()
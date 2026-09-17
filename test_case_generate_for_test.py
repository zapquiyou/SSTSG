import random
import string
from nltk.corpus import words
import math

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

def GenerateRandomJudge(is_condition, is_overtime, is_duration, is_keywork):
    is_zero = random.randint(0, 2)
    if is_zero == 0:
        random_time = "0"
    else:
        random_time = random.uniform(0, 50)
        random_time = "{:.3f}".format(random_time)

    all_chars = string.digits + '_.-' + string.ascii_letters
    operator = ['=', '<', '<=', '>=', '>' , '∈']
    option = ['&', '|']
    keyword = ['JUDGE', 'SIMSET', 'simu_start', 'simu_stop', 'simmu_sleep', 'simu_assert', 'simu_get_port_value', 'simu_set_port_value', 'simu_get_current_time', 'overtime', 'duration', 'condition']
    random_word_list = words.words()

    random_option_num = random.randint(1, 3)
    res = str()

    for i in range(random_option_num):
        random_model_name_len = random.randint(1, 5)
        random_word_num = random.randint(1, min(2, random_model_name_len))
        if random_word_num == 2:
            random_word2_index = random.randint(1, random_model_name_len - 1)
        else:
            random_word2_index = -1
        random_model = str()
        for j in range(random_model_name_len):
            if j == 0:
                if is_keywork == True:
                    random_keyword_num = random.randint(1, 1000)
                    if random_keyword_num == 1:
                        random_model += random.choice(keyword)
                    else:
                        random_model += random.choice(random_word_list)
                else:
                    random_model += random.choice(random_word_list)
            elif j == random_word2_index:
                if is_keywork == True:
                    random_keyword_num = random.randint(1, 1000)
                    if random_keyword_num == 1:
                        random_model += random.choice(keyword)
                    else:
                        random_model += random.choice(random_word_list)
                else:
                    random_model += random.choice(random_word_list)
            else:
                random_model += random.choice(all_chars)
        random_model = random_change_string_case(random_model)
        
        random_port_name_len = random.randint(1, 5)
        random_word_num = random.randint(1, min(2, random_port_name_len))
        if random_word_num == 2:
            random_word2_index = random.randint(1, random_port_name_len - 1)
        random_port = str()
        for j in range(random_port_name_len):
            if j == 0:
                if is_keywork == True:
                    random_keyword_num = random.randint(1, 1000)
                    if random_keyword_num == 1:
                        random_port += random.choice(keyword)
                    else:
                        random_port += random.choice(random_word_list)
                else:
                    random_port += random.choice(random_word_list)
            elif j == random_word2_index:
                if is_keywork == True:
                    random_keyword_num = random.randint(1, 1000)
                    if random_keyword_num == 1:
                        random_port += random.choice(keyword)
                    else:
                        random_port += random.choice(random_word_list)
                else:
                    random_port += random.choice(random_word_list)
            else:
                random_port += random.choice(all_chars)
        random_port = random_change_string_case(random_port)

        random_operator = random.choice(operator)

        if random_operator != '∈':
            is_int = random.randint(0, 1)
            if is_int == 0:
                random_value = random.uniform(-100000, 100000)
                random_value = "{:.4f}".format(random_value).rstrip('0').rstrip('.')
            else:
                random_value = random.randint(-100000, 100000)
            
            res += f"{random_model}@{random_port}{random_operator}{random_value}"
        else:
            is_int = random.randint(0, 1)
            if is_int == 0:
                random_lower_value = random.uniform(-100000, 100000)
                random_lower_value = "{:.4f}".format(random_lower_value).rstrip('0').rstrip('.')
            else:
                random_lower_value = random.randint(-100000, 100000)
            is_int = random.randint(0, 1)
            if is_int == 0:
                random_upper_value = random.uniform(math.ceil(float(random_lower_value)), 100000)
                random_upper_value = "{:.4f}".format(random_upper_value).rstrip('0').rstrip('.')
            else:
                random_upper_value = random.randint(math.ceil(float(random_lower_value)), 100000)
            
            res += f"{random_model}@{random_port}{random_operator}[{random_lower_value},{random_upper_value}]"

        if i != random_option_num - 1:
            res += f" {random.choice(option)} "

    random_option_num = random.randint(1, 3)
    res_condition = str()
    for i in range(random_option_num):
        random_model_name_len = random.randint(1, 5)
        random_word_num = random.randint(1, min(2, random_model_name_len))
        if random_word_num == 2:
            random_word2_index = random.randint(1, random_model_name_len - 1)
        random_model = str()
        for j in range(random_model_name_len):
            if j == 0:
                if is_keywork == True:
                    random_keyword_num = random.randint(1, 1000)
                    if random_keyword_num == 1:
                        random_model += random.choice(keyword)
                    else:
                        random_model += random.choice(random_word_list)
                else:
                    random_model += random.choice(random_word_list)
            elif j == random_word2_index:
                if is_keywork == True:
                    random_keyword_num = random.randint(1, 1000)
                    if random_keyword_num == 1:
                        random_model += random.choice(keyword)
                    else:
                        random_model += random.choice(random_word_list)
                else:
                    random_model += random.choice(random_word_list)
            else:
                random_model += random.choice(all_chars)
        random_model = random_change_string_case(random_model)
        
        random_port_name_len = random.randint(1, 5)
        random_word_num = random.randint(1, min(2, random_port_name_len))
        if random_word_num == 2:
            random_word2_index = random.randint(1, random_port_name_len - 1)
        random_port = str()
        for j in range(random_port_name_len):
            if j == 0:
                if is_keywork == True:
                    random_keyword_num = random.randint(1, 1000)
                    if random_keyword_num == 1:
                        random_port += random.choice(keyword)
                    else:
                        random_port += random.choice(random_word_list)
                else:
                    random_port += random.choice(random_word_list)
            elif j == random_word2_index:
                if is_keywork == True:
                    random_keyword_num = random.randint(1, 1000)
                    if random_keyword_num == 1:
                        random_port += random.choice(keyword)
                    else:
                        random_port += random.choice(random_word_list)
                else:
                    random_port += random.choice(random_word_list)
            else:
                random_port += random.choice(all_chars)
        random_port = random_change_string_case(random_port)

        random_operator = random.choice(operator)

        if random_operator != '∈':
            is_int = random.randint(0, 1)
            if is_int == 0:
                random_value = random.uniform(-100000, 100000)
                random_value = "{:.4f}".format(random_value).rstrip('0').rstrip('.')
            else:
                random_value = random.randint(-100000, 100000)
            
            res_condition += f"{random_model}@{random_port}{random_operator}{random_value}"
        else:
            is_int = random.randint(0, 1)
            if is_int == 0:
                random_lower_value = random.uniform(-100000, 100000)
                random_lower_value = "{:.4f}".format(random_lower_value).rstrip('0').rstrip('.')
            else:
                random_lower_value = random.randint(-100000, 100000)
            is_int = random.randint(0, 1)
            if is_int == 0:
                random_upper_value = random.uniform(math.ceil(float(random_lower_value)), 100000)
                random_upper_value = "{:.4f}".format(random_upper_value).rstrip('0').rstrip('.')
            else:
                random_upper_value = random.randint(math.ceil(float(random_lower_value)), 100000)
            
            res_condition += f"{random_model}@{random_port}{random_operator}[{random_lower_value},{random_upper_value}]"

        if i != random_option_num - 1:
            res_condition += f" {random.choice(option)} "
    res_condition = res_condition.replace(' ', '')

    is_int = random.randint(0, 1)
    if is_int == 0:
        random_overtime = random.uniform(0, 50)
        random_overtime = "{:.3f}".format(random_overtime).rstrip('0').rstrip('.')
    else:
        random_overtime = random.randint(0, 50)

    is_int = random.randint(0, 1)
    if is_int == 0:
        random_duration = random.uniform(0, 50)
        random_duration = "{:.3f}".format(random_duration).rstrip('0').rstrip('.')
    else:
        random_duration = random.randint(0, 50)

    res = res.replace(' ', '')
    if is_condition == False and is_overtime == False and is_duration == False:
        res = f"JUDGE({random_time};{res})\n"
    elif is_condition == True and is_overtime == False and is_duration == False:
        res = f"JUDGE({random_time};{res};condition:{res_condition})\n"
    elif is_condition == False and is_overtime == True and is_duration == False:
        res = f"JUDGE({random_time};{res};overtime:{random_overtime})\n"
    elif is_condition == False and is_overtime == False and is_duration == True:
        res = f"JUDGE({random_time};{res};duration:{random_duration})\n"
    elif is_condition == True and is_overtime == True and is_duration == False:
        fields = [f"condition:{res_condition}", f"overtime:{random_overtime}"]
        random.shuffle(fields)
        res = f"JUDGE({random_time};{res};" + ";".join(fields) + ")\n"
    elif is_condition == True and is_overtime == False and is_duration == True:
        fields = [f"condition:{res_condition}", f"duration:{random_duration}"]
        random.shuffle(fields)
        res = f"JUDGE({random_time};{res};" + ";".join(fields) + ")\n"
    elif is_condition == False and is_overtime == True and is_duration == True:
        fields = [f"overtime:{random_overtime}", f"duration:{random_duration}"]
        random.shuffle(fields)
        res = f"JUDGE({random_time};{res};" + ";".join(fields) + ")\n"
    elif is_condition == True and is_overtime == True and is_duration == True:
        fields = [f"condition:{res_condition}", f"overtime:{random_overtime}", f"duration:{random_duration}"]
        random.shuffle(fields)
        res = f"JUDGE({random_time};{res};" + ";".join(fields) + ")\n"

    return res

def GenerateRandomSimset(is_condition, is_keywork):
    is_zero = random.randint(0, 2)
    if is_zero == 0:
        random_time = "0"
    else:
        random_time = random.uniform(0, 50)
        random_time = "{:.3f}".format(random_time)

    all_chars = string.digits + '_.-' + string.ascii_letters
    operator = ['=', '<', '<=', '>=', '>' , '∈']
    keyword = ['JUDGE', 'SIMSET', 'simu_start', 'simu_stop', 'simmu_sleep', 'simu_assert', 'simu_get_port_value', 'simu_set_port_value', 'simu_get_current_time', 'overtime', 'duration', 'condition']
    option = ['&', '|']
    random_word_list = words.words()

    res = str()

    random_model_name_len = random.randint(1, 5)
    random_word_num = random.randint(1, min(2, random_model_name_len))
    if random_word_num == 2:
        random_word2_index = random.randint(1, random_model_name_len - 1)
    else:
        random_word2_index = -1
    random_model = str()
    for j in range(random_model_name_len):
        if j == 0:
            if is_keywork == True:
                random_keyword_num = random.randint(1, 1000)
                if random_keyword_num == 1:
                    random_model += random.choice(keyword)
                else:
                    random_model += random.choice(random_word_list)
            else:
                random_model += random.choice(random_word_list)
        elif j == random_word2_index:
            if is_keywork == True:
                random_keyword_num = random.randint(1, 1000)
                if random_keyword_num == 1:
                    random_model += random.choice(keyword)
                else:
                    random_model += random.choice(random_word_list)
            else:
                random_model += random.choice(random_word_list)
        else:
            random_model += random.choice(all_chars)
    
    random_port_name_len = random.randint(1, 5)
    random_word_num = random.randint(1, min(2, random_port_name_len))
    if random_word_num == 2:
        random_word2_index = random.randint(1, random_port_name_len - 1)
    random_port = str()
    for j in range(random_port_name_len):
        if j == 0:
            if is_keywork == True:
                random_keyword_num = random.randint(1, 1000)
                if random_keyword_num == 1:
                    random_port += random.choice(keyword)
                else:
                    random_port += random.choice(random_word_list)
            else:
                random_port += random.choice(random_word_list)
        elif j == random_word2_index:
            if is_keywork == True:
                random_keyword_num = random.randint(1, 1000)
                if random_keyword_num == 1:
                    random_port += random.choice(keyword)
                else:
                    random_port += random.choice(random_word_list)
            else:
                random_port += random.choice(random_word_list)
        else:
            random_port += random.choice(all_chars)

    is_int = random.randint(0, 1)
    random_value = 0
    if is_int == 0:
        random_value = random.uniform(-100000, 100000)
        random_value = "{:.4f}".format(random_value).rstrip('0').rstrip('.')
    else:
        random_value = random.randint(-100000, 100000)

    random_option_num = random.randint(1, 3)
    res_condition = str()
    for i in range(random_option_num):
        random_model_name_len = random.randint(1, 5)
        random_word_num = random.randint(1, min(2, random_model_name_len))
        if random_word_num == 2:
            random_word2_index = random.randint(1, random_model_name_len - 1)
        random_model = str()
        for j in range(random_model_name_len):
            if j == 0:
                random_model += random.choice(random_word_list)
            elif j == random_word2_index:
                random_model += random.choice(random_word_list)
            else:
                random_model += random.choice(all_chars)
        
        random_model = random_change_string_case(random_model)
        
        random_port_name_len = random.randint(1, 5)
        random_word_num = random.randint(1, min(2, random_port_name_len))
        if random_word_num == 2:
            random_word2_index = random.randint(1, random_port_name_len - 1)
        random_port = str()
        for j in range(random_port_name_len):
            if j == 0:
                if is_keywork == True:
                    random_keyword_num = random.randint(1, 1000)
                    if random_keyword_num == 1:
                        random_port += random.choice(keyword)
                    else:
                        random_port += random.choice(random_word_list)
                else:
                    random_port += random.choice(random_word_list)
            elif j == random_word2_index:
                if is_keywork == True:
                    random_keyword_num = random.randint(1, 1000)
                    if random_keyword_num == 1:
                        random_port += random.choice(keyword)
                    else:
                        random_port += random.choice(random_word_list)
                else:
                    random_port += random.choice(random_word_list)
            else:
                random_port += random.choice(all_chars)
        random_port = random_change_string_case(random_port)

        random_operator = random.choice(operator)

        if random_operator != '∈':
            is_int = random.randint(0, 1)
            random_value = 0
            if is_int == 0:
                random_value = random.uniform(-100000, 100000)
                random_value = "{:.4f}".format(random_value).rstrip('0').rstrip('.')
            else:
                random_value = random.randint(-100000, 100000)

            res_condition += f"{random_model}@{random_port}{random_operator}{random_value}"
        else:
            is_int = random.randint(0, 1)
            if is_int == 0:
                random_lower_value = random.uniform(-100000, 100000)
                random_lower_value = "{:.4f}".format(random_lower_value).rstrip('0').rstrip('.')
            else:
                random_lower_value = random.randint(-100000, 100000)
            is_int = random.randint(0, 1)
            if is_int == 0:
                random_upper_value = random.uniform(math.ceil(float(random_lower_value)), 100000)
                random_upper_value = "{:.4f}".format(random_upper_value).rstrip('0').rstrip('.')
            else:
                random_upper_value = random.randint(math.ceil(float(random_lower_value)), 100000)
            
            res_condition += f"{random_model}@{random_port}{random_operator}[{random_lower_value},{random_upper_value}]"

        if i != random_option_num - 1:
            res_condition += f" {random.choice(option)} "
    res_condition = res_condition.replace(' ', '')

    if is_condition == False:

        res = f"SIMSET({random_time};{random_model}@{random_port}={random_value})\n"
    else:
        res = f"SIMSET({random_time};{random_model}@{random_port}={random_value};condition:{res_condition})\n"

    return res

file_path_list = ["generate_data/test/generate_test_", "fix_data/test/fix_test_", "verify_data/test/verify_test_"]
case_num_list = [100]
for file_path in file_path_list:
    for case_num in case_num_list:
        judge_num = case_num
        special_word_flag = True
        file = open(file_path + str(case_num * 10) + ".txt", "w", encoding='utf-8')
        for i in range(judge_num):
            file.write("--------Test_Cases--------:\n")
            file.write(GenerateRandomJudge(False, False, False, special_word_flag))
            print("judge " + str(i) + " done")

        judge_c_num = case_num
        for i in range(judge_c_num):
            file.write("--------Test_Cases--------:\n")
            file.write(GenerateRandomJudge(True, False, False, special_word_flag))
            print("judge_c " + str(i) + " done")

        judge_o_num = case_num
        for i in range(judge_o_num):
            file.write("--------Test_Cases--------:\n")
            file.write(GenerateRandomJudge(False, True, False, special_word_flag))
            print("judge_o " + str(i) + " done")

        judge_d_num = case_num
        for i in range(judge_d_num):
            file.write("--------Test_Cases--------:\n")
            file.write(GenerateRandomJudge(False, False, True, special_word_flag))
            print("judge_d " + str(i) + " done")

        judge_co_num = case_num
        for i in range(judge_co_num):
            file.write("--------Test_Cases--------:\n")
            file.write(GenerateRandomJudge(True, True, False, special_word_flag))
            print("judge_co " + str(i) + " done")

        judge_cd_num = case_num
        for i in range(judge_cd_num):
            file.write("--------Test_Cases--------:\n")
            file.write(GenerateRandomJudge(False, True, True, special_word_flag))
            print("judge_cd " + str(i) + " done")

        judge_od_num = case_num
        for i in range(judge_od_num):
            file.write("--------Test_Cases--------:\n")
            file.write(GenerateRandomJudge(False, True, True, special_word_flag))
            print("judge_od " + str(i) + " done")

        judge_cod_num = case_num
        for i in range(judge_cod_num):
            file.write("--------Test_Cases--------:\n")
            file.write(GenerateRandomJudge(True, True, True, special_word_flag))
            print("judge_cod " + str(i) + " done")

        simset_num = case_num
        for i in range(simset_num):
            file.write("--------Test_Cases--------:\n")
            file.write(GenerateRandomSimset(False, special_word_flag))
            print("simset " + str(i) + " done")

        simset_c_num = case_num
        for i in range(simset_c_num):
            file.write("--------Test_Cases--------:\n")
            file.write(GenerateRandomSimset(True, special_word_flag))
            print("simset_c " + str(i) + " done")

        file.close()
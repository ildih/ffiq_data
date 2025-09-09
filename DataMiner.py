import re
import pandas as pd 

filename = '2025_proj.txt'

def get_pos(s):
    
    match = re.search(r'(\d{1,3})$', s)
    digits = match.group(1)           
    rest = s[:-len(digits)]           
    return rest

def convert_adp(adp, current_size=12, new_size=10):
    round_num = int(adp)
    pick_num = round((adp - round_num) * 100)
    
    overall_pick = (round_num - 1) * current_size + pick_num
    
    new_round = (overall_pick - 1) // new_size + 1
    new_pick = (overall_pick - 1) % new_size + 1

    return f"{new_round}.{new_pick:02d}"

def convert_adp_to_pick(adp):
    adp = float(adp)
    round_ = int(adp)
    pick = round((adp - round_) * 100)
    return (round_ - 1) * 10 + pick

df_data = []
with open(filename, 'r') as f:
    
    lines = [line.strip() for line in f if line.strip()]    
    data = [lines[i:i+10] for i in range(0, len(lines), 10)]

    for player in data:
        name = str(player[1])
        pos = str(get_pos(player[3]))
        adp = float(player[5].split()[1])
        sos = float(player[5].split()[3][:-1])
        inj = int(player[5].split()[4][:-1])
        min_ = int(player[6])
        avg = int(player[7])
        max_ = int(player[8])
        val = int(player[9])
        
        df_data.append([name, pos, adp, sos, inj, min_, avg, max_])
        
df = pd.DataFrame(df_data, columns=['Name', 'Pos', 'ADP', 'SoS', 'Inj', 'Min', 'Avg', 'Max'])
df['ADP'] = df['ADP'].apply(convert_adp)
df["EDP"] = df["ADP"].apply(convert_adp_to_pick)
df[['SoS']] = df[['SoS']] * -1
df['Tlt'] = (df['Max'] - df['Avg']) - (df['Avg'] - df['Min'])
df = df[['Name', 'Pos', 'EDP', 'SoS', 'Inj', 'Min', 'Avg', 'Max', 'Tlt']]
df.to_json('proj_2025.json', orient='records', indent=2)
df.to_csv('2025_proj.csv', index=False)

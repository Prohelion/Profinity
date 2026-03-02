import requests
import matplotlib.pyplot as plt
import re
from collections import defaultdict
import getpass

def login(server_url, username, password):
    """
    Authenticates and returns a token.
    """
    login_endpoint = '/api/V2/Users/Authenticate'
    login_url = server_url + login_endpoint
    login_data = {'username': username, 'password': password}
    resp = requests.post(login_url, json=login_data, timeout=20)
    resp.raise_for_status()
    login_response = resp.json()
    token = login_response.get('token')
    if not token:
        raise RuntimeError('No token received from server.')
    return token

def get_cmu_cell_voltages(server_url, token):
    """
    Fetches BMS data and returns a dict {cmu_number: [cell_voltages]}.
    """
    bmu_endpoint = '/api/v2/Data/Prohelion%20BMU'
    bmu_url = server_url + bmu_endpoint
    headers = {'Authorization': f'Bearer {token}'}
    resp = requests.get(bmu_url, headers=headers, timeout=20)
    resp.raise_for_status()
    bms_data = resp.json()
    # Parse voltages
    cmu_pattern = re.compile(r'Cmu(\d+)Cells(\d+)to(\d+)Voltages')
    cmu_groups = defaultdict(list)
    for key in bms_data:
        m = cmu_pattern.fullmatch(key)
        if m:
            cmu_num = int(m.group(1))
            start_cell = int(m.group(2))
            voltages = bms_data[key]
            cmu_groups[cmu_num].append((start_cell, voltages))
    if not cmu_groups:
        raise RuntimeError('No CMU cell voltage data found in response.')
    # Build output: {cmu_num: [cell_voltages]}
    cmu_voltages = {}
    for cmu_num in sorted(cmu_groups):
        cell_chunks = sorted(cmu_groups[cmu_num], key=lambda x: x[0])
        voltages = []
        for _, vdict in cell_chunks:
            for cell_key in sorted(vdict, key=lambda k: int(k.replace('Cell',''))):
                voltages.append(vdict[cell_key])
        cmu_voltages[cmu_num] = voltages
    return cmu_voltages

# Main script
if __name__ == '__main__':
    default_server_url = 'http://127.0.0.1:18080'
    server_url = input(f'Enter Prohelion API server URL [{default_server_url}]: ').strip()
    if not server_url:
        server_url = default_server_url
    username = input('Enter your Prohelion API username: ').strip()
    password = getpass.getpass('Enter your Prohelion API password: ')
    try:
        token = login(server_url, username, password)
        cmu_voltages = get_cmu_cell_voltages(server_url, token)
    except Exception as e:
        print(f'Error: {e}')
        exit(1)
    # Set any negative voltages to zero
    for cmu_num in cmu_voltages:
        cmu_voltages[cmu_num] = [v if v >= 0 else 0 for v in cmu_voltages[cmu_num]]
    # Plot
    plt.figure()
    for cmu_num in sorted(cmu_voltages):
        v = cmu_voltages[cmu_num]
        idx = [i+1 for i, val in enumerate(v) if val > 0]  # 1-based index for values > 0
        vals = [val for val in v if val > 0]
        plt.plot(idx, vals, '-o', label=f'CMU {cmu_num}')
    plt.xlabel('Cell Index')
    plt.ylabel('Voltage (V)')
    plt.title('Cell Voltages from Each CMU')
    plt.legend()
    plt.grid(True)
    plt.ylim([2500, 4200])
    plt.show() 
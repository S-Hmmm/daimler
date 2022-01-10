import yaml
import os
import pandas as pd


def yaml_data_load(file_name):
    yaml_path = os.path.join(os.path.dirname(__file__), file_name)
    case, http, expected = [], [], []

    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.load(f.read(), Loader=yaml.SafeLoader)
        method = data['method']
        url = data['url']
        cases = data['cases']
        for item in cases:
            case.append(item.get('case', ''))
            http.append(item.get('http', {}))
            expected.append(item.get('expected', {}))
    parameters = zip(http, expected)

    return method, url, case, parameters


def yaml_load_ls(file_name):
    yaml_path = os.path.join(os.path.dirname(__file__), file_name)
    case, http, expected, ids = [], [], [], []

    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.load(f.read(), Loader=yaml.SafeLoader)
        method = data['method']
        url = data['url']
        cases = data['cases']
        for item in cases:
            for u in item.get('id'):
                case.append(item.get('case', ''))
                http.append(item.get('http', {}))
                expected.append(item.get('expected', {}))
                ids.append(u)
    parameters = zip(http, expected, ids)

    return method, url, case, parameters


def yaml_load(file_name):
    yaml_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.load(f.read(), Loader=yaml.SafeLoader)

    return data


def read_csv(file_name):
    csv_path = os.path.join(os.path.dirname(__file__), file_name)
    cases = []

    df = pd.read_csv(csv_path)
    max_row = df.shape[0]
    if max_row > 0:
        for row in range(0, max_row):
            sub_data = {
                'case': df.loc[row, 'case'],
                'method': df.loc[row, 'method'],
                'url': df.loc[row, 'url'],
                'expected': df.loc[row, 'expected']
            }
            if not pd.isnull(df.loc[row, 'data']):
                sub_data['data'] = df.loc[row, 'data']
            cases.append(sub_data)

    return cases

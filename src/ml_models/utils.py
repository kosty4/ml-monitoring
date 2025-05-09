
def write_to_env(key: str, value: str, env_file='.env'):
    with open(env_file, 'w') as f:
        f.write(f'{key}={value}\n')
    print(f"{env_file} file update with: {key}={value}")
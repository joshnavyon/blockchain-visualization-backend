def get_constant_value(key):
    try:
        with open('config.txt', 'r') as file:
            for line in file:
                if key in line:
                    # Parse the value from the line
                    _, value_str = line.split('=')
                    return value_str.strip()
    except FileNotFoundError:
        pass

    # Default value if the file doesn't exist or the constant isn't found
    return None

NEO4J_URI = get_constant_value("NEO4J_URI")
NEO4J_USERNAME = get_constant_value("NEO4J_USERNAME")
NEO4J_PASSWORD = get_constant_value("NEO4J_PASSWORD")


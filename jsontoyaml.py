import json
import yaml

def convert_json_to_yaml(json_file_path, yaml_file_path):
    """
    Converts a JSON file to a YAML file.

    :param json_file_path: Path to the input JSON file.
    :param yaml_file_path: Path to the output YAML file.
    """
    try:
        # Read the JSON file
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)

        # Write to the YAML file
        with open(yaml_file_path, 'w') as yaml_file:
            yaml.dump(data, yaml_file, default_flow_style=False)

        print(f"Successfully converted {json_file_path} to {yaml_file_path}")

    except Exception as e:
        print(f"Error: {e}")

# Example usage
if __name__ == "__main__":
    json_file_path = "input.json"  # Replace with your JSON file path
    yaml_file_path = "output.yaml" # Replace with your desired YAML file path
    convert_json_to_yaml(json_file_path, yaml_file_path)

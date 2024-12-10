import json
import yaml

def transform_spinnaker_to_harness(data):
    """
    Transform Spinnaker JSON structure to Harness YAML structure.
    Modify this function based on specific requirements.
    """
    # Example transformation logic
    transformed_data = data.copy()
    if 'spinnakerKey' in transformed_data:
        transformed_data['harnessKey'] = transformed_data.pop('spinnakerKey')
    # Add more transformations as needed
    return transformed_data

def convert_json_to_yaml(json_file_path, yaml_file_path):
    """
    Converts a JSON file to a YAML file with specific transformations.

    :param json_file_path: Path to the input JSON file.
    :param yaml_file_path: Path to the output YAML file.
    """
    try:
        # Read the JSON file
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)

        # Transform the data
        transformed_data = transform_spinnaker_to_harness(data)

        # Write to the YAML file
        with open(yaml_file_path, 'w') as yaml_file:
            yaml.dump(transformed_data, yaml_file, default_flow_style=False)

        print(f"Successfully converted {json_file_path} to {yaml_file_path}")

    except Exception as e:
        print(f"Error: {e}")

# Example usage
if __name__ == "__main__":
    json_file_path = "/harnesstest5/spinnaker.json"  # Replace with your JSON file path
    yaml_file_path = "/harnesstest5/harness.yaml" # Replace with your desired YAML file path
    convert_json_to_yaml(json_file_path, yaml_file_path)

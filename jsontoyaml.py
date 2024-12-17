import json
import yaml

def transform_spinnaker_to_harness(data):
    """
    Transform Spinnaker JSON structure to Harness YAML structure.
    Modify this function based on specific requirements.
    """
    transformed_data = {}

    # Map pipeline metadata
    pipeline_name = data.get("name", "Default Pipeline")
    transformed_data["pipeline"] = {
        "name": pipeline_name,
        "identifier": pipeline_name.replace(" ", "_").lower(),
        "projectIdentifier": data.get("projectId", "default_project"),
        "orgIdentifier": data.get("orgId", "default_org"),
        "stages": []
    }

    # Transform stages
    for stage in data.get("stages", []):
        harness_stage = {
            "name": stage.get("name", "Unnamed Stage"),
            "type": stage.get("type", "Custom"),
            "spec": {}
        }

        if stage.get("type") == "deploy":
            harness_stage["type"] = "Deployment"
            harness_stage["spec"]["deploymentType"] = stage.get("deploymentType", "Kubernetes")
            harness_stage["spec"]["infrastructure"] = []

            for cluster in stage.get("clusters", []):
                infrastructure = {
                    "account": cluster.get("account"),
                    "application": cluster.get("application"),
                    "stack": cluster.get("stack"),
                    "details": cluster.get("details"),
                    "capacity": cluster.get("capacity", {})
                }
                harness_stage["spec"]["infrastructure"].append(infrastructure)

        elif stage.get("type") == "manualJudgment":
            harness_stage["type"] = "Approval"
            harness_stage["spec"]["approvalMessage"] = stage.get("approvalMessage", "Please approve this stage")
            harness_stage["spec"]["approvers"] = {
                "userGroups": stage.get("approvers", ["default_user_group"])
            }

        # Add transformed stage to the pipeline
        transformed_data["pipeline"]["stages"].append(harness_stage)

    # Transform triggers
    if "triggers" in data:
        transformed_data["pipeline"]["triggers"] = []
        for trigger in data["triggers"]:
            harness_trigger = {
                "name": trigger.get("name", "default_trigger"),
                "type": trigger.get("type", "Webhook"),
                "spec": {
                    "source": trigger.get("source", "git"),
                    "repo": trigger.get("repository", "default_repo"),
                    "branch": trigger.get("branch", "main")
                }
            }
            transformed_data["pipeline"]["triggers"].append(harness_trigger)

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

        # Write to the YAML file using safe_dump
        with open(yaml_file_path, 'w') as yaml_file:
            yaml.safe_dump(transformed_data, yaml_file, default_flow_style=False)

        print("Successfully converted {} to {}".format(json_file_path, yaml_file_path))

    except Exception as e:
        print("Error: {}".format(e))

def read_yaml_file(yaml_file_path):
    """
    Reads a YAML file and returns its content.

    :param yaml_file_path: Path to the YAML file.
    :return: Parsed YAML content.
    """
    try:
        with open(yaml_file_path, 'r') as yaml_file:
            data = yaml.safe_load(yaml_file)  # Ensure safe_load is used
            return data
    except Exception as e:
        print("Error reading YAML file: {}".format(e))
        return None

if __name__ == "__main__":
    json_file_path = "spinnaker.json"  # Replace with your JSON file path
    yaml_file_path = "harness.yaml"   # Replace with your desired YAML file path

    # Convert JSON to YAML
    convert_json_to_yaml(json_file_path, yaml_file_path)

    # Read and print the YAML content
    yaml_data = read_yaml_file(yaml_file_path)
    if yaml_data:
        print("YAML Content:")
        print(yaml.safe_dump(yaml_data, default_flow_style=False))

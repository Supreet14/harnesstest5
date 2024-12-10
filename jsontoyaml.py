import json
import yaml

def transform_spinnaker_to_harness(data):
    """
    Transform Spinnaker JSON structure to Harness YAML structure.
    Modify this function based on specific requirements.
    """
    transformed_data = {}

    # Map pipeline name
    transformed_data["pipeline"] = {
        "name": data.get("name", "Default Pipeline"),
        "identifier": data.get("name", "Default Pipeline").replace(" ", "_").lower(),
        "projectIdentifier": "default_project",  # Update with actual project ID
        "orgIdentifier": "default_org",  # Update with actual org ID
        "stages": []
    }

    # Transform stages
    for stage in data.get("stages", []):
        harness_stage = {
            "name": stage.get("name", "Unnamed Stage"),
            "type": stage.get("type", "Custom"),  # Map to Harness stage type
            "spec": {}
        }

        if stage.get("type") == "deploy":
            harness_stage["type"] = "Deployment"
            harness_stage["spec"]["deploymentType"] = "Kubernetes"  # Example

            # Example: Transform clusters to infrastructure
            if "clusters" in stage:
                harness_stage["spec"]["infrastructure"] = []
                for cluster in stage["clusters"]:
                    harness_stage["spec"]["infrastructure"].append({
                        "account": cluster.get("account"),
                        "application": cluster.get("application"),
                        "stack": cluster.get("stack"),
                        "details": cluster.get("details"),
                        "capacity": cluster.get("capacity")
                    })

        elif stage.get("type") == "manualJudgment":
            harness_stage["type"] = "Approval"
            harness_stage["spec"]["approvalMessage"] = "Please approve this stage"
            harness_stage["spec"]["approvers"] = {
                "userGroups": ["default_user_group"]  # Replace with actual user group
            }

        transformed_data["pipeline"]["stages"].append(harness_stage)

    # Transform triggers
    if "triggers" in data:
        transformed_data["pipeline"]["triggers"] = []
        for trigger in data["triggers"]:
            harness_trigger = {
                "type": "Webhook",  # Example: Map to Harness trigger type
                "spec": {
                    "source": trigger.get("source"),
                    "repo": trigger.get("repository"),
                    "branch": trigger.get("branch")
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

        # Write to the YAML file
        with open(yaml_file_path, 'w') as yaml_file:
            yaml.dump(transformed_data, yaml_file, default_flow_style=False)

        print("Successfully converted {} to {}".format(json_file_path, yaml_file_path))

    except Exception as e:
        print("Error: {}".format(e))

# Example usage
if __name__ == "__main__":
    json_file_path = "spinnaker.json"  # Replace with your JSON file path
    yaml_file_path = "harness.yaml" # Replace with your desired YAML file path
    convert_json_to_yaml(json_file_path, yaml_file_path)

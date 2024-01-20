import json

class JsonValidator:
    def __init__(self):
        pass

    def validate_schema(self, json_file, schema_file):
        """
        Validate JSON against a given schema file.
        :param json_file: Path to the JSON file to be validated
        :type json_file: str
        :param schema_file: Path to the schema file for validation
        :type schema_file: str
        :return: True if validation succeeds, False otherwise
        :rtype: bool
        """
        try:
            with open(json_file, 'r') as file:
                json_data = json.load(file)

            with open(schema_file, 'r') as file:
                schema = json.load(file)

            required_fields = schema.get('required_fields', [])
            at_least_one_fields = schema.get('at_least_one_fields', [])
            either_or_fields = schema.get('either_or_fields', [])
            mutually_exclusive_fields = schema.get('mutually_exclusive_fields', [])
            field_values = schema.get('field_values', {})

            return (
                self.validate_required_fields(json_data, required_fields) and
                self.validate_at_least_one_field(json_data, at_least_one_fields) and
                self.validate_either_or_fields(json_data, *either_or_fields) and
                self.validate_mutually_exclusive_fields(json_data, *mutually_exclusive_fields) and
                self.validate_field_values(json_data, **field_values)
            )

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False

    def validate_required_fields(self, json_data, required_fields):
        for field in required_fields:
            if field not in json_data:
                return False
        return True

    def validate_at_least_one_field(self, json_data, fields_to_check):
        for field in fields_to_check:
            if field in json_data:
                return True
        return False

    def validate_either_or_fields(self, json_data, field1, field2):
        if field1 in json_data and field2 in json_data:
            return False
        return True

    def validate_mutually_exclusive_fields(self, json_data, field1, field2):
        if field1 in json_data and field2 in json_data:
            return False
        return True

    def validate_field_values(self, json_data, field, allowed_values):
        if field in json_data and json_data[field] not in allowed_values:
            return False
        return True

# validator = JsonValidator()
# result = validator.validate_schema('your_json_file.json', 'your_schema_file.json')
# print(result)

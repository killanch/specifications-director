{
    "rest_name": "childapi",
    "resource_name": "childapis",
    "description": "Represents an child api.",
    "entity_name": "ChildAPI",
    "package": "specifications",
    "extends": ["@parsable"],

    "attributes": {
        "path": {
            "allowed_chars": null,
            "allowed_choices": null,
            "autogenerated": false,
            "availability": null,
            "channel": null,
            "creation_only": false,
            "default_order": false,
            "default_value": false,
            "description": "Defines if the api is deprecated",
            "exposed": true,
            "filterable": true,
            "format": null,
            "max_length": null,
            "max_value": null,
            "min_length": null,
            "min_value": null,
            "orderable": true,
            "read_only": true,
            "required": false,
            "transient": true,
            "type": "string",
            "unique": false
        },
        "specification": {
            "allowed_chars": null,
            "allowed_choices": null,
            "autogenerated": false,
            "availability": null,
            "channel": null,
            "creation_only": false,
            "default_order": false,
            "default_value": false,
            "description": "Defines if the api is deprecated",
            "exposed": true,
            "filterable": true,
            "format": null,
            "max_length": null,
            "max_value": null,
            "min_length": null,
            "min_value": null,
            "orderable": true,
            "read_only": false,
            "required": false,
            "transient": false,
            "type": "string",
            "unique": false
        },
        "deprecated": {
            "allowed_chars": null,
            "allowed_choices": null,
            "autogenerated": false,
            "availability": null,
            "channel": null,
            "creation_only": false,
            "default_order": false,
            "default_value": false,
            "description": "Defines if the api is deprecated",
            "exposed": true,
            "filterable": true,
            "format": null,
            "max_length": null,
            "max_value": null,
            "min_length": null,
            "min_value": null,
            "orderable": true,
            "read_only": false,
            "required": false,
            "transient": false,
            "type": "boolean",
            "unique": false
        },
        "relationship": {
            "allowed_chars": null,
            "allowed_choices": ["child", "member", "root"],
            "autogenerated": false,
            "availability": null,
            "channel": null,
            "creation_only": false,
            "default_order": false,
            "default_value": false,
            "description": "Defines if the api is deprecated",
            "exposed": true,
            "filterable": true,
            "format": null,
            "max_length": null,
            "max_value": null,
            "min_length": null,
            "min_value": null,
            "orderable": true,
            "read_only": false,
            "required": false,
            "transient": false,
            "type": "enum",
            "unique": false
        },
        "allowsGet": {
            "allowed_chars": null,
            "allowed_choices": null,
            "autogenerated": false,
            "availability": null,
            "channel": null,
            "creation_only": false,
            "default_order": false,
            "default_value": false,
            "description": "Defines if teh available operations",
            "exposed": true,
            "filterable": true,
            "format": null,
            "max_length": null,
            "max_value": null,
            "min_length": null,
            "min_value": null,
            "orderable": true,
            "read_only": false,
            "required": false,
            "transient": false,
            "type": "bool",
            "unique": false
        },
        "allowsCreate": {
            "allowed_chars": null,
            "allowed_choices": null,
            "autogenerated": false,
            "availability": null,
            "channel": null,
            "creation_only": false,
            "default_order": false,
            "default_value": false,
            "description": "Defines if teh available operations",
            "exposed": true,
            "filterable": true,
            "format": null,
            "max_length": null,
            "max_value": null,
            "min_length": null,
            "min_value": null,
            "orderable": true,
            "read_only": false,
            "required": false,
            "transient": false,
            "type": "bool",
            "unique": false
        },
        "allowsUpdate": {
            "allowed_chars": null,
            "allowed_choices": null,
            "autogenerated": false,
            "availability": null,
            "channel": null,
            "creation_only": false,
            "default_order": false,
            "default_value": false,
            "description": "Defines if teh available operations",
            "exposed": true,
            "filterable": true,
            "format": null,
            "max_length": null,
            "max_value": null,
            "min_length": null,
            "min_value": null,
            "orderable": true,
            "read_only": false,
            "required": false,
            "transient": false,
            "type": "bool",
            "unique": false
        },
        "allowsDelete": {
            "allowed_chars": null,
            "allowed_choices": null,
            "autogenerated": false,
            "availability": null,
            "channel": null,
            "creation_only": false,
            "default_order": false,
            "default_value": false,
            "description": "Defines if teh available operations",
            "exposed": true,
            "filterable": true,
            "format": null,
            "max_length": null,
            "max_value": null,
            "min_length": null,
            "min_value": null,
            "orderable": true,
            "read_only": false,
            "required": false,
            "transient": false,
            "type": "bool",
            "unique": false
        },
        "associatedSpecificationID": {
            "allowed_chars": null,
            "allowed_choices": null,
            "autogenerated": false,
            "availability": null,
            "channel": null,
            "creation_only": false,
            "default_order": false,
            "default_value": null,
            "description": "the associated specification.",
            "exposed": true,
            "filterable": true,
            "format": null,
            "max_length": null,
            "max_value": null,
            "min_length": null,
            "min_value": null,
            "orderable": false,
            "read_only": false,
            "required": false,
            "transient": false,
            "type": "string",
            "unique": false
        }
    }
}
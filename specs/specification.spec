{
    "attributes": [
        {
            "description": "The rest name of the object. example 'unicorn'",
            "name": "objectRESTName",
            "type": "string"
        },
        {
            "description": "The resource name of the object. example 'unicorns'",
            "name": "objectResourceName",
            "type": "string"
        },
        {
            "description": "true if root api",
            "name": "root",
            "type": "boolean"
        },
        {
            "description": "The entity name of the object. example 'Unicorn'.",
            "name": "entityName",
            "type": "string"
        }
    ],
    "model": {
        "description": "Represents the specification of an object.",
        "entity_name": "Specification",
        "extends": [
            "@parsable",
            "@specification"
        ],
        "resource_name": "specifications",
        "rest_name": "specification"
    }
}
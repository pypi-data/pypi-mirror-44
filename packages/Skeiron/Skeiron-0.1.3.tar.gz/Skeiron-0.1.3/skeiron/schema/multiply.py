def get_schema():
    return {
        "type": "object",
        "properties": {
            "name": {
                "description": "unique name for relay event",
                "type": "string"
            },
            "active": {
                "description": "entry ignored if set to False",
                "type": "boolean"
            },
            "type": {
                "description": "[forward, echo, collect, distribute, multiply]",
                "type": "string",
                "enum": ["multiply"]
            },
            "topics-sub": {
                "description": "forward messages published to these topics",
                "type": "array",
                "items": {
                    "type": "string"
                }
            },
            "topics-pub": {
                "description": "publish incoming messages to these topics",
                "type": "array",
                "items": {
                    "type": "string"
                }
            },
            "replace-message": {
                "description": "use this message instead of received message (optional)",
                "type": "string"
            }
        },
        "required": ["active", "name", "type", "topics-sub", "topics-pub"],
        "additionalProperties": False
    }
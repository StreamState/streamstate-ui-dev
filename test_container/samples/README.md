# Add sample data from Kafka topics here

Each json file needs to be put into the appropriate topic "subfolder".  Each json object needs to be on a single line.  Multiple json lines should simply be placed on new lines.

For example, 

```json
{"field1": "myexample1"}
{"field1": "myexample2"}
```

is valid, but

```json
{
    "field1": "myexample1"
}
```

is not.
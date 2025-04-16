# Schema.json to UI Mapping

## Schema to UI Flow

The `schema.json` file in each module defines the UI form that users interact with. This document explains how the schema flows through the system to create dynamic UI elements.

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│  schema.json    │───►│  /schema route  │───►│  Frontend UI    │
│  in module      │    │  processing     │    │  rendering      │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## How It Works

1. **Schema Definition**: Each module defines a `schema.json` file containing field definitions.

2. **API Endpoint**: The CDK framework automatically exposes these schemas through a `/schema` endpoint.

3. **UI Rendering**: The frontend receives the schema and dynamically renders form elements.

4. **Form Submission**: When submitted, form values are sent to your module's `/execute` endpoint, with field IDs mapping directly to request parameters.

## Example Schema Field

```json
{
  "id": "first_name",
  "type": "string",
  "label": "First Name",
  "validation": {
    "required": true
  }
}
```

↓ Transforms into ↓

```
┌───────────────────────────────┐
│                               │
│  First Name                   │
│  ┌───────────────────────┐    │
│  │ John                  │    │
│  └───────────────────────┘    │
│                               │
└───────────────────────────────┘
```

## Supported Field Types

- **string**: Text input fields
- **array**: Lists of items, often with nested object structures
- **object**: Grouping of related fields
- **boolean**: Checkbox or toggle inputs
- **number**: Numeric input fields

## Special UI Options

The `ui_options` property allows customization of field appearance:

```json
{
  "id": "message",
  "label": "Message",
  "type": "string",
  "ui_options": {
    "ui_widget": "CodeblockWidget",
    "ui_options": {
      "language": "json"
    }
  }
}
```

This creates a code editor with JSON syntax highlighting instead of a standard text input.

## Nested Fields and Arrays

Arrays with object items create dynamic, repeatable sections:

```json
{
  "id": "tasks",
  "label": "Tasks",
  "type": "array",
  "items": {
    "type": "object",
    "fields": [
      {
        "id": "name",
        "type": "string"
      },
      {
        "id": "description",
        "type": "string"
      }
    ]
  }
}
```

Renders as:

```
┌─────────────────────────────────────────────────┐
│ Tasks                                           │
│ ┌─────────────────────────────────────────────┐ │
│ │ Name         │ Description                  │ │
│ │ ┌───────────┐│ ┌──────────────────────────┐ │ │
│ │ │ Task 1    ││ │ Description for task 1   │ │ │
│ │ └───────────┘│ └──────────────────────────┘ │ │
│ └─────────────────────────────────────────────┘ │
│                   [+ Add Task]                   │
└─────────────────────────────────────────────────┘
```

## Data Flow

1. When building a workflow, the UI requests the schema from `/schema`
2. The schema is parsed to create form fields
3. Users fill in the form with their data
4. On submission, data is sent to `/execute` with the structure:
   ```
   {
     "first_name": "John",
     "last_name": "Doe",
     "message": "Hello, World!",
     "tasks": [
       {
         "name": "Task 1",
         "description": "Description for task 1"
       }
     ]
   }
   ```
5. Your module code receives this exact structure in `request.data` at the `/execute` route

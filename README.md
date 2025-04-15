# Example Workflows Module

This is an example module demonstrating the unified router system for Stacksync Workflows CDK.

## Features

- Unified router system with versioned endpoints
- Built-in health checks and module information
- Request validation using Pydantic models
- Standardized error handling and responses
- Production-ready with Gunicorn support

## Available Endpoints

### System Endpoints

- `GET /health` - Health check endpoint
- `GET /info` - Module information and documentation

### V1 Endpoints

- `POST /api/send_message/v1` - Send a message (basic)
- `POST /api/search/v1` - Perform a search (basic)

### V2 Endpoints

- `POST /api/send_message/v2` - Send a message (enhanced)
- `POST /api/search/v2` - Perform a search (enhanced)

## Setup

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate  # Windows
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy environment variables:

```bash
cp .env.example .env
```

4. Configure environment variables in `.env`

## Development

Run the development server:

```bash
python main.py
```

## Production

Run with Gunicorn:

```bash
gunicorn -c gunicorn.conf.py main:router.app
```

## Docker

Build and run with Docker:

```bash
docker build -t workflows-app-example .
docker run -p 8080:8080 workflows-app-example
```

For development with Docker:

```bash
docker build -f Dockerfile.dev -t workflows-app-example-dev .
docker run -p 8080:8080 -v $(pwd):/app workflows-app-example-dev
```

## Testing

Run tests:

```bash
pytest
```

## API Documentation

### Send Message (V1)

```json
POST /api/send_message/v1
{
    "message": "Hello!",
    "recipient": "user@example.com",
    "subject": "Greeting"
}
```

### Send Message (V2)

```json
POST /api/send_message/v2
{
    "message": "Hello!",
    "recipient": "user@example.com",
    "subject": "Greeting"
}
```

Response includes additional delivery status information.

### Search (V1)

```json
POST /api/search/v1
{
    "query": "example",
    "filters": {
        "type": "document"
    }
}
```

### Search (V2)

```json
POST /api/search/v2
{
    "query": "example",
    "filters": {
        "type": "document"
    }
}
```

Response includes relevance scores, metadata, and pagination.

## Design: Flexible Credentials System

### Overview

The new credentials system allows any field in a module's options to be marked as requiring credentials, moving away from a fixed "credentials" field to a more flexible approach.

### Schema Design

```typescript
// Example module schema
{
  "options": {
    "type": "object",
    "properties": {
      "openai": {
        "type": "object",
        "properties": {
          "api_key": {
            "type": "object",
            "enum": ["openai_prod", "openai_dev"],
            "credentials": true,  // Mark this field as requiring credentials
            "connection_type": "openai"  // Specify the type of credentials needed
          },
          "model": {
            "type": "string",
            "enum": ["gpt-4", "gpt-3.5-turbo"]
          }
        }
      },
      "postgres": {
        "type": "object",
        "properties": {
          "connection": {
            "type": "object",
            "credentials": true,  // Another credentials field
            "connection_type": "postgres"
          },
          "query": {
            "type": "string"
          }
        }
      }
    }
  }
}
```

### Data Flow

1. Frontend to Backend:

```typescript
// Example request body
{
  "options": {
    "openai": {
      "api_key": "{{connection:openai_prod}}",  // Reference to a credential
      "model": "gpt-4"
    },
    "postgres": {
      "connection": "{{connection:db_prod}}",
      "query": "SELECT * FROM users"
    }
  }
}
```

2. Backend Processing:

```python
# The execution engine processes each field marked with credentials=true
{
    "data": {
        "openai": {
            "api_key": "sk-actual-key-here",  # Resolved credential
            "model": "gpt-4"
        },
        "postgres": {
            "connection": {
                "host": "db.example.com",
                "password": "actual-password"  # Resolved credential
            },
            "query": "SELECT * FROM users"
        }
    }
}
```

### Implementation Requirements

1. Frontend:

- Schema validation to identify credential fields
- UI components to handle credential selection
- Connection reference syntax: {{connection:name}}
- Credential type validation

2. Backend:

- Credential resolution system
- Security measures for credential handling
- Validation of credential types
- Error handling for missing/invalid credentials

3. Execution Engine:

- Dynamic credential injection
- Secure credential storage
- Credential access logging
- Error handling for credential failures

### Security Considerations

1. Credential Storage:

- Encrypted at rest
- Secure transmission
- Access control per workspace
- Audit logging

2. Runtime Security:

- Memory protection
- Credential rotation
- Access scope limitation
- Temporary credential generation

### Migration Path

1. Phase 1: Dual Support

- Support both old and new credential formats
- Add new credential field markers
- Update validation logic

2. Phase 2: Schema Updates

- Convert existing modules to new format
- Update stored workflows
- Validate all conversions

3. Phase 3: Complete Migration

- Remove old credential handling
- Clean up legacy code
- Update documentation

### Example Usage

```typescript
// Module definition
{
  "module_id": "openai-chat",
  "options": {
    "api": {
      "credentials": true,
      "connection_type": "openai",
      "required": true
    },
    "messages": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "role": { "type": "string" },
          "content": { "type": "string" }
        }
      }
    }
  }
}

// Usage in workflow
{
  "options": {
    "api": "{{connection:openai_prod}}",
    "messages": [
      {
        "role": "user",
        "content": "Hello!"
      }
    ]
  }
}
```

### Error Handling

1. Validation Errors:

- Missing credentials
- Invalid credential types
- Permission issues

2. Runtime Errors:

- Credential resolution failures
- Connection timeouts
- Access denied scenarios

### Testing Requirements

1. Unit Tests:

- Credential field detection
- Reference syntax validation
- Type checking

2. Integration Tests:

- Credential resolution
- Security measures
- Error scenarios

3. End-to-End Tests:

- Complete workflow execution
- Multiple credential types
- Error recovery

### Performance Considerations

1. Caching:

- Credential resolution results
- Schema validation results
- Connection pooling

2. Optimization:

- Batch credential resolution
- Minimal credential copying
- Efficient memory usage

### Monitoring

1. Metrics:

- Credential resolution time
- Error rates
- Usage patterns

2. Alerts:

- Credential failures
- Security violations
- Performance issues

### Documentation Requirements

1. Developer Guide:

- Schema definition
- Credential field usage
- Security best practices

2. User Guide:

- Credential setup
- Connection management
- Troubleshooting

3. API Documentation:

- Endpoint specifications
- Request/response formats
- Error codes

### Future Enhancements

1. Planned Features:

- Dynamic credential types
- Credential chaining
- Advanced security options

2. Compatibility:

- Third-party integrations
- Custom credential types
- Legacy system support

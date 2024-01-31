# web-index

```mermaid
graph TD;

subgraph "User Input"
  input_file -->|List of URLs| main
end

subgraph "Main Application"
  main -->|Read URLs| Utils
  Utils -->|Read JSON| urls
  main -->|Choose Index Type| NonPositionalIndex or PositionalIndex
  NonPositionalIndex -->|Create Non-Pos Index| Utils
  PositionalIndex -->|Create Pos Index| Utils
  NonPositionalIndex -->|Run| Utils
  PositionalIndex -->|Run| Utils
end

subgraph "Index Creation"
  Utils -->|Read URL| AbstractIndex
  AbstractIndex -->|Download HTML| BeautifulSoup
  BeautifulSoup -->|Parse HTML| AbstractIndex
  AbstractIndex -->|Get Text| AbstractIndex
  AbstractIndex -->|Tokenize| AbstractIndex
  AbstractIndex -->|Update Index| NonPositionalIndex or PositionalIndex
end

subgraph "Output"
  NonPositionalIndex -->|Write Index| Utils
  NonPositionalIndex -->|Write Metadata| Utils
  PositionalIndex -->|Write Index| Utils
  PositionalIndex -->|Write Metadata| Utils
end

subgraph "Logging and Statistics"
  NonPositionalIndex -->|Print Logs| Logging
  NonPositionalIndex -->|Print Metadata| Logging
  PositionalIndex -->|Print Logs| Logging
  PositionalIndex -->|Print Metadata| Logging
end

```

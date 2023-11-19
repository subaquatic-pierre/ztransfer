# Ztransfer

## Overview

ztransfer is a file-sharing application that utilizes the Zero Chain blockchain to provide a secure and decentralized experience. This application focuses on an intuitive user interface, interacting with the backend through a custom Python library.

## Features

- **Zero Chain Integration**: Utilizes the Zero Chain blockchain for secure and decentralized file storage.
- **User-Friendly Interface**: Prioritizes an intuitive and user-friendly interface for a seamless file-sharing experience.

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Run application

1. Clone repo
2. Install Docker and Docker Compose
3. Change names of env files to hidden folders and remove 'example' eg. '.env.dev', '.env.prod' '.env.prod.db'

#### Development

```
docker-compose up -d --build
```

#### Production:

```
docker-compose -f docker-compose.prod.yaml up -d --build
```

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.
License

This project is licensed under the MIT License.

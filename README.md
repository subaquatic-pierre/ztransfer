# Ztransfer

0Chain transfer platform

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
docker-compose -f docker-compose.prod.yml up -d --build
```

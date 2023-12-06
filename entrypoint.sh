#!/bin/bash

echo "$ENV"

sleep 10

if [ "$ENV" == "development" ]; then
  alembic upgrade head
fi

python runserver.py
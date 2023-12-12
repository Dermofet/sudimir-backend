#!/bin/bash

echo "$ENV"

sleep 3

if [ "$ENV" == "development" ]; then
  alembic upgrade head
fi

python runserver.py
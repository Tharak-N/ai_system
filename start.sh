#!/bin/bash

poetry run fastapi dev app/main.py --host=0.0.0.0 &
poetry run phoenix serve &
wait 
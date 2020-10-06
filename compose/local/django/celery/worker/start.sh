#!/bin/bash

celery -A blogproject.taskapp worker -l INFO

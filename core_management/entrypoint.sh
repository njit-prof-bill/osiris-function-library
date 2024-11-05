#!/bin/sh
echo "Running tests..."
pytest core_management/tests

if [ $? -ne 0 ]; then
    echo "Tests failed. Exiting."
    exit 1
fi

echo "Tests passed. Starting server in the background..."
python main.py &

# Wait a few seconds to ensure the server is fully up and running
sleep 3

echo "Running client test request..."
python core_management/client/client.py

# Keep the server running in the foreground
wait

CURRENTLY RUNS SERVER AND TEST CASES (Using mock values)

WHILE IN /osiris-function-library:
dos2unix core_management/entrypoint.sh
docker build -t osiris-function-library -f core_management/Dockerfile .
docker run -it osiris-function-library
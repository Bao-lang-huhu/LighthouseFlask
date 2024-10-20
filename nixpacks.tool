[phases.setup]
commands = ["apt-get update", "apt-get install -y python3-pip python3-venv"]

[phases.build]
commands = ["cd python_service && python3 -m pip install -r requirements.txt"]

[phases.start]
commands = ["cd python_service && gunicorn -w 4 -b 0.0.0.0:$PORT app:app"]

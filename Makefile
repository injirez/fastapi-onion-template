pre-run:
	@ scripts/set_secret_key.sh
	@ python scripts/configure_docker_compose.py
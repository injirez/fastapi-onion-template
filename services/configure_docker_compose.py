import sys
from pathlib import Path

import yaml

# Changing python path for using modules
# ------------
script_path = Path(__file__).absolute
sys.path.insert(0, str(script_path))
base_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(base_dir / "backend" / "app"))
# -----------

from core.settings import settings


def update_ports() -> None:
    with open("./docker-compose.yml") as ymlfile:
        docker_config = yaml.safe_load(ymlfile)

    docker_config["services"]["backend"]["ports"] = [f"{settings.PORT_BACKEND}:{settings.PORT_BACKEND}"]
    # Uncomment if you use frontend
    docker_config["services"]["frontend"]["ports"] = [f"{settings.PORT_FRONTEND}:{settings.PORT_FRONTEND}"]

    with open("./docker-compose.yml", "w") as file:
        yaml.safe_dump(docker_config, file)


if __name__ == "__main__":
    update_ports()

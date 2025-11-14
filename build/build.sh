# shellcheck disable=SC2046
poetry add $(cat "../requirements.txt")

poetry build
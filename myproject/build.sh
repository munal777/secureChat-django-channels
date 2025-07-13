set -o errexit

# Set Django settings module
export DJANGO_SETTINGS_MODULE=myproject.settings

# install python dependencies
pip install -r requirements.txt

#!/bin/bash

# Check if Docker is installed
if (! command -v docker &> /dev/null) || (! command docker compose version &> /dev/null)
then
    echo "Docker and/or Docker Compose is not installed."
	echo "Please make sure both are installed before you proceed"
    read -p "Would you like to view the Docker installation guide? (y/n): " response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        echo "Opening Docker installation guide..."
        xdg-open "https://docs.docker.com/get-docker/" 2>/dev/null || \
        open "https://docs.docker.com/get-docker/" 2>/dev/null || \
        echo "Please visit https://docs.docker.com/get-docker/ in your browser."
    else
        echo "Docker installation guide skipped."
    fi
    exit 1  # End execution if Docker is not installed
else
    echo "Docker is already installed."
fi

# Check if the user is in a Python virtual environment or Conda environment
if [[ -z "$VIRTUAL_ENV" && -z "$CONDA_DEFAULT_ENV" ]]; then
    echo "It looks like you're not using a Python virtual environment or Conda."
    echo "Using a virtual environment is recommended to keep dependencies isolated."
    read -p "Would you like to learn more about setting up a Python virtual environment? (y/n): " response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        echo "Opening Python virtual environment guide..."
        xdg-open "https://docs.python.org/3/library/venv.html" 2>/dev/null || \
        open "https://docs.python.org/3/library/venv.html" 2>/dev/null || \
        echo "Please visit https://docs.python.org/3/library/venv.html in your browser."
    else
        echo "Python virtual environment guide skipped."
    fi
    exit 1  # End execution if not using a virtual environment or Conda
else
    echo "Python virtual environment or Conda environment detected."
fi

# Continue with the rest of the script
echo

pip install -r requirements.txt

echo

# Check for .env file and create one if it doesn't exist
if [ ! -f .env ]; then
	read -p "Would you like to create a new .env file for secret authentication? (y/n)" response
	if [[ "$response" =~ ^[Yy]$ ]]; then
		read -p "Enter your secret api key for oauth2 authentication: " -s secret_key
		read -p "Enter your database root password: " -s db_pass
		echo -e "API_SECRET_KEY=${secret_key}\nDB_PASSWORD=${db_pass}" > .env
	else
		echo ".env creation skipped"
		exit 1
	fi
else
	echo ".env file found"
fi

echo
echo "Environment checks passed :)"
echo

read -p "Would you like to build a database image with docker? (y/n)" response
if [[ "$response" =~ ^[Yy]$ ]]; then
	echo "Building Database Image"
	docker build --build-arg MYSQL_ROOT_PASSWORD=$(cat .env | grep DB_PASSWORD | cut -d '=' -f2) -t soundtrackd-db ./database
	read -p "Would you like to deploy the database image as a container? (y/n)" response
	if [[ "$response" =~ ^[Yy]$ ]]; then
		echo "Deploying db container"
		docker compose up -d db
	fi
else
	echo "database initialization skipped"
fi

echo
echo "Your development environment has been set up. Run 'python -m app' to start the api."

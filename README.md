# IoT Server
This repository contains all files for a server to recive and store information from an edge in a iot pipeline. 
The server is planned to connect to a SQLite database to store the data.

The server works deploying a Docker container. And launching the server in it, using the port `8080`.

## Installation Guide
To deploy the server, exectue the following command in a bash console, in the directory containing this repository:

````bash
bash deploy_container.sh
````

If the machine does not have Docker, you can install it executing the following command in a bash console, in the directory containing this repository:

````bash
sudo bash install_docker.sh
````

To get the repository into the machine, simply execute the following command in a bash console:

````bash
git clone https://github.com/NIU1638962/iot-server
````

Alternatively, create a `server.sh` file, paste the following code:

````bash
#!/bin/bash

echo "Preparing environment."
if [ -d "iot-server" ];
then
    echo "Directory already exists. Removing."
    rm -d -f -r iot-server
    echo "Directory removed."
fi

if command -v git > /dev/null 2>&1; then
    echo "Git is already installed."
else
    echo "Git is not installed. Installing git."
    sudo apt-get update -y
    sudo apt-get install -y git
    echo "Git has been installed."
fi

echo "Cloning repository with the server infrastructure."
git clone https://github.com/NIU1638962/iot-server
echo "Repository cloned."

echo "Setting working directory."
cd iot-server
echo "Working directory set."

echo "Execute install docker."
bash install_docker.sh
echo "Environment prepared."

echo "Execute deploy."
bash deploy_container.sh
````

and execute the following command in a bash console:

````bash
sudo bash server.sh
````

and all the steps needed will be performed automatically and the server will be deployed.
# SwissHacks25-Priceless

This project is managed with Docker Compose. Below are the details of the services, their exposed ports, and how to run them.

## Available Commands

### Development Mode

docker compose -f compose.dev.yml up --build 

docker compose -f compose.dev.yml down --volumes


### Production Mode

docker compose -f compose.prod.yml up --build 

docker compose -f compose.prod.yml down --volumes


## Services Overview

### Frontend - Vue 3
- Repository: [https://github.com/HackathonCliTemplate/frontend-vue3-template.git](https://github.com/HackathonCliTemplate/frontend-vue3-template.git)
- Exposed Ports: `5173:5173`, `8080:8080`
- Depends on: `backend`

### Backend - FlaskAPI
- Repository: [https://github.com/HackathonCliTemplate/api-flask-static-template.git](https://github.com/HackathonCliTemplate/api-flask-static-template.git)
- Exposed Ports: `5000:5000`, `5000:5000`
- Volumes: `./backend:/app`

### Database - MongoDB
- Image: `mongo:latest`
- Exposed Ports: `27017:27017`, `27017:27017`


## Python Dependencies
 - It needs to be done with pyenv.
    - Install pyenv with the following command:
        ```bash
        curl https://pyenv.run | bash
        ```
    - Add the following lines to your shell configuration file (e.g., `~/.bashrc`, `~/.zshrc`):
        ```
            export PATH="$HOME/.pyenv/bin:$PATH"
            eval "$(pyenv init --path)"
            eval "$(pyenv init -)"
            eval "$(pyenv virtualenv-init -)"
        ```
    - Restart your shell or run `source ~/.bashrc` or `source ~/.zshrc`.
    - Install the required Python version:
        ```
        pyenv install 3.13.2
        ```
    - Create a virtual environment:
        ```
        ${HOME}/.pyenv/versions/3.13.2/bin/python -m venv venv

  - Activate the virtual environment:
        ```
        source venv/bin/activate
        ```
  - When installing new dependencies, include the version that is used in the required python requirements.txt file.

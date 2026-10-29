# linux101

## Setup

Clone the repository:

```bash
git clone <repository-url>
cd linux101
```

## Start the Challenge

Navigate to the challenge directory and start the Docker container:

```bash
cd challenge
docker compose up
```

## Connect to the Container

Open a new terminal and run the following command to get an interactive shell:

```bash
socat file:`tty`,raw,echo=0 tcp:127.0.0.1:4444
```

You're ready to solve the challenge.

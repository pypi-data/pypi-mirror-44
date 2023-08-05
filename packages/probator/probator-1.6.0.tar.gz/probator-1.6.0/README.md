# Probator

A security and compliance tool for validating your infrastructure. For full documentation please head over to https://probator.gitlab.io/


## Docker

Using the provided `Dockerfile` it is trivial to build a container that contains everyting
necessary to run a the backend, scheduler and worker processes.

### Build Arguments

The Dockerfile currently supports 3 arguments as `--build-arg` variables

| Name | Description |
|------|-------------|
| pip_flags | Used to pass any extra configuration arguments to the pip install command. An example of this could be to pass in the `--extra-index-url` argument for loading extra packages from a private PyPi repository |
| extra_packages | Any extra python packages you would like to install, such as custom plugins |
| timezone | The timezone to set in the container, used for the schedulers. Defaults to `UTC` |


### Limitations

The container does not come with a database, that will need to be provided externally. You
will also need to map in a volume containing the configuration files

### Examples

##### Build with custom plugin from private repository

This example uses the `pip_flags` and `extra_packages` to install a custom plugin `probator-auth-openid`

```
docker build . -t probator:latest --build-arg pip_flags="--extra-index-url https://pypi.company.tld/simple/" --build-arg extra_packages="probator-auth-openid"
```

##### Example execution

To run any part of the system you will need to pass in the configuration folder with the required files (`config.json`, `logging.json` and `ssl/private.key`) present to `/usr/local/etc/probator` inside the container.

The example below will execute the scheduler

```
docker run --rm -v probator-config:/usr/local/etc/probator probator:latest probator scheduler
```

The next example shows how to run the API server with a port mapping for a production API server

```
docker run --rm -p 5000:5000 -v probator-config:/usr/local/etc/probator probator:latest gunicorn -w 6 -b 0.0.0.0:5000 -k gthread -t 60 "probator.wsgi:run()"
```

# Credits

Based on the work by Riot Games' [Cloud Inquisitor](https://github.com/RiotGames/cloud-inquisitor)

# Nanowire JupyterHub Authenticator #

Simple authenticator for [Nanowire](https://www.spotlightdata.co.uk/) based on the dummyauthenticator.

## Installation ##

```
pip install jupyterhub-nanowireauthenticator
```

Should install it. It has no additional dependencies beyond JupyterHub and requests.

You can then use this as your authenticator by adding the following line to
your `jupyterhub_config.py`:

```
c.JupyterHub.authenticator_class = 'nanowireauthenticator.NanowireAuthenticator'
```


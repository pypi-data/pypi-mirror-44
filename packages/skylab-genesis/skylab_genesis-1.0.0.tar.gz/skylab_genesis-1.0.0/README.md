# Skylab Genesis Python Client

[![CircleCI](https://circleci.com/gh/skylab-tech/genesis_client_python.svg?style=svg)](https://circleci.com/gh/skylab-tech/genesis_client_python)
[![Maintainability](https://api.codeclimate.com/v1/badges/6e3316f60d72a9ca9276/maintainability)](https://codeclimate.com/github/skylab-tech/genesis_client_python/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/6e3316f60d72a9ca9276/test_coverage)](https://codeclimate.com/github/skylab-tech/genesis_client_python/test_coverage)

SkylabTech Genesis Python client.

[genesis.skylabtech.ai](https://genesis.skylabtech.ai)

## Requirements

- [Python requests library](http://docs.python-requests.org/en/master/user/install/#install)

## Installation

```bash
$ pip install skylab_genesis
```

## Usage

For all examples, assume:

```python
import skylab_genesis

api = skylab_genesis.api(api_key='YOUR-API-KEY')
```

### Error Handling

By default, the API calls return a response object no matter the type of response.

### Endpoints

#### List all jobs

```python
api.list_jobs()
```

#### Create job

```python
payload = {
  'profile_id': 1
}

api.create_job(payload=payload)
```

For all payload options, consult the [API documentation](http://docs.genesis.skylabtech.ai/#operation/createJob).

#### Get job

```python
api.get_job(job_id=1)
```

#### Update job

```python
payload = {
  'profile_id': 2
}

api.create_job(job_id=1, payload=payload)
```

For all payload options, consult the [API documentation](http://docs.genesis.skylabtech.ai/#operation/updateJobById).

#### Delete job

```python
api.delete_job(job_id=1)
```

#### Process job

```python
api.process_job(job_id=1)
```

#### Cancel job

```python
api.cancel_job(job_id=1)
```

#### List all profiles

```python
api.list_profiles()
```

#### Create profile

```python
payload = {
  'profile_id': 1
}

api.create_profile(payload=payload)
```

For all payload options, consult the [API documentation](http://docs.genesis.skylabtech.ai/#operation/createProfile).

#### Get profile

```python
api.get_profile(profile_id=1)
```

#### Update profile

```python
payload = {
  'profile_id': 2
}

api.create_profile(profile_id=1, payload=payload)
```

For all payload options, consult the [API documentation](http://docs.genesis.skylabtech.ai/#operation/updateProfileById).

#### Delete profile

```python
api.delete_profile(profile_id=1)
```

#### List all photos

```python
api.list_photos()
```

#### Create photo

```python
payload = {
  'photo_id': 1
}

api.create_photo(payload=payload)
```

For all payload options, consult the [API documentation](http://docs.genesis.skylabtech.ai/#operation/createPhoto).

#### Get photo

```python
api.get_photo(photo_id=1)
```

#### Update photo

```python
payload = {
  'photo_id': 2
}

api.create_photo(photo_id=1, payload=payload)
```

For all payload options, consult the [API documentation](http://docs.genesis.skylabtech.ai/#operation/updatePhotoById).

#### Delete photo

```python
api.delete_photo(photo_id=1)
```

### Expected Responses

#### Success

```bash
    >>> response.status_code
    200

    >>> response.json().get('success')
    True

    >>> response.json().get('status')
    u'OK'

    >>> response.json().get('profile_id')
    u'numeric-profile-id'
```

#### Error

* Malformed request

```bash
    >>> response.status_code
    400
```

* Bad API key

```bash
    >>> response.status_code
    403
```

## Testing

Use [tox](https://tox.readthedocs.io/en/latest/) to run the tests:

```bash
tox
```

### Testing Multiple Python Versions

This assumes you have [tox](https://tox.readthedocs.io/en/latest/) installed and used
[pyenv](https://github.com/yyuu/pyenv) to install multiple versions of python.

Once all the supported python versions are installed simply run:

```bash
tox
```

This will run the tests against all the versions specified in `tox.ini`.

## Troubleshooting

### General Troubleshooting

- Enable debug mode
- Make sure you're using the latest Python client
- Capture the response data and check your logs &mdash; often this will have the exact error

### Enable Debug Mode

Debug mode prints out the underlying request information as well as the data
payload that gets sent to Genesis. You will most likely find this information
in your logs. To enable it, simply put `debug=True` as a parameter when instantiating
the API object. Use the debug mode to compare the data payload getting
sent to [Genesis' API docs](http://docs.genesis.skylabtech.ai/#).

```python
import skylab_genesis

api = skylab_genesis.api(api_key='YOUR-API-KEY', debug=True)
```
### Response Ranges

Genesis' API typically sends responses back in these ranges:

-   2xx – Successful Request
-   4xx – Failed Request (Client error)
-   5xx – Failed Request (Server error)

If you're receiving an error in the 400 response range follow these steps:

-   Double check the data and ID's getting passed to Genesis
-   Ensure your API key is correct
-   Log and check the body of the response

## Distribution

To package:

```bash
  python setup.py sdist bdist_wheel upload
```
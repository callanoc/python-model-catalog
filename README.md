# Model Catalog API

This Python RPC API allows users to create, update, and access information about
models.

The RPC framework used is gRPC: https://grpc.io/

Provided services:
* Sign up
* Sign in
* Create folder
* Create model
* Grant user access to a folder
* List models
* Upload a model version
* Download a model version

## Installation

#### Python 3.10 is required

Create virtual env:
``` shell
python3.10 -m venv model_catalog_venv 
```

Activate virtual env:
``` shell
source model_catalog_venv/bin/activate 
```

Install requirements:
``` shell
pip install -r requirements.txt
```

## How to run the server
``` shell
python -m api.src.server
```

## How to test it

#### Database unit tests

``` shell
PYTHONPATH='.' pytest database/tests/test_in_memory_store.py
```

#### Integration test

#### / ! \  Don't forget to run the server before running integration tests within the virtual env / ! \ 

With the interactive client:
``` shell
python -m api.src.interactive_client
```

#### Special cases:
Create model without folder permission:
``` shell
python -m api.src.integration_tests.create_model_without_folder_permission_test
```

Create model after grant folder permission: 
``` shell
python -m api.src.integration_tests.create_model_after_grant_permissions_test
```

List only authorized models:
``` shell
python -m api.src.integration_tests.list_only_authorized_models
```

Upload and download:
``` shell
python -m api.src.integration_tests.upload_download
```

## Authentication

### SSL authentication
Server/Client communication is secured with SSL authentication (key/certificate)
#### How to generate new SSL key/certificate
``` shell
 openssl req -newkey rsa:4096 -nodes -keyout server.key -sha256 -x509 -days 3650 -out server.crt -subj '/CN=localhost'
```

### SSO
Users need to sign up/sign in through an authentication system which hashes passwords and generates JWT tokens.

#### How to generate new JWT keys
``` shell
 ssh-keygen -t rsa -b 4096 -m PEM -f jwtRS256.key
 openssl rsa -in jwtRS256.key -pubout -outform PEM -out jwtRS256.key.pub
```

## Short-cuts and improvements

Short-cuts taken and some improvements needed if I have had more time

### Tests

Only the in-memory database has unit tests, all services should be unit tested as well.

Fixtures could be added

Services are tested through integration tests.

More integration tests should be added

Integration tests would be integrated in the pytest test suite

### Upload

Upload and download features have been currently tested with a .txt file.

Should be tested with more file types (eg. tar.gz or .onnx files)

Upload a version to model is currently divided into different rpc calls.
It should be simplified and refactored it into a unique simpler rpc call.

### Error and security failures management

Error and possible security failures/threats management should be improved

# python-model-catalog

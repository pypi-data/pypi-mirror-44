## How to use
This package provided function *install_magento* for install magento using [magento-apache](https://gitlab.com/general-oil/infrastructure/tree/master/Environment/Magento/DemoPortalApache) running on docker engine.  
The function has required params:
+ env_params: dict values, must contains all below keys:
  + MAGENTO_VERSION: 'x.x.x'  
  e.g: 2.2.5
  + SAMPLE_DATA: sample data profile name (empty value for no sample data)   
  valid values : 'small', 'medium', 'medium_msite', 'large', 'extra_large'
  + PHP_VERSION: 'x.x.x'  
  e.g: 7.1.20
+ server_params: dict values, must contains all below keys:
  + 'HOST': remove server ip address
  + 'USER': remote server username
  + 'PASSWORD': remote server password (if 'KEY_PATH' has value, this key is optional)
  + 'KEY_PATH': local private key file path to conect to remote server
+ git_credential: git credential url that provided permission to access to [infrastructure](https://gitlab.com/general-oil/infrastructure) repo 

1. Install package *magestore-aup*
2. Import function to other file
```python
from magestore_aup import install_magento
```

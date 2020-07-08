import os
from amundsen_application import create_app
from OpenSSL import SSL

context = SSL.Context(SSL.SSLv3_METHOD)
context.use_privatekey_file('ssl_cert/gds-amundsen-test.int.electrolux.com.key')
context.use_certificate_file('ssl_cert/gds-amundsen-test.int.electrolux.com.crt')

application = create_app(
    config_module_class=os.getenv('FRONTEND_SVC_CONFIG_MODULE_CLASS') or
    'amundsen_application.config.LocalConfig')

if __name__ == '__main__':
    application.run(host='0.0.0.0', ssl_context=context)

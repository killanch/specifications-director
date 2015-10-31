#!/bin/bash

CURRENT_PATH=`pwd`
rm -rf libs
mkdir libs

cd ../../bambou/
python setup.py sdist
cd $CURRENT_PATH
cp ../../bambou/dist/bambou*.tar.gz libs

cd ../../garuda/
python setup.py sdist
cd $CURRENT_PATH
cp ../../garuda/dist/garuda*.tar.gz libs

cd ../../monolithe/
python setup.py sdist
cd $CURRENT_PATH
cp ../../monolithe/dist/monolithe*.tar.gz libs

cd ..
../monolithe/commands/monogen-sdk -f specs -c specs/monoconf/config.ini
cd codegen
python setup.py sdist
cd $CURRENT_PATH
cp ../codegen/dist/specdk*.tar.gz libs


cat << EOF > libs/nuage.pem
-----BEGIN CERTIFICATE-----
MIIDsDCCApigAwIBAgIBATANBgkqhkiG9w0BAQsFADBAMR4wHAYDVQQKExVVUy5B
TENBVEVMLUxVQ0VOVC5DT00xHjAcBgNVBAMTFUNlcnRpZmljYXRlIEF1dGhvcml0
eTAeFw0xMzExMjAwNDUwMDdaFw0zMzExMjAwNDUwMDdaMEAxHjAcBgNVBAoTFVVT
LkFMQ0FURUwtTFVDRU5ULkNPTTEeMBwGA1UEAxMVQ2VydGlmaWNhdGUgQXV0aG9y
aXR5MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA0XPgKxpFs6TaR6gq
nttzBpD1iW40HySAqrsGNFI8QVXr0dnrPWjbWPAczAz1QH/Bo8vb0vjzK3H+lt78
/U8BxCo39iOf1XGMtpz3Fxyow8deGzxkFi2gPanqOBXdIQa8yc6ejjKOAvq2cH8k
s/NBGJ1RS0QUU59ugp8vpt6WHgBAuSrfWrJ4et93xrfGqirHKSk2OdJ+3wSvZgza
TqDWZNnb5DyPIm+Or4t6DjTj/2CFgb98zNRF6UcN8qmRBSDikaEg6lXz+clQyGLd
ZFnF6DBH4nreBAthF1m1G5WhW1s3dSjCiM/DlfAtw/C1o40KMr5Gh0tMZKuarIDr
/E4khQIDAQABo4G0MIGxMB8GA1UdIwQYMBaAFDLlGdXnmdAVXvhi+8VTy1/KuyXA
MA8GA1UdEwEB/wQFMAMBAf8wDgYDVR0PAQH/BAQDAgHGMB0GA1UdDgQWBBQy5RnV
55nQFV74YvvFU8tfyrslwDBOBggrBgEFBQcBAQRCMEAwPgYIKwYBBQUHMAGGMmh0
dHA6Ly9udWFnZWxkYXAxLnVzLmFsY2F0ZWwtbHVjZW50LmNvbTo4MC9jYS9vY3Nw
MA0GCSqGSIb3DQEBCwUAA4IBAQAubBNAhr7TxA1MxBzw4TcqYR16i7x1kWOQs8x1
CaIFtELTx5CX0w0m8r2jDJsZnCkKEwBKcuGyxDExGhBejFDbPYFhQD5U/erem3//
9fqFP+ehykEQP3kifVVS4d+48GV0nji3677xo5yCnveNe2I8ThT0JGjDQmO+utB/
nBls2L3i6gcRzqF/Cbhiw9D+LEkeJWENjKxaki/vOkiNwv614eE9VPKjeXj8K0L8
t1oXTFtsbwMMdV5ljOSg4iPNpNe5UlCAHUzVtM7q93NRvge0FdyeXh1iWPrv8gTk
T1xqYtqyyAaJbuiScKn02Ui1f0uQ9PaCdgGOQr/pW0HEGE1e
-----END CERTIFICATE-----
EOF

"""Создание сертификата HTTPS."""

import logging
import os
import shutil
from typing import Callable

DOMAIN_EXT: str = """
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
subjectAltName = @alt_names
[alt_names]
DNS.1 = {domain}
"""


def create(domain: str) -> Callable[[], None]:
    """Создать сертификат HTTPS.

    :param domain: название домена, для которого будет создан сертификат
    :return: задача
    """

    def _create() -> None:
        logging.info("Создаем корневой сертификат сервера в папке ~/certs")
        certs_dir: str = os.path.expanduser("~/certs")
        if os.path.exists(certs_dir):
            shutil.rmtree(certs_dir)
        os.makedirs(certs_dir)
        os.chdir(certs_dir)
        os.system("openssl genrsa -des3 -out myCA.key 2048")
        os.system(
            "openssl req -x509 -new -nodes -key myCA.key "
            "-sha256 -days 1825 -out myCA.pem",
        )
        logging.info("Корневой сертификат создан")
        logging.info(f"Создаем сертификат для домена {domain}")
        os.system(f"openssl genrsa -out {domain}.key 2048")
        os.system(f"openssl req -new -key {domain}.key -out {domain}.csr")
        with open(f"{domain}.ext", "w") as f:
            f.write(DOMAIN_EXT.format(domain=domain))
        os.system(
            f"openssl x509 -req -in {domain}.csr -CA myCA.pem -CAkey myCA.key "
            f"-CAcreateserial -out {domain}.crt -days 825 -sha256 "
            f"-extfile {domain}.ext",
        )

    return _create

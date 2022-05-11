#include <openssl/bio.h>
#include <openssl/rsa.h>
#include <openssl/pem.h>
#include <openssl/err.h>

#include <cstring>
#include <iostream>
#include <iomanip>
#include <fstream>

int main() {
    char* publicKey = "-----BEGIN PUBLIC KEY-----\n"
                        "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAror7nlgLYn+s/AI3z8BH\n"
                        "5NSrVC0semYy5L+U8UcaTriDxOUwRPkGhrqiUfJbnlpZwRrc5GgWANNuBMzFIxuQ\n"
                        "gD9WY0zGCCnkqXj6fY39+fkTx0Gn/bfkFXG+O+K8EWbbTzsBmtb2LNDvGP5aGSI2\n"
                        "OwG3LhukFhBOrcOMBjBYPJ8K4tBWf/uZGulJmAy3QXJudlu90oYrQmXeEpif3wrc\n"
                        "rtWkGcKJC96rTS1AkONBXrAiL0Qcf8GfRlUuoI5XGtw+Y+z9CTcsCzdgXvl2E+Eb\n"
                        "CqNXOBWR8MY9aleIo0TEmdtAfCoTLIyZShZWUkxbbbnNfaK8z6+vMPN5ei1vU3PQ\n"
                        "CwIDAQAB\n"
                        "-----END PUBLIC KEY-----\n";
    RSA* rsaPublicKey = 0;
    BIO* bo = BIO_new(BIO_s_mem());
    BIO_write(bo, publicKey, strlen(publicKey));
    PEM_read_bio_RSA_PUBKEY(bo, &rsaPublicKey, 0, 0);

    char* message = "HI\n\n234rdxf\n32,BRUH...";
    int messageLen = strlen(message);
    int nLen = RSA_size(rsaPublicKey);

    char* pEncode = (char*) malloc(nLen + 1);
    int rc = RSA_public_encrypt(
        messageLen,
        (unsigned char*) message,
        (unsigned char*) pEncode,
        rsaPublicKey,
        RSA_PKCS1_PADDING
    );
    if (rc < 0) {
        char buf[128];
        std::cerr << "RSA_public_encrypt: " << ERR_error_string(ERR_get_error(), buf) << std::endl;
    }

    std::ofstream fs("enc.bin", std::ios::out | std::ios::binary);
    fs << pEncode;
    fs.close();

    BIO_free(bo);
    RSA_free(rsaPublicKey);
}

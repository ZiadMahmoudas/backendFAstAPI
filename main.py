from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import datetime

from database import engine, Base
from routers import heroes

# Security
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa


app = FastAPI(title="Heroes API (Async)", version="6.0")
app.include_router(heroes.router)

origins = [
    "http://localhost:4200",
    "https://localhost:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def on_startup():
    await init_models()


def generate_ssl_cert():
    cert_dir = "ssl"
    os.makedirs(cert_dir, exist_ok=True)

    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    subject = issuer = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, u"localhost")])

    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.utcnow())
        .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))
        .sign(key, hashes.SHA256())
    )

    keyfile = os.path.join(cert_dir, "server.key")
    certfile = os.path.join(cert_dir, "server.crt")

    with open(keyfile, "wb") as f:
        f.write(
            key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )

    with open(certfile, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))

    return keyfile, certfile


if __name__ == "__main__":
    keyfile, certfile = generate_ssl_cert()
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        ssl_keyfile=keyfile,
        ssl_certfile=certfile,
        reload=True,
    )

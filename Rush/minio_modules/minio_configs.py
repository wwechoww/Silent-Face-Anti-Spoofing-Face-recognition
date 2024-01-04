class MinioConfig:
    def __init__(self, endpoint, access_key, secret_key, bucket):
        self.endpoint = endpoint
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket = bucket

# 具体的 MinIO 配置
minio_config = MinioConfig(
    endpoint="Your endpoint",
    access_key="Your access_key",
    secret_key="Your secret_key",
    bucket="Your bucket"
)
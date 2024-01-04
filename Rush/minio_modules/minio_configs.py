class MinioConfig:
    def __init__(self, endpoint, access_key, secret_key, bucket):
        self.endpoint = endpoint
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket = bucket

# 具体的 MinIO 配置
minio_config = MinioConfig(
    endpoint="42.192.42.17:11985",
    access_key="1198006606",
    secret_key="Yby@17625207472",
    bucket="ruoyi"
)
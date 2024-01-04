class AlgorithmCommandVo:
    def __init__(self, cameraUrl, cameraName, uploadUrl, enable):
        self.cameraUrl = cameraUrl
        self.cameraName = cameraName
        self.uploadUrl = uploadUrl
        self.enable = enable

    def __str__(self):
        return f"AlgRush(id={self.cameraUrl}, " \
               f"cameraUrl={self.cameraName}, " \
               f"cameraName={self.uploadUrl}, " \
               f"userName={self.enable})"
class AlgRush:
    def __init__(self, cameraUrl, cameraName, userName, checkTime, illegal, message, imgUrl):
        self.cameraUrl = cameraUrl
        self.cameraName = cameraName
        self.userName = userName
        self.checkTime = checkTime
        self.illegal = illegal
        self.message = message
        self.imgUrl = imgUrl

    def __str__(self):
        return f"AlgRush(cameraUrl={self.cameraUrl}, cameraName={self.cameraName}, userName={self.userName}, checkTime={self.checkTime}, illegal={self.illegal}, message={self.message}, imgUrl={self.imgUrl})"

    def to_dict(self):
        return {
            "cameraUrl": self.cameraUrl,
            "cameraName": self.cameraName,
            "userName": self.userName,
            "checkTime": self.checkTime,
            "illegal": self.illegal,
            "message": self.message,
            "imgUrl": self.imgUrl
        }
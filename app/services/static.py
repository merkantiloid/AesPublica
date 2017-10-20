class Static:
    SPACES = {'h':'Hi-Sec', 'l':'Low-Sec', 'z':'Zero/WH'}
    DEFAULT_SPACE = 'z'

    @staticmethod
    def to_json():
        return {
            "spaces": Static.SPACES,
        }
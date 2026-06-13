from asset import Asset
class Bond(Asset):
    def __init__(self, id : str, market_value : float, book_value : float, couponRate : float, faceValue : float, maturityYear : int ):
        super().__init__(id, market_value,book_value)
        self.couponRate = couponRate
        self.faceValue = faceValue
        self.maturityYear = maturityYear



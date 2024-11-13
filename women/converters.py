class FourDigitYearConverter:
    regex = r'\d{4}'

    # методы to_python и to_url в данном случае являются опциональными
    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return str(value)
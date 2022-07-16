class Padding:
    @staticmethod
    def padd_message_byte(data_in, length):
        while len(data_in) % length != 0:
            data_in = data_in + b' '
        return data_in

    @staticmethod
    def padd_message(data_in):
        while len(data_in) % 16 != 0:
            data_in = data_in + " "
        return data_in
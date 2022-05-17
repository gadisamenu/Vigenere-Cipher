from multiprocessing import Pool


class Tirthmius(object):
    enc_space = 95
    min_char = 32

    def __init__(self) -> None:
        self.key = ""
        self.block_size = len(self.key)

    def set_block_size(self, key):
        self.block_size = len(key)

    def _add_padding(self, text: str) -> str:
        padding = self.block_size - (len(text) % self.block_size)
        if padding == self.block_size:
            return text
        text += '\0'*padding
        return text

    def _remove_padding(self, text: str) -> str:
        count = text.count('\0')
        return text[:-count]

    def encrypt(self, plain_text: str) -> str:
        plain_text = self._add_padding(plain_text)
        input = []
        i = 0
        for _ in range(0, len(plain_text), self.block_size):
            input.append(plain_text[i: i+self.block_size])
            i += self.block_size

        if len(input) > 20:
            p= Pool(20)
        else: p = Pool(len(input))
        output = p.map(self._encrypt_block, input)
        p.close()
        return ''.join(output)

    def decrypt(self, cipher_text: str) -> str:
        cipher_text = self._add_padding(cipher_text)
        input = []
        i = 0
        for _ in range(0, len(cipher_text), self.block_size):
            input.append(cipher_text[i: i+self.block_size])
            i += self.block_size

        if len(input) > 20:
            p= Pool(20)
        else: p = Pool(len(input))
        output = p.map(self._decrypt_block, input)
        p.close()
        return ''.join(output)

    def _encrypt_block(self, block: str):
        cipher_block = [None for i in range(self.block_size)]
        for i in range(self.block_size):
            if block[i] == '\0':
                cipher_block[i] = '\0'
                continue
            elif block[i] == '\n':
                cipher_block[i] = '\n'
                continue
            temp = ord(block[i]) + ord(self.key[i]) - 2 * Tirthmius.min_char
            cipher_block[i] = chr((temp % Tirthmius.enc_space) + Tirthmius.min_char)
        return ''.join(cipher_block)

    def _decrypt_block(self, block: str):
        plain_block = [None for i in range(self.block_size)]
        for i in range(self.block_size):
            if block[i] == '\0':
                plain_block[i] = '\0'
                continue
            elif block[i] == '\n':
                plain_block[i] = '\n'
                continue
            temp = ord(block[i]) - ord(self.key[i])
            plain_block[i] = chr((temp % Tirthmius.enc_space) + Tirthmius.min_char)
        return ''.join(plain_block)


if __name__ == "__main__":
    t = Tirthmius("DKDKDKDK")
    enc = t.encrypt("How I Met Your Mother")
    print(enc)
    print(t.decrypt(enc))
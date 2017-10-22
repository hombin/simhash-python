#!/usr/bin/python
# coding=utf-8
# Implementation of Charikar simhashes in Python
# Google Simhash算法的python实现
# See: http://dsrg.mff.cuni.cz/~holub/sw/shash/#a1


class Simhash(object):
    def __init__(self, tokens='', hashbits=128):
        self.hashbits = hashbits
        self.hash = self.simhash(tokens)

    # toString函数
    def __str__(self):
        return str(self.hash)

    def __long__(self):
        return long(self.hash)

    def __float__(self):
        return float(self.hash)

    def simhash(self, tokens):
        # Returns a Charikar simhash with appropriate bitlength
        v = [0] * self.hashbits
        for t in [self._string_hash(x) for x in tokens]:
            # t为token的普通hash值
            print(t)
            for i in range(self.hashbits):
                bitmask = 1 << i
                print(t, bitmask, t & bitmask)
                if t & bitmask:
                    v[i] += 1
                    # 查看当前bit位是否为1，是的话则将该位加1
                else:
                    v[i] -= 1
                    # 否则的话，该位减1
        fingerprint = 0
        for i in range(self.hashbits):
            if v[i] >= 0:
                fingerprint += 1 << i

        return fingerprint
        # 整个文档的fingerprint为最终各个位大于等于0的位的和

    def _string_hash(self, source):
        # A variable-length version of Python's builtin hash
        # 针对source生成hash值
        if source == "":
            return 0
        else:
            x = ord(source[0]) << 7
            m = 1000003
            mask = 2 ** self.hashbits - 1
            for c in source:
                x = ((x*m) ^ ord(c)) & mask
            x ^= len(source)
            if x == -1:
                x = -2
            return x

    # 求 海明距离
    def hamming_distance(self, other_hash):
        x = (self.hash ^ other_hash.hash) & ((1 << self.hashbits) - 1)
        tot = 0
        while x:
            tot += 1
            x &= x-1
            return tot

    # 求 相似度
    def similarity(self, other_hash):
        a = float(self.hash)
        b = float(other_hash)
        if a > b:
            return b/a
        return a/b

if __name__ == '__main__':
    s1 = 'This is a test string for testing'
    hash1 = Simhash("".join(s1.split()))
    # print ("%s/t0x%x" % (s, hash1))
    s2 = 'This is a test string for testing also!'
    hash2 = Simhash("".join(s2.split()))
    # print ("%s/t[simhash = 0x%x]" % (s, hash2))
    s3 = 'Hello world, hello Python'
    hash3 = Simhash("".join(s3.split()))
    # test

    print(hash1.similarity(hash2), "percent similar")
    print(hash1.similarity(hash3), "percent similar")
    print(hash1.hamming_distance(hash2), "bits differ out of", hash1.hashbits)
    print(hash1.hamming_distance(hash3), "bits differ out of", hash1.hashbits)

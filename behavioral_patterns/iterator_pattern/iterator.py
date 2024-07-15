import itertools


class Prime:
    def __init__(self, initial, final=0) -> None:
        self.current = initial
        self.final = final

    def __iter__(self):
        return self

    def __next__(self):
        return self._compute()

    def _compute(self):
        while True:
            is_prime = True
            for x in range(2, int(pow(self.current, 0.5) + 1)):
                if self.current % x == 0:
                    is_prime = False
                    break

            num = self.current
            self.current += 1

            if is_prime:
                return num

            if self.final > 0 and self.current > self.final:
                raise StopIteration


if __name__ == "__main__":
    p = Prime(2, 10)
    for num in p:
        print(num)
        """
        2
        3
        5
        7
        """

    print(list(Prime(2, 50)))
    # [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

    p = Prime(2)  # 무한 이터레이터
    print(list(itertools.islice(Prime(2), 100)))  # 처음 100개의 소수 출력
    """
    [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
        53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109,
        113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179,
        181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241,
        251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313,
        317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389,
        397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461,
        463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541
    ]
    """

    # 단위 위치에서 1로 끝나는 처음 10개의 소수들
    print(list(itertools.islice(itertools.filterfalse(lambda x: x % 10 != 1, Prime(2)), 10)))
    # [11, 31, 41, 61, 71, 101, 131, 151, 181, 191]

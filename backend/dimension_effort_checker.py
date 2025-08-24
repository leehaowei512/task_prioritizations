import math


class EffortChecker:
    """
    Effort need to be a valid Fibonacci number
    """

    def __init__(self):
        pass

    @staticmethod
    def _is_perfect_square(n):
        root = math.isqrt(n)
        return root * root == n

    def effort_is_valid(self, n: int) -> bool:
        """
        Check if effort is valid Fibonacci number
        :param n:
        :return:
        """
        if n < 0:
            return False
        return self._is_perfect_square(5 * n * n + 4) or self._is_perfect_square(
            5 * n * n - 4
        )

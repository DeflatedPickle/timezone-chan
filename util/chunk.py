def chunk(li: list, length: int):
    return [li[x:x + length] for x in range(0, len(li), length)]

class LZ77:

    def __init__(
        self, search_window_size: int = 16, look_ahead_size: int = 8
    ):
        self.search_window_size = search_window_size
        self.look_ahead_size = look_ahead_size

    def compress(self, data: bytes) -> list:
        """Compresses byte data into a list of LZ77 triplets: (offset, length, next_symbol)."""
        n = len(data)
        tags = []
        current = 0

        while current < n:
            # 1. Update window boundary and reset match variables for this step
            search_window_start = max(0, current - self.search_window_size)
            longest_matching = 0
            position = 0

            # 2. Find longest match in search window
            for p in range(search_window_start, current):
                length = 0
                while (
                    current + length < n
                    and length < self.look_ahead_size
                    and data[p + length] == data[current + length]
                ):
                    length += 1

                if length > longest_matching:
                    longest_matching = length
                    position = current - p

            # 3. Get next literal symbol
            if current + longest_matching < n:
                next_symbol = bytes([data[current + longest_matching]])
            else:
                next_symbol = None  # End of stream reached

            # 4. Save tag and advance current index
            tags.append((position, longest_matching, next_symbol))
            current += longest_matching + 1

        return tags

    def decompress(self, tags: list) -> bytes:
        """Reconstructs the original byte sequence from LZ77 tags."""
        decompressed = bytearray()

        for pos, length, next_symbol in tags:
            if length > 0:
                start = len(decompressed) - pos
                for i in range(length):
                    decompressed.append(decompressed[start + i])

            if next_symbol is not None:
                decompressed.extend(next_symbol)

        return bytes(decompressed)

    def compress_file(self, filename: str) -> list:
        """Reads a file as binary and returns compressed LZ77 tags."""
        with open(filename, 'rb') as file:
            data = file.read()
        return self.compress(data)


# Execution Example
if __name__ == '__main__':
    lz = LZ77(search_window_size=16, look_ahead_size=8)

    # Compress
    tags = lz.compress_file("data.txt")
    print(f'Compressed Tags:   {tags}')

    # Decompress
    restored = lz.decompress(tags)
    print(f'Decompressed Data: {restored}')


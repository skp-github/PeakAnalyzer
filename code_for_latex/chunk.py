def chunk_array_by_sizes(self, data, chunk_sizes):
    chunks = []
    start_index = 0

    for size in chunk_sizes:
        if start_index + size > len(data):
            raise ValueError("Chunk sizes exceed the length of the data.")
        end_index = start_index + size
        chunk = data[start_index:end_index]
        chunks.append(chunk)
        start_index = end_index

    return chunks
import polars as pl


def load_vocabulary() -> pl.DataFrame:
    current_file_path = __file__
    current_folder_path = "/".join(current_file_path.split("/")[:-1])
    vocabulary_path = f"{current_folder_path}/vocabulary.xlsx"

    return pl.read_excel(vocabulary_path, infer_schema_length=10000)


vocabulary = load_vocabulary()

if __name__ == '__main__':
    print(vocabulary.head(3))

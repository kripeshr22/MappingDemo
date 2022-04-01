import category_encoders as ce

import get_data

def main(encode="one_hot", select_cols=None):
    tablename = 'cleanlacountytable'
    encode_col = 'zipcode5'

    df = get_data.get_df_from_heroku(tablename, select_cols)

    if encode == "hash":
        return encode_hash(df, 5, encode_col)
    if encode == "one_hot":
        return encode_one_hot(df, encode_col)


def encode_hash(df, count, encode_col):
    encoder_purpose = ce.HashingEncoder(n_components=count, cols=[encode_col])
    hashlabels = encoder_purpose.fit_transform(df)
    return hashlabels


def encode_one_hot(df, encode_col):
    enc = ce.OneHotEncoder(cols=[encode_col], return_df=True)
    onehotlabels = enc.fit_transform(df)
    return onehotlabels

if __name__ == "__main__":
    main()





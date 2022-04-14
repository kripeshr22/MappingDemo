import category_encoders as ce

import get_data

# case studies for test data
rows = ['20218343001022', '20218341002019', '20218326006011', '20218340027025', '20218335013012', '20218342002020', 
        '20214288014002', '20214291018015', '20214291015027', '20214288003023', '20214288002044', '20214291011012']
        #'20216211005003', '20216204021019', '20216323025055', '20216208001023', '20216209015040', '20216202002028'


def main(encode="hash", select_cols = None):
    encode_col = 'zipcode5'
    
    train_df = get_data.get_past4y_df('cleanlacountytable', select_cols)       # all properties assessed in 2018-2021
    est_df = get_data.get_distinct_df('laclean_pre2018_table', select_cols)     # all distinct properties to make predictions for
    
    if encode == "hash":
        train_df = encode_hash(train_df, 5, encode_col)
        est_df = encode_hash(est_df, 5, encode_col)
        return train_df, est_df
    if encode == "one_hot":
        train_df = encode_one_hot(train_df, encode_col)
        est_df = encode_one_hot(est_df, encode_col)
        return train_df, est_df
    else:
        print("encode was not /'hash/' or /'one_hot/'")

def test_df(encode="one_hot", select_cols=None):
    tablename = 'cleanlacountytable'
    encode_col = 'zipcode5'
    df = get_data.get_test_df(tablename, select_cols, rows)

    if encode == "hash":
        return encode_hash(df, 5, encode_col)
    if encode == "one_hot":
        return encode_one_hot(df, encode_col)

def test_df_noenc(select_cols):
    tablename = 'cleanlacountytable'
    df = get_data.get_test_df(tablename, select_cols, rows)
    return df

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





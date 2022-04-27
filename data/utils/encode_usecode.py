import category_encoders as ce
import pandas as pd
import get_data

# case studies for test data
rows = ['20218343001022', '20218341002019', '20218326006011', '20218340027025', '20218335013012', '20218342002020', 
        '20214288014002', '20214291018015', '20214291015027', '20214288003023', '20214288002044', '20214291011012']
        #'20216211005003', '20216204021019', '20216323025055', '20216208001023', '20216209015040', '20216202002028'

def test_df(select_cols):
    tablename = 'cleanlacountytable'
    df = get_data.get_test_df(tablename, select_cols, rows)
    df['usecode1'] = df['propertyusecode'].astype(str).str[0]
    df['usecode2'] = df['propertyusecode'].astype(str).str[1]
    df['usecode3'] = df['propertyusecode'].astype(str).str[2]
    df['usecode4'] = df['propertyusecode'].astype(str).str[3]
    df = df.drop(['propertyusecode'],1)

    # for col in ['usecode1', 'usecode2', 'usecode3', 'usecode4']:
    #     df[col] = df[col].apply(pd.to_numeric)
    #     df = encode_one_hot(df, col)

    print('encoded usecode')
    return df

def encode_hash(df, count, encode_col):
    encoder_purpose = ce.HashingEncoder(n_components=count, cols=[encode_col])
    hashlabels = encoder_purpose.fit_transform(df)
    return hashlabels


def encode_one_hot(df, encode_col):
    enc = ce.OneHotEncoder(cols=[encode_col], return_df=True)
    onehotlabels = enc.fit_transform(df)
    return onehotlabels

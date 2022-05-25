
















df = pd.DataFrame.from_dict(dic, orient='index', columns=['Codes'])


def color_rule(val):
    return ['background-color:'+str(val) ]

html_column = df.style.apply(color_rule, axis=1, subset=['index'])

html_column.to_excel('styled.xlsx', engine='openpyxl')

html_column
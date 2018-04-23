import pandas as pd 
#connect python to xlsx file and tell it which sheet to focus on.
xl = pd.ExcelFile('SalesDataFull.xlsx')
ReturnsOnlyData = xl.parse('Returns')

Return_ID_Col = ReturnsOnlyData[['Order ID']]

idList =  Return_ID_Col.values.tolist()

# print str(idList[1]).encode('utf-8')
OrdersOnlyData = xl.parse('Orders')
State_Profit_Col = OrdersOnlyData[['State','Profit']]


profitsInOrderOfStatesArray =  State_Profit_Col.groupby(by='State').sum().sort_values(by='Profit', ascending = False).values.tolist()[:10]
statesInOrderOfProfitArray = State_Profit_Col.groupby(by='State').sum().sort_values(by='Profit', ascending = False).index.get_level_values(0).tolist()
# print statesInOrderOfProfitArray[:10] #10 states in order
# print statesInOrderOfProfitArray

resultsArray = []
for i in range(10):
    print(statesInOrderOfProfitArray[i].encode('utf-8'))
    resultsArray.append(statesInOrderOfProfitArray[i])

print resultsArray
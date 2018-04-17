import pandas as pd 
#connect python to xlsx file and tell it which sheet to focus on.
xl = pd.ExcelFile('SalesDataFull.xlsx')
ReturnsOnlyData = xl.parse('Returns')

Return_ID_Col = ReturnsOnlyData[['Order ID']]

idList =  Return_ID_Col.values.tolist()

# print str(idList[1]).encode('utf-8')

resultList = []
OrdersOnlyData = xl.parse('Orders')

for item in idList:         
    findThisID =  u", ".join(item)
    a = OrdersOnlyData.loc[OrdersOnlyData['Order ID'] == findThisID]
    resultList.append(a['Product Name'])

print resultList




# print a['Product Name']




# #Top/Bottom 20% of states sorted according to profits gained/lost. 
# State_Profit_Col = OrdersOnlyData[['State','Profit']]
# State_Profits = State_Profit_Col.groupby(by='State').sum().sort_values(by='Profit', ascending = False) 
# print("\nStates with the highest profit.")


# # print(State_Profits.head(10).columns) 


# print State_Profit_Col.columns
# print State_Profits.head(10).values.tolist()



# print('='*30)
# print("\nStates with the lowest profit.")
# print(State_Profits.tail(10))
# #tail_ending = tail_end + State_Profits[::-1] 
# #print(tail_ending)


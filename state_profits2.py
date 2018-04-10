import pandas as pd 
#connect python to xlsx file and tell it which sheet to focus on.
xl = pd.ExcelFile('SalesDataFull.xlsx')
OrdersOnlyData = xl.parse('Orders')

#Top/Bottom 20% of states sorted according to profits gained/lost. 
State_Profit_Col = OrdersOnlyData[['State','Profit']]
State_Profits = State_Profit_Col.groupby(by='State').sum().sort_values(by='Profit', ascending = False) 
print("\nStates with the highest profit.")
print(State_Profits.head(10)) 
print('='*30)
print("\nStates with the lowest profit.")
print(State_Profits.tail(10))
#tail_ending = tail_end + State_Profits[::-1] 
#print(tail_ending)


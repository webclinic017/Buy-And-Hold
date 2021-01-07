### PRODUCT INFORMATION --------------------------------------------------------------------------------
# Copyright InnoQuantivity.com, granted to the public domain.
# Use entirely at your own risk.
# This algorithm contains open source code from other sources and no claim is being made to such code.
# Do not remove this copyright notice.
### ----------------------------------------------------------------------------------------------------

from BuyAndHoldAlphaCreation import BuyAndHoldAlphaCreationModel
from CustomEqualWeightingPortfolioConstruction import CustomEqualWeightingPortfolioConstructionModel

class BuyAndHoldFrameworkAlgorithm(QCAlgorithmFramework):
    
    '''
    Trading Logic:
        This algorithm buys and holds the provided tickers from the start date until the end date
    Modules:
        Universe: Manual input of tickers
        Alpha: Constant creation of Up Insights every trading bar
        Portfolio: Equal Weighting (allocate equal amounts of portfolio % to each security)
            - If some of the tickers did not exist at the start date, it will buy them when they first appeared in the market,
                in which case it will sell part of the existing securities in order to buy the new ones keeping an equally weighted portfolio
            - To rebalance the portfolio periodically to ensure equal weighting, change the rebalancingParam below
        Execution: Immediate Execution with Market Orders
        Risk: Null
    '''

    def Initialize(self):
        
        ### user-defined inputs --------------------------------------------------------------

        self.SetStartDate(1998, 1, 1)   # set start date
        #self.SetEndDate(2019, 1, 1)     # set end date
        self.SetCash(100000)            # set strategy cash
        
        # add tickers to the list
        tickers = ['FB', 'AMZN', 'NFLX', 'GOOG']
        #tickers = ['SPY']
        
        # rebalancing period (to enable rebalancing enter an integer for number of days, e.g. 1, 7, 30, 365)
        rebalancingParam = False
            
        ### -----------------------------------------------------------------------------------
        
        # set the brokerage model for slippage and fees
        self.SetBrokerageModel(AlphaStreamsBrokerageModel())
        
        # set requested data resolution and disable fill forward data
        self.UniverseSettings.Resolution = Resolution.Daily
        self.UniverseSettings.FillForward = False
        
        symbols = []
        # loop through the tickers list and create symbols for the universe
        for i in range(len(tickers)):
            symbols.append(Symbol.Create(tickers[i], SecurityType.Equity, Market.USA))
        
        # select modules
        self.SetUniverseSelection(ManualUniverseSelectionModel(symbols))
        self.SetAlpha(BuyAndHoldAlphaCreationModel())
        self.SetPortfolioConstruction(CustomEqualWeightingPortfolioConstructionModel(rebalancingParam = rebalancingParam))
        self.SetExecution(ImmediateExecutionModel())
        self.SetRiskManagement(NullRiskManagementModel())
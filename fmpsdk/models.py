import math
import os
import sys
from typing import Annotated, Any, Dict, List, Optional, Union

from pydantic import BaseModel, BeforeValidator, Field, RootModel, model_validator

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


def _round_float_to_int(value: Any) -> Any:
    """Round finite floats to the nearest int, halves away from zero.

    FMP returns fractional values for fields that are logically integers, e.g.
    split-adjusted historical share counts (1756172378.625) or float artifacts
    (1773627764.9999995). Strict ``int`` rejects these. Non-floats and
    non-finite floats pass through unchanged so pydantic validates them as usual.
    """
    if isinstance(value, float) and math.isfinite(value):
        return int(math.copysign(math.floor(abs(value) + 0.5), value))
    return value


# int that accepts fractional floats by rounding. Whole-number inputs validate
# exactly as plain ``int`` does.
LenientInt = Annotated[int, BeforeValidator(_round_float_to_int)]


class FMPBaseModel(BaseModel):
    """Base model for all FMP models that handles 'None' string conversion."""

    @model_validator(mode="before")
    @classmethod
    def convert_none_strings(cls, values: Any) -> Any:
        """Convert 'None' strings to actual None values."""
        if isinstance(values, dict):
            return {k: None if v == "None" else v for k, v in values.items()}
        return values


class FMPSymbolSearch(FMPBaseModel):
    symbol: str
    name: str
    currency: str
    exchangeFullName: Optional[str] = None
    exchange: Optional[str] = None


class FMPCompanyNameSearch(FMPBaseModel):
    symbol: str
    name: str
    currency: str
    exchangeFullName: Optional[str] = None
    exchange: Optional[str] = None


class FMPCompanyCIKSearch(FMPBaseModel):
    symbol: str
    companyName: str
    cik: str
    exchangeFullName: str
    exchange: str
    currency: str


class FMPCusipSearch(FMPBaseModel):
    symbol: str
    companyName: str
    cusip: str
    marketCap: float


class FMPIsinSearch(FMPBaseModel):
    symbol: str
    name: str
    isin: str
    marketCap: float


class FMPStockScreenerResult(FMPBaseModel):
    symbol: str
    companyName: str
    marketCap: Optional[float] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    beta: Optional[float] = None
    price: float
    lastAnnualDividend: Optional[float] = None
    volume: float
    exchange: str
    exchangeShortName: str
    country: Optional[str] = None
    isEtf: bool
    isFund: bool
    isActivelyTrading: Optional[bool] = None


class FMPCompanyProfile(FMPBaseModel):
    symbol: str
    price: Optional[float] = None
    beta: Optional[float] = None
    volAvg: Optional[float] = None
    mktCap: Optional[float] = None
    lastDiv: Optional[float] = None
    range: Optional[str] = None
    changes: Optional[float] = None
    companyName: Optional[str] = None
    currency: Optional[str] = None
    cik: Optional[str] = None
    isin: Optional[str] = None
    cusip: Optional[str] = None
    exchange: Optional[str] = None
    exchangeShortName: Optional[str] = None
    industry: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    ceo: Optional[str] = None
    sector: Optional[str] = None
    country: Optional[str] = None
    fullTimeEmployees: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    dcfDiff: Optional[float] = None
    dcf: Optional[float] = None
    image: Optional[str] = None
    ipoDate: Optional[str] = None
    defaultImage: Optional[bool] = None
    isEtf: Optional[bool] = None
    isActivelyTrading: Optional[bool] = None
    isAdr: Optional[bool] = None
    isFund: Optional[bool] = None


class FMPSymbolAndCompanyNameList(FMPBaseModel):
    symbol: str
    companyName: Optional[str] = None


class FMPSymbolAndNameList(FMPBaseModel):
    symbol: str
    name: Optional[str] = None


class FMPFinancialStatementSymbolList(FMPBaseModel):
    symbol: str
    companyName: str
    tradingCurrency: str
    reportingCurrency: Optional[str] = None


class FMPSymbolAndCIKList(FMPBaseModel):
    cik: str
    companyName: str


class FMPSymbolChange(FMPBaseModel):
    date: str
    companyName: str
    oldSymbol: str
    newSymbol: str


class FMPEarningsTranscriptList(FMPBaseModel):
    symbol: str
    companyName: str
    noOfTranscripts: str


class FMPExchangeInfo(FMPBaseModel):
    exchange: str
    name: str
    countryName: str
    countryCode: str
    symbolSuffix: str
    isMarketOpen: Optional[bool] = None
    delay: Optional[str] = None


class FMPSector(FMPBaseModel):
    sector: str


class FMPIndustry(FMPBaseModel):
    industry: str


class FMPCountry(FMPBaseModel):
    country: str

    @property
    def name(self) -> str:
        """Alias for country field to match expected interface."""
        return self.country


class FMPAnalystEstimates(FMPBaseModel):
    symbol: str
    date: str
    revenueLow: LenientInt
    revenueHigh: LenientInt
    revenueAvg: LenientInt
    ebitdaLow: LenientInt
    ebitdaHigh: LenientInt
    ebitdaAvg: LenientInt
    ebitLow: LenientInt
    ebitHigh: LenientInt
    ebitAvg: LenientInt
    netIncomeLow: LenientInt
    netIncomeHigh: LenientInt
    netIncomeAvg: float
    sgaExpenseLow: LenientInt
    sgaExpenseHigh: LenientInt
    sgaExpenseAvg: LenientInt
    epsAvg: float
    epsHigh: float
    epsLow: float
    numAnalystsRevenue: LenientInt
    numAnalystsEps: LenientInt


class FMPRatingSnapshot(FMPBaseModel):
    symbol: str
    rating: str
    overallScore: LenientInt
    discountedCashFlowScore: LenientInt
    returnOnEquityScore: LenientInt
    returnOnAssetsScore: LenientInt
    debtToEquityScore: LenientInt
    priceToEarningsScore: LenientInt
    priceToBookScore: LenientInt


class FMPHistoricalRating(FMPBaseModel):
    symbol: str
    date: str
    rating: str
    overallScore: LenientInt
    discountedCashFlowScore: LenientInt
    returnOnEquityScore: LenientInt
    returnOnAssetsScore: LenientInt
    debtToEquityScore: LenientInt
    priceToEarningsScore: LenientInt
    priceToBookScore: LenientInt


class FMPHistoricalRatingV3(FMPBaseModel):
    symbol: str
    date: str
    rating: str
    ratingScore: LenientInt
    ratingRecommendation: str
    ratingDetailsDCFScore: LenientInt
    ratingDetailsDCFRecommendation: str
    ratingDetailsROEScore: LenientInt
    ratingDetailsROERecommendation: str
    ratingDetailsROAScore: LenientInt
    ratingDetailsROARecommendation: str
    ratingDetailsDEScore: LenientInt
    ratingDetailsDERecommendation: str
    ratingDetailsPEScore: LenientInt
    ratingDetailsPERecommendation: str
    ratingDetailsPBScore: LenientInt
    ratingDetailsPBRecommendation: str


class FMPPriceTargetSummary(FMPBaseModel):
    symbol: str
    lastMonthCount: LenientInt
    lastMonthAvgPriceTarget: float
    lastQuarterCount: LenientInt
    lastQuarterAvgPriceTarget: float
    lastYearCount: LenientInt
    lastYearAvgPriceTarget: float
    allTimeCount: LenientInt
    allTimeAvgPriceTarget: float
    publishers: str


class FMPPriceTargetConsensus(FMPBaseModel):
    symbol: str
    targetHigh: float
    targetLow: float
    targetConsensus: float
    targetMedian: float


class FMPPriceTargetNews(FMPBaseModel):
    symbol: str
    publishedDate: str
    newsURL: str
    newsTitle: str
    analystName: Optional[str] = None
    priceTarget: float
    adjPriceTarget: float
    priceWhenPosted: float
    newsPublisher: str
    newsBaseURL: str
    analystCompany: str


class FMPStockGrade(FMPBaseModel):
    symbol: str
    date: str
    gradingCompany: str
    previousGrade: str
    newGrade: str
    action: str


class FMPHistoricalStockGrade(FMPBaseModel):
    symbol: str
    date: str
    analystRatingsStrongBuy: LenientInt
    analystRatingsBuy: LenientInt
    analystRatingsHold: LenientInt
    analystRatingsSell: LenientInt
    analystRatingsStrongSell: LenientInt


class FMPStockGradeSummary(FMPBaseModel):
    symbol: str
    strongBuy: LenientInt
    buy: LenientInt
    hold: LenientInt
    sell: LenientInt
    strongSell: LenientInt
    consensus: str


class FMPStockGradeNews(FMPBaseModel):
    symbol: str
    publishedDate: str
    newsURL: str
    newsTitle: str
    newsBaseURL: str
    newsPublisher: str
    newGrade: str
    previousGrade: Optional[str] = None
    gradingCompany: str
    action: str
    priceWhenPosted: float


class FMPDividend(FMPBaseModel):
    symbol: str
    date: str
    recordDate: str
    paymentDate: str
    declarationDate: str
    adjDividend: float
    dividend: float
    yield_: Optional[float] = None
    frequency: str


class FMPDividendCalendarEventV3(FMPBaseModel):
    date: str
    label: str
    adjDividend: Optional[float]
    symbol: str
    dividend: Optional[float]
    recordDate: Optional[str] = None
    paymentDate: Optional[str] = None
    declarationDate: Optional[str] = None


class FMPEarningsReport(FMPBaseModel):
    symbol: str
    date: str
    epsActual: Optional[float] = None
    epsEstimated: Optional[float] = None
    revenueActual: Optional[float] = None
    revenueEstimated: Optional[float] = None
    lastUpdated: str


class FMPEarningsCalendarEvent(FMPBaseModel):
    symbol: str
    date: str
    epsActual: Optional[float] = None
    epsEstimated: Optional[float] = None
    revenueActual: Optional[float] = None
    revenueEstimated: Optional[float] = None
    lastUpdated: str


class FMPUpcomingIPO(FMPBaseModel):
    symbol: str
    date: str
    daa: str
    company: str
    exchange: str
    actions: str
    shares: Optional[LenientInt] = None
    priceRange: Optional[str] = None
    marketCap: Optional[LenientInt] = None


class FMPDisclosureFiling(FMPBaseModel):
    symbol: str
    cik: str
    filingDate: str
    acceptedDate: str
    effectivenessDate: str
    form: str
    url: str


class FMPProspectusFiling(FMPBaseModel):
    symbol: str
    acceptedDate: str
    filingDate: str
    ipoDate: str
    cik: str
    pricePublicPerShare: float
    pricePublicTotal: float
    discountsAndCommissionsPerShare: float
    discountsAndCommissionsTotal: Optional[float] = None
    proceedsBeforeExpensesPerShare: float
    proceedsBeforeExpensesTotal: float
    form: str
    url: str


class FMPStockSplit(FMPBaseModel):
    symbol: str
    date: str
    numerator: float
    denominator: float


class FMPHistoricalDataPointLight(FMPBaseModel):
    symbol: str
    date: str
    price: float
    volume: LenientInt


class FMPHistoricalDataPointFull(FMPBaseModel):
    symbol: str
    date: str
    open: float = None
    high: float = None
    low: float = None
    close: float = None
    volume: float = None
    change: float = None
    changePercent: float = None
    vwap: float = None


class FMPHistoricalDataPointAdjusted(FMPBaseModel):
    symbol: str
    date: str
    adjOpen: float = None
    adjHigh: float = None
    adjLow: float = None
    adjClose: float = None
    volume: float = None


class FMPIntradayDataPoint(FMPBaseModel):
    date: str
    open: float
    low: float
    high: float
    close: float
    volume: float


class FMPCompanyNote(FMPBaseModel):
    cik: str
    symbol: str
    title: str
    exchange: str


class FMPStockPeer(FMPBaseModel):
    symbol: str
    companyName: str
    price: float
    mktCap: LenientInt


class FMPDelistedCompany(FMPBaseModel):
    symbol: str
    companyName: str
    exchange: str
    ipoDate: str
    delistedDate: str


class FMPEmployeeCount(FMPBaseModel):
    symbol: str
    cik: str
    acceptanceTime: str
    periodOfReport: str
    companyName: str
    formType: str
    filingDate: str
    employeeCount: LenientInt
    source: str


class FMPHistoricalEmployeeCount(FMPBaseModel):
    symbol: str
    cik: str
    acceptanceTime: str
    periodOfReport: str
    companyName: str
    formType: str
    filingDate: str
    employeeCount: LenientInt
    source: str


class FMPMarketCap(FMPBaseModel):
    symbol: str
    date: str
    marketCap: float


class FMPShareFloat(FMPBaseModel):
    symbol: str
    date: Optional[str] = None
    freeFloat: Optional[float] = None
    floatShares: Optional[LenientInt] = None
    outstandingShares: LenientInt


class FMPMergerAcquisition(FMPBaseModel):
    symbol: str
    companyName: str
    cik: str
    targetedCompanyName: str
    targetedCik: Optional[str] = None
    targetedSymbol: Optional[str] = None
    transactionDate: str
    acceptedDate: str
    link: str


class FMPExecutiveProfile(FMPBaseModel):
    title: str
    name: str
    pay: Optional[float] = None
    currencyPay: str
    gender: Optional[str] = None
    yearBorn: Optional[LenientInt] = None
    active: Optional[LenientInt] = None


class FMPExecutiveCompensation(FMPBaseModel):
    cik: str
    symbol: str
    companyName: str
    filingDate: str
    acceptedDate: str
    nameAndPosition: str
    year: LenientInt
    salary: Optional[LenientInt] = None
    bonus: Optional[LenientInt] = None
    stockAward: Optional[LenientInt] = None
    optionAward: Optional[LenientInt] = None
    incentivePlanCompensation: Optional[LenientInt] = None
    allOtherCompensation: Optional[LenientInt] = None
    total: Optional[LenientInt] = None
    link: str


class FMPExecutiveCompensationBenchmark(FMPBaseModel):
    industryTitle: str
    year: LenientInt
    averageCompensation: float


class FMPCommitmentOfTradersReport(FMPBaseModel):
    symbol: str
    date: str
    name: str
    sector: str
    marketAndExchangeNames: str
    cftcContractMarketCode: str
    cftcMarketCode: str
    cftcRegionCode: str
    cftcCommodityCode: str
    openInterestAll: LenientInt
    noncommPositionsLongAll: LenientInt
    noncommPositionsShortAll: LenientInt
    noncommPositionsSpreadAll: LenientInt
    commPositionsLongAll: LenientInt
    commPositionsShortAll: LenientInt
    totReptPositionsLongAll: LenientInt
    totReptPositionsShortAll: LenientInt
    nonreptPositionsLongAll: LenientInt
    nonreptPositionsShortAll: LenientInt
    openInterestOld: LenientInt
    noncommPositionsLongOld: LenientInt
    noncommPositionsShortOld: LenientInt
    noncommPositionsSpreadOld: LenientInt
    commPositionsLongOld: LenientInt
    commPositionsShortOld: LenientInt
    totReptPositionsLongOld: LenientInt
    totReptPositionsShortOld: LenientInt
    nonreptPositionsLongOld: LenientInt
    nonreptPositionsShortOld: LenientInt
    openInterestOther: LenientInt
    noncommPositionsLongOther: LenientInt
    noncommPositionsShortOther: LenientInt
    noncommPositionsSpreadOther: LenientInt
    commPositionsLongOther: LenientInt
    commPositionsShortOther: LenientInt
    totReptPositionsLongOther: LenientInt
    totReptPositionsShortOther: LenientInt
    nonreptPositionsLongOther: LenientInt
    nonreptPositionsShortOther: LenientInt
    changeInOpenInterestAll: LenientInt
    changeInNoncommLongAll: LenientInt
    changeInNoncommShortAll: LenientInt
    changeInNoncommSpeadAll: LenientInt
    changeInCommLongAll: LenientInt
    changeInCommShortAll: LenientInt
    changeInTotReptLongAll: LenientInt
    changeInTotReptShortAll: LenientInt
    changeInNonreptLongAll: LenientInt
    changeInNonreptShortAll: LenientInt
    pctOfOpenInterestAll: LenientInt
    pctOfOiNoncommLongAll: float
    pctOfOiNoncommShortAll: float
    pctOfOiNoncommSpreadAll: float
    pctOfOiCommLongAll: float
    pctOfOiCommShortAll: float
    pctOfOiTotReptLongAll: float
    pctOfOiTotReptShortAll: float
    pctOfOiNonreptLongAll: float
    pctOfOiNonreptShortAll: float
    pctOfOpenInterestOl: float
    pctOfOiNoncommLongOl: float
    pctOfOiNoncommShortOl: float
    pctOfOiNoncommSpreadOl: float
    pctOfOiCommLongOl: float
    pctOfOiCommShortOl: float
    pctOfOiTotReptLongOl: float
    pctOfOiTotReptShortOl: float
    pctOfOiNonreptLongOl: float
    pctOfOiNonreptShortOl: float
    pctOfOpenInterestOther: float
    pctOfOiNoncommLongOther: float
    pctOfOiNoncommShortOther: float
    pctOfOiNoncommSpreadOther: float
    pctOfOiCommLongOther: float
    pctOfOiCommShortOther: float
    pctOfOiTotReptLongOther: float
    pctOfOiTotReptShortOther: float
    pctOfOiNonreptLongOther: float
    pctOfOiNonreptShortOther: float
    tradersTotAll: LenientInt
    tradersNoncommLongAll: LenientInt
    tradersNoncommShortAll: LenientInt
    tradersNoncommSpreadAll: LenientInt
    tradersCommLongAll: LenientInt
    tradersCommShortAll: LenientInt
    tradersTotReptLongAll: LenientInt
    tradersTotReptShortAll: LenientInt
    tradersTotOl: LenientInt
    tradersNoncommLongOl: LenientInt
    tradersNoncommShortOl: LenientInt
    tradersNoncommSpeadOl: LenientInt
    tradersCommLongOl: LenientInt
    tradersCommShortOl: LenientInt
    tradersTotReptLongOl: LenientInt
    tradersTotReptShortOl: LenientInt
    tradersTotOther: LenientInt
    tradersNoncommLongOther: LenientInt
    tradersNoncommShortOther: LenientInt
    tradersNoncommSpreadOther: LenientInt
    tradersCommLongOther: LenientInt
    tradersCommShortOther: LenientInt
    tradersTotReptLongOther: LenientInt
    tradersTotReptShortOther: LenientInt
    concGrossLe4TdrLongAll: float
    concGrossLe4TdrShortAll: float
    concGrossLe8TdrLongAll: float
    concGrossLe8TdrShortAll: float
    concNetLe4TdrLongAll: float
    concNetLe4TdrShortAll: float
    concNetLe8TdrLongAll: float
    concNetLe8TdrShortAll: float
    concGrossLe4TdrLongOl: float
    concGrossLe4TdrShortOl: float
    concGrossLe8TdrLongOl: float
    concGrossLe8TdrShortOl: float
    concNetLe4TdrLongOl: float
    concNetLe4TdrShortOl: float
    concNetLe8TdrLongOl: float
    concNetLe8TdrShortOl: float
    concGrossLe4TdrLongOther: float
    concGrossLe4TdrShortOther: float
    concGrossLe8TdrLongOther: float
    concGrossLe8TdrShortOther: float
    concNetLe4TdrLongOther: float
    concNetLe4TdrShortOther: float
    concNetLe8TdrLongOther: float
    concNetLe8TdrShortOther: float
    contractUnits: str


class FMPCommitmentOfTradersAnalysis(FMPBaseModel):
    symbol: str
    date: str
    name: str
    sector: str
    exchange: str
    currentLongMarketSituation: float
    currentShortMarketSituation: float
    marketSituation: str
    previousLongMarketSituation: float
    previousShortMarketSituation: float
    previousMarketSituation: str
    netPostion: LenientInt
    previousNetPosition: LenientInt
    changeInNetPosition: float
    marketSentiment: str
    reversalTrend: bool


class FMPDcfValuation(FMPBaseModel):
    symbol: str
    date: str
    dcf: Optional[float] = None
    Stock_Price: Optional[float] = Field(default=None, alias="Stock Price")


class FMPDCFCustomValuation(FMPBaseModel):
    year: str
    symbol: str
    revenue: Optional[LenientInt] = None
    revenuePercentage: Optional[float] = None
    ebitda: Optional[float] = None
    ebitdaPercentage: Optional[float] = None
    ebit: Optional[float] = None
    ebitPercentage: Optional[float] = None
    depreciation: Optional[float] = None
    depreciationPercentage: Optional[float] = None
    totalCash: Optional[float] = None
    totalCashPercentage: Optional[float] = None
    receivables: Optional[float] = None
    receivablesPercentage: Optional[float] = None
    inventories: Optional[float] = None
    inventoriesPercentage: Optional[float] = None
    payable: Optional[float] = None
    payablePercentage: Optional[float] = None
    capitalExpenditure: Optional[float] = None
    capitalExpenditurePercentage: Optional[float] = None
    price: Optional[float] = None
    beta: Optional[float] = None
    dilutedSharesOutstanding: Optional[LenientInt] = None
    costofDebt: Optional[float] = None
    taxRate: Optional[float] = None
    afterTaxCostOfDebt: Optional[float] = None
    riskFreeRate: Optional[float] = None
    marketRiskPremium: Optional[float] = None
    costOfEquity: Optional[float] = None
    totalDebt: Optional[LenientInt] = None
    totalEquity: Optional[LenientInt] = None
    totalCapital: Optional[LenientInt] = None
    debtWeighting: Optional[float] = None
    equityWeighting: Optional[float] = None
    wacc: Optional[float] = None
    taxRateCash: Optional[LenientInt] = None
    ebiat: Optional[float] = None
    ufcf: Optional[float] = None
    sumPvUfcf: Optional[LenientInt] = None
    longTermGrowthRate: Optional[float] = None
    terminalValue: Optional[LenientInt] = None
    presentTerminalValue: Optional[LenientInt] = None
    enterpriseValue: Optional[LenientInt] = None
    netDebt: Optional[LenientInt] = None
    equityValue: Optional[LenientInt] = None
    equityValuePerShare: Optional[float] = None
    freeCashFlowT1: Optional[LenientInt] = None


class FMPTreasuryRates(FMPBaseModel):
    date: str
    month1: float
    month2: float
    month3: float
    month6: float
    year1: float
    year2: float
    year3: float
    year5: float
    year7: float
    year10: float
    year20: float
    year30: float


class FMPEconomicIndicator(FMPBaseModel):
    name: str
    date: str
    value: float


class FMPEconomicCalendarEvent(FMPBaseModel):
    date: str
    country: str
    event: str
    currency: str
    previous: Optional[float] = None
    estimate: Optional[float] = None
    actual: Optional[float] = None
    change: Optional[float] = None
    impact: Optional[str] = None
    changePercentage: Optional[float] = None
    unit: Optional[str] = None


class FMPMarketRiskPremium(FMPBaseModel):
    country: str
    continent: Optional[str] = None
    countryRiskPremium: float
    totalEquityRiskPremium: float


class FMPESGFiling(FMPBaseModel):
    date: str
    acceptedDate: str
    symbol: str
    cik: str
    companyName: str
    formType: str
    environmentalScore: float
    socialScore: float
    governanceScore: float
    ESGScore: float
    url: str


class FMPESGRating(FMPBaseModel):
    symbol: str
    cik: str
    companyName: str
    industry: str
    fiscalYear: LenientInt
    ESGRiskRating: str
    industryRank: str


class FMPESGBenchmark(FMPBaseModel):
    fiscalYear: LenientInt
    sector: str
    environmentalScore: float
    socialScore: float
    governanceScore: float
    ESGScore: float


class FMPFundHolding(FMPBaseModel):
    symbol: str
    asset: str
    name: str
    isin: str
    securityCusip: str
    sharesNumber: LenientInt
    weightPercentage: float
    marketValue: float
    updatedAt: str
    updated: str


class FMPFundInfoSectorsListItem(FMPBaseModel):
    industry: str
    exposure: float


class FMPCommodityListItem(FMPBaseModel):
    symbol: str
    name: str
    exchange: Optional[str] = None
    tradeMonth: str
    currency: Optional[str] = None


class FMPCryptocurrencyListItem(FMPBaseModel):
    symbol: str
    name: str
    exchange: str
    icoDate: Optional[str] = None
    circulatingSupply: Optional[float] = None
    totalSupply: Optional[float] = None


class FMPIndexListItem(FMPBaseModel):
    symbol: str
    name: str
    exchange: str
    currency: str


class FMPFundInfo(FMPBaseModel):
    symbol: str
    name: str
    description: str
    isin: str
    assetClass: str
    securityCusip: str
    domicile: str
    website: str
    etfCompany: Optional[str]
    expenseRatio: float
    assetsUnderManagement: float
    avgVolume: float
    inceptionDate: str
    nav: float
    navCurrency: str
    holdingsCount: LenientInt
    updatedAt: str
    sectorsList: List[FMPFundInfoSectorsListItem]


class FMPFundCountryAllocation(FMPBaseModel):
    country: str
    weightPercentage: str


class FMPFundAssetExposure(FMPBaseModel):
    symbol: str
    asset: str
    sharesNumber: LenientInt
    weightPercentage: float
    marketValue: LenientInt


class FMPFundSectorWeighting(FMPBaseModel):
    symbol: str
    sector: str
    weightPercentage: float


class FMPFundHolder(FMPBaseModel):
    cik: str
    holder: str
    shares: LenientInt
    dateReported: str
    change: LenientInt
    weightPercent: float


class FMPFundDisclosure(FMPBaseModel):
    cik: str
    date: str
    acceptedDate: str
    symbol: str
    name: str
    lei: str
    title: str
    cusip: str
    isin: str
    balance: LenientInt
    units: str
    cur_cd: str
    valUsd: float
    pctVal: float
    payoffProfile: str
    assetCat: str
    issuerCat: str
    invCountry: str
    isRestrictedSec: str
    fairValLevel: str
    isCashCollateral: str
    isNonCashCollateral: str
    isLoanByFund: str


class FMPFundDisclosureNameSearch(FMPBaseModel):
    symbol: str
    cik: str
    classId: str
    seriesId: str
    entityName: str
    entityOrgType: str
    seriesName: str
    className: str
    reportingFileNumber: str
    address: str
    city: str
    zipCode: str
    state: str


class FMPFundDisclosureDate(FMPBaseModel):
    date: str
    year: LenientInt
    quarter: LenientInt


class FMPCrowdfundingCampaign(FMPBaseModel):
    cik: str
    companyName: Optional[str] = None
    date: Optional[str] = None
    filingDate: str
    acceptedDate: str
    formType: str
    formSignification: str
    nameOfIssuer: Optional[str] = None
    legalStatusForm: Optional[str] = None
    jurisdictionOrganization: Optional[str] = None
    issuerStreet: Optional[str] = None
    issuerCity: Optional[str] = None
    issuerStateOrCountry: Optional[str] = None
    issuerZipCode: Optional[str] = None
    issuerWebsite: Optional[str] = None
    intermediaryCompanyName: Optional[str] = None
    intermediaryCommissionCik: Optional[str] = None
    intermediaryCommissionFileNumber: Optional[str] = None
    compensationAmount: Optional[str] = None
    financialInterest: Optional[str] = None
    securityOfferedType: Optional[str] = None
    securityOfferedOtherDescription: Optional[str] = None
    numberOfSecurityOffered: LenientInt
    offeringPrice: float
    offeringAmount: float
    overSubscriptionAccepted: str
    overSubscriptionAllocationType: Optional[str] = None
    maximumOfferingAmount: Optional[float] = None
    offeringDeadlineDate: Optional[str] = None
    currentNumberOfEmployees: LenientInt
    totalAssetMostRecentFiscalYear: float
    totalAssetPriorFiscalYear: float
    cashAndCashEquiValentMostRecentFiscalYear: float
    cashAndCashEquiValentPriorFiscalYear: float
    accountsReceivableMostRecentFiscalYear: float
    accountsReceivablePriorFiscalYear: float
    shortTermDebtMostRecentFiscalYear: float
    shortTermDebtPriorFiscalYear: float
    longTermDebtMostRecentFiscalYear: float
    longTermDebtPriorFiscalYear: float
    revenueMostRecentFiscalYear: float
    revenuePriorFiscalYear: float
    costGoodsSoldMostRecentFiscalYear: float
    costGoodsSoldPriorFiscalYear: float
    taxesPaidMostRecentFiscalYear: float
    taxesPaidPriorFiscalYear: float
    netIncomeMostRecentFiscalYear: float
    netIncomePriorFiscalYear: float


class FMPCrowdfundingSearch(FMPBaseModel):
    cik: str
    name: str
    date: Optional[str] = None


class FMPEquityOffering(FMPBaseModel):
    cik: str
    companyName: str
    date: Optional[str] = None
    filingDate: str
    acceptedDate: str
    formType: str
    formSignification: str
    entityName: str
    issuerStreet: str
    issuerCity: str
    issuerStateOrCountry: str
    issuerStateOrCountryDescription: str
    issuerZipCode: str
    issuerPhoneNumber: str
    jurisdictionOfIncorporation: str
    entityType: str
    incorporatedWithinFiveYears: Optional[bool] = None
    yearOfIncorporation: str
    relatedPersonFirstName: Optional[str] = None
    relatedPersonLastName: str
    relatedPersonStreet: str
    relatedPersonCity: str
    relatedPersonStateOrCountry: str
    relatedPersonStateOrCountryDescription: str
    relatedPersonZipCode: str
    relatedPersonRelationship: str
    industryGroupType: str
    revenueRange: Optional[str] = None
    federalExemptionsExclusions: str
    isAmendment: Optional[bool] = None
    dateOfFirstSale: str
    durationOfOfferingIsMoreThanYear: Optional[bool] = None
    securitiesOfferedAreOfEquityType: Optional[bool] = None
    isBusinessCombinationTransaction: Optional[bool] = None
    minimumInvestmentAccepted: LenientInt
    totalOfferingAmount: LenientInt
    totalAmountSold: LenientInt
    totalAmountRemaining: LenientInt
    hasNonAccreditedInvestors: Optional[bool] = None
    totalNumberAlreadyInvested: LenientInt
    salesCommissions: LenientInt
    findersFees: LenientInt
    grossProceedsUsed: LenientInt


class FMPEquityOfferingSearch(FMPBaseModel):
    cik: str
    name: str
    date: str


class FMPForexPair(FMPBaseModel):
    symbol: str
    fromCurrency: str
    toCurrency: str
    fromName: str
    toName: str


class FMPFinancialReportDate(FMPBaseModel):
    symbol: str
    fiscalYear: LenientInt
    period: str
    linkJson: str
    linkXlsx: str


# Root model for each dictionary item in a section
class FinancialSectionEntry(RootModel[Dict[str, List[Union[str, float, int, None]]]]):
    pass


# Root model for a section (which is a list of entries)
class FinancialSection(RootModel[List[FinancialSectionEntry]]):
    pass


class FMPFullFinancialReport(FMPBaseModel):
    symbol: str
    period: Optional[str] = None
    year: Optional[str] = None

    # Use model_config to allow extra fields for all the financial sections
    model_config = {"extra": "allow"}

    @property
    def sections(self) -> Dict[str, Any]:
        """Get all the financial statement sections (excluding symbol, period, year)."""
        return {
            k: v
            for k, v in self.__dict__.items()
            if k not in {"symbol", "period", "year"}
        }

    @classmethod
    def from_raw(
        cls,
        raw: Dict[str, Union[str, List[Dict[str, List[Union[str, int, float, None]]]]]],
    ):
        fixed_fields = {
            "symbol": str(raw.get("symbol", "")),
            "period": str(raw.get("period", "")) if raw.get("period") else None,
            "year": str(raw.get("year", "")) if raw.get("year") else None,
        }

        # Create instance with fixed fields
        instance = cls(**fixed_fields)

        # Add sections as dynamic attributes
        for k, v in raw.items():
            if k not in {"symbol", "period", "year"} and isinstance(v, list):
                # Process each entry in the list
                section_entries = []
                for entry in v:
                    if isinstance(entry, dict):
                        section_entries.append(FinancialSectionEntry(entry))
                setattr(instance, k, FinancialSection(section_entries))

        return instance


class FMPRevenueSegmentation(FMPBaseModel):
    symbol: str
    fiscalYear: LenientInt
    period: str
    reportedCurrency: Optional[str] = None
    date: str
    data: Optional[Dict[str, LenientInt]] = None


class FMPAsReportedIncomeStatement(FMPBaseModel):
    symbol: str
    fiscalYear: LenientInt
    period: str
    reportedCurrency: Optional[str] = None
    date: str
    data: Dict[
        str, Any
    ]  # This can be a complex structure, so using Any for flexibility


class FMPAsReportedBalanceSheet(FMPBaseModel):
    symbol: str
    fiscalYear: LenientInt
    period: str
    reportedCurrency: Optional[str] = None
    date: str
    data: Dict[
        str, Any
    ]  # This can be a complex structure, so using Any for flexibility


class FMPAsReportedCashFlowStatement(FMPBaseModel):
    symbol: str
    fiscalYear: LenientInt
    period: str
    reportedCurrency: Optional[str] = None
    date: str
    data: Dict[
        str, Any
    ]  # This can be a complex structure, so using Any for flexibility


class FMPAsReportedFullStatement(FMPBaseModel):
    symbol: str
    fiscalYear: LenientInt
    period: str
    reportedCurrency: Optional[str] = None
    date: str
    data: Dict[
        str, Any
    ]  # This can be a complex structure, so using Any for flexibility


class FMPForm13FFiling(FMPBaseModel):
    cik: str
    name: str
    date: str
    filingDate: str
    acceptedDate: str
    formType: str
    link: str
    finalLink: str


class FMPSECFiling(FMPBaseModel):
    symbol: Optional[str] = None
    cik: str
    filingDate: str
    acceptedDate: str
    formType: str
    link: str
    finalLink: str


class FMPForm13FExtract(FMPBaseModel):
    date: str
    filingDate: str
    acceptedDate: str
    cik: str
    securityCusip: str
    symbol: str
    nameOfIssuer: str
    shares: LenientInt
    titleOfClass: str
    sharesType: str
    putCallShare: str
    value: LenientInt
    link: str
    finalLink: str


class FMPForm13FDate(FMPBaseModel):
    date: str
    year: LenientInt
    quarter: LenientInt


class FMPForm13FAnalytics(FMPBaseModel):
    date: str
    cik: str
    filingDate: str
    investorName: str
    symbol: str
    securityName: str
    typeOfSecurity: str
    securityCusip: str
    sharesType: str
    putCallShare: str
    investmentDiscretion: str
    industryTitle: str
    weight: float
    lastWeight: float
    changeInWeight: float
    changeInWeightPercentage: float
    marketValue: LenientInt
    lastMarketValue: LenientInt
    changeInMarketValue: LenientInt
    changeInMarketValuePercentage: float
    sharesNumber: LenientInt
    lastSharesNumber: LenientInt
    changeInSharesNumber: LenientInt
    changeInSharesNumberPercentage: float
    quarterEndPrice: float
    avgPricePaid: float
    isNew: bool
    isSoldOut: bool
    ownership: float
    lastOwnership: float
    changeInOwnership: float
    changeInOwnershipPercentage: float
    holdingPeriod: LenientInt
    firstAdded: str
    performance: LenientInt
    performancePercentage: float
    lastPerformance: LenientInt
    changeInPerformance: LenientInt
    isCountedForPerformance: bool


class FMPHolderPerformance(FMPBaseModel):
    date: str
    cik: str
    investorName: str
    portfolioSize: LenientInt
    securitiesAdded: LenientInt
    securitiesRemoved: LenientInt
    marketValue: LenientInt
    previousMarketValue: LenientInt
    changeInMarketValue: LenientInt
    changeInMarketValuePercentage: float
    averageHoldingPeriod: LenientInt
    averageHoldingPeriodTop10: LenientInt
    averageHoldingPeriodTop20: LenientInt
    turnover: float
    turnoverAlternateSell: float
    turnoverAlternateBuy: float
    performance: LenientInt
    performancePercentage: float
    lastPerformance: LenientInt
    changeInPerformance: LenientInt
    performance1year: LenientInt
    performancePercentage1year: float
    performance3year: LenientInt
    performancePercentage3year: float
    performance5year: LenientInt
    performancePercentage5year: float
    performanceSinceInception: LenientInt
    performanceSinceInceptionPercentage: float
    performanceRelativeToSP500Percentage: float
    performance1yearRelativeToSP500Percentage: float
    performance3yearRelativeToSP500Percentage: float
    performance5yearRelativeToSP500Percentage: float
    performanceSinceInceptionRelativeToSP500Percentage: float


class FMPHolderIndustryBreakdown(FMPBaseModel):
    date: str
    cik: str
    investorName: str
    industryTitle: str
    weight: float
    lastWeight: float
    changeInWeight: float
    changeInWeightPercentage: float
    performance: LenientInt
    performancePercentage: float
    lastPerformance: LenientInt
    changeInPerformance: LenientInt


class FMPPositionSummary(FMPBaseModel):
    symbol: str
    cik: str
    date: str
    investorsHolding: LenientInt
    lastInvestorsHolding: LenientInt
    investorsHoldingChange: LenientInt
    numberOf13Fshares: LenientInt
    lastNumberOf13Fshares: LenientInt
    numberOf13FsharesChange: LenientInt
    totalInvested: LenientInt
    lastTotalInvested: LenientInt
    totalInvestedChange: LenientInt
    ownershipPercent: float
    lastOwnershipPercent: float
    ownershipPercentChange: float
    newPositions: LenientInt
    lastNewPositions: LenientInt
    newPositionsChange: LenientInt
    increasedPositions: LenientInt
    lastIncreasedPositions: LenientInt
    increasedPositionsChange: LenientInt
    closedPositions: LenientInt
    lastClosedPositions: LenientInt
    closedPositionsChange: LenientInt
    reducedPositions: LenientInt
    lastReducedPositions: LenientInt
    reducedPositionsChange: LenientInt
    totalCalls: LenientInt
    lastTotalCalls: LenientInt
    totalCallsChange: LenientInt
    totalPuts: LenientInt
    lastTotalPuts: LenientInt
    totalPutsChange: LenientInt
    putCallRatio: float
    lastPutCallRatio: float
    putCallRatioChange: float


class FMPIndustryPerformanceSummary(FMPBaseModel):
    industryTitle: str
    industryValue: LenientInt
    date: str


class FMPIndex(FMPBaseModel):
    symbol: str
    name: str
    exchange: Optional[str] = None
    currency: Optional[str] = None


class FMPIndexConstituent(FMPBaseModel):
    symbol: str
    name: str
    sector: str
    subSector: str
    headQuarter: str
    dateFirstAdded: Optional[str] = None
    cik: str
    founded: str


class FMPHistoricalIndexConstituent(FMPBaseModel):
    dateAdded: str
    addedSecurity: Optional[str] = None
    removedTicker: Optional[str] = None
    removedSecurity: Optional[str] = None
    date: str
    symbol: str
    reason: Optional[str] = None


class FMPInsiderTrade(FMPBaseModel):
    symbol: str
    filingDate: str
    transactionDate: str
    reportingCik: str
    companyCik: str
    transactionType: str
    securitiesOwned: float
    reportingName: str
    typeOfOwner: str
    acquisitionOrDisposition: str
    directOrIndirect: Optional[str] = None
    formType: str
    securitiesTransacted: float
    price: float
    securityName: str
    url: str


class FMPInsiderTransactionType(FMPBaseModel):
    transactionType: str


class FMPInsiderTradeStatistics(FMPBaseModel):
    symbol: str
    cik: str
    year: LenientInt
    quarter: LenientInt
    acquiredTransactions: LenientInt
    disposedTransactions: LenientInt
    acquiredDisposedRatio: float
    totalAcquired: float
    totalDisposed: float
    averageAcquired: float
    averageDisposed: float
    totalPurchases: LenientInt
    totalSales: LenientInt


class FMPAcquisitionOwnership(FMPBaseModel):
    cik: str
    symbol: str
    filingDate: str
    acceptedDate: str
    cusip: str
    nameOfReportingPerson: str
    citizenshipOrPlaceOfOrganization: Optional[str] = None
    soleVotingPower: Optional[str] = None
    sharedVotingPower: Optional[str] = None
    soleDispositivePower: Optional[str] = None
    sharedDispositivePower: Optional[str] = None
    amountBeneficiallyOwned: str
    percentOfClass: str
    typeOfReportingPerson: str
    url: str


class FMPNewsArticle(FMPBaseModel):
    symbol: Optional[str] = None
    publishedDate: str
    publisher: Optional[str] = None
    title: Optional[str] = None
    image: Optional[str] = None
    site: Optional[str] = None
    text: Optional[str] = None
    url: Optional[str] = None


class FMPTechnicalIndicator(FMPBaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    sma: Optional[float] = None
    ema: Optional[float] = None
    wma: Optional[float] = None
    dema: Optional[float] = None
    tema: Optional[float] = None
    rsi: Optional[float] = None
    standardDeviation: Optional[float] = None
    williams: Optional[float] = None
    adx: Optional[float] = None


class FMPCommodity(FMPBaseModel):
    symbol: str
    name: str
    exchange: Optional[str] = None
    tradeMonth: Optional[str] = None
    currency: Optional[str] = None


class FmpFinancialStatementSymbolsListResponse(FMPBaseModel):
    symbol: str
    calendarYear: str
    period: str
    date: str
    dateAdded: str


class FmpFinancialReportDatesListResponse(FMPBaseModel):
    date: str
    period: str
    linkCalendarYear: Optional[str] = None
    filedDate: Optional[str] = None


class FMPQuoteFull(FMPBaseModel):
    symbol: str
    name: str
    price: float
    changePercentage: float
    change: float
    volume: Optional[float] = None
    dayLow: float
    dayHigh: float
    yearHigh: float
    yearLow: float
    marketCap: Optional[float] = None
    priceAvg50: float
    priceAvg200: float
    exchange: str
    open: float
    previousClose: float
    timestamp: LenientInt


class FMPQuoteShort(FMPBaseModel):
    symbol: str
    price: float
    change: float
    volume: float


class FMPAftermarketTrade(FMPBaseModel):
    symbol: str
    price: float
    tradeSize: Optional[LenientInt] = None
    timestamp: LenientInt


class FMPAftermarketQuote(FMPBaseModel):
    symbol: str
    bidSize: LenientInt
    bidPrice: float
    askSize: LenientInt
    askPrice: float
    volume: float
    timestamp: LenientInt


class FMPStockPriceChange(FMPBaseModel):
    symbol: str
    _1D: Optional[float] = None
    _5D: Optional[float] = None
    _1M: Optional[float] = None
    _3M: Optional[float] = None
    _6M: Optional[float] = None
    ytd: Optional[float] = None
    _1Y: Optional[float] = None
    _3Y: Optional[float] = None
    _5Y: Optional[float] = None
    _10Y: Optional[float] = None
    max: Optional[float] = None


class FMPBulkEOD(FMPBaseModel):
    symbol: str
    date: str
    open: float
    low: float
    high: float
    close: float
    adjClose: float
    volume: LenientInt


class FMPPoliticalTrade(FMPBaseModel):
    symbol: str
    disclosureDate: str
    transactionDate: str
    firstName: str
    lastName: str
    office: str
    district: str
    owner: str
    assetDescription: str
    assetType: str
    type: str
    amount: str
    capitalGainsOver200USD: Optional[str] = None
    comment: str
    link: str


class FMPCompanySECFilings(FMPBaseModel):
    symbol: Optional[str] = None
    name: str
    cik: str
    sicCode: str
    industryTitle: str
    businessAddress: str
    phoneNumber: Optional[str] = None


class FMPIndustryClassification(FMPBaseModel):
    office: Optional[str] = None
    sicCode: str
    industryTitle: str


class FMPIndustryClassificationSearch(FMPBaseModel):
    symbol: str
    name: str
    cik: str
    sicCode: str
    industryTitle: str
    businessAddress: str
    phoneNumber: str


class FMPEarningsTranscript(FMPBaseModel):
    symbol: str
    period: str
    fiscalYear: LenientInt
    date: str
    content: Optional[str] = None


class FMPEarningsTranscriptBySymbol(FMPBaseModel):
    quarter: str
    fiscalYear: LenientInt
    date: str


class FMPBulkRating(FMPBaseModel):
    symbol: str
    date: str
    rating: str
    ratingRecommendation: str
    ratingDetailsDCFRecommendation: str
    ratingDetailsROERecommendation: str
    ratingDetailsROARecommendation: str
    ratingDetailsDERecommendation: str
    ratingDetailsPERecommendation: str
    ratingDetailsPBRecommendation: str


class FMPBulkDCF(FMPBaseModel):
    symbol: str
    date: str
    discountedCashFlow: float
    dcfPercentDiff: str


class FMPFinancialScores(FMPBaseModel):
    symbol: str
    reportedCurrency: str
    altmanZScore: Optional[float] = None
    piotroskiScore: Optional[LenientInt] = None
    workingCapital: Optional[float] = None
    totalAssets: Optional[float] = None
    retainedEarnings: Optional[float] = None
    ebit: Optional[float] = None
    marketCap: Optional[float] = None
    totalLiabilities: Optional[float] = None
    revenue: Optional[float] = None


class FMPBulkPriceTargetSummary(FMPBaseModel):
    symbol: str
    lastMonth: str
    lastMonthAvgPT: str
    lastMonthAvgPTPercentDif: str
    lastQuarter: str
    lastQuarterAvgPT: str
    lastQuarterAvgPTPercentDif: str
    lastYear: str
    lastYearAvgPT: str
    lastYearAvgPTPercentDif: str
    allTime: str
    allTimeAvgPT: str
    allTimeAvgPTPercentDif: str
    publishers: str


class FMPBulkETFHolder(FMPBaseModel):
    symbol: str
    sharesNumber: str
    asset: str
    weightPercentage: str
    cusip: str
    isin: str
    name: str
    marketValue: str
    updatedAt: str


class FMPBulkUpgradeDowngradeConsensus(FMPBaseModel):
    symbol: str
    strongBuy: str
    buy: str
    hold: str
    sell: str
    strongSell: str
    consensus: str


class FMPBulkStockPeers(FMPBaseModel):
    symbol: str
    peers: str


class FMPBulkEarningsSurprise(FMPBaseModel):
    symbol: str
    date: str
    epsActual: str
    epsEstimated: str
    lastUpdated: str


class FMPBalanceSheetStatement(FMPBaseModel):
    date: str
    symbol: str
    reportedCurrency: str
    cik: str
    filingDate: str
    acceptedDate: str
    fiscalYear: str
    period: str
    cashAndCashEquivalents: float
    shortTermInvestments: float
    cashAndShortTermInvestments: float
    netReceivables: float
    accountsReceivables: float
    inventory: float
    prepaids: float
    otherCurrentAssets: float
    totalCurrentAssets: float
    propertyPlantEquipmentNet: float
    goodwill: float
    intangibleAssets: float
    goodwillAndIntangibleAssets: float
    longTermInvestments: float
    taxAssets: float
    otherNonCurrentAssets: float
    totalNonCurrentAssets: float
    otherAssets: float
    totalAssets: float
    accountPayables: float
    otherPayables: float
    accruedExpenses: float
    shortTermDebt: float
    capitalLeaseObligationsCurrent: Optional[float] = None
    taxPayables: float
    deferredRevenue: float
    otherCurrentLiabilities: float
    totalCurrentLiabilities: float
    longTermDebt: float
    deferredRevenueNonCurrent: float
    deferredTaxLiabilitiesNonCurrent: float
    otherNonCurrentLiabilities: float
    totalNonCurrentLiabilities: float
    otherLiabilities: float
    capitalLeaseObligations: float
    totalLiabilities: float
    treasuryStock: Optional[float] = None
    preferredStock: float
    commonStock: float
    retainedEarnings: float
    accumulatedOtherComprehensiveIncomeLoss: float
    otherTotalStockholdersEquity: float
    totalStockholdersEquity: float
    totalEquity: float
    minorityInterest: float
    totalLiabilitiesAndTotalEquity: float
    totalInvestments: float
    totalDebt: float
    netDebt: float


class FMPBalanceSheetGrowth(FMPBaseModel):
    symbol: str
    date: str
    fiscalYear: str
    period: str
    reportedCurrency: str
    growthCashAndCashEquivalents: float
    growthShortTermInvestments: float
    growthCashAndShortTermInvestments: float
    growthNetReceivables: float
    growthInventory: float
    growthOtherCurrentAssets: float
    growthTotalCurrentAssets: float
    growthPropertyPlantEquipmentNet: float
    growthGoodwill: float
    growthIntangibleAssets: float
    growthGoodwillAndIntangibleAssets: float
    growthLongTermInvestments: float
    growthTaxAssets: float
    growthOtherNonCurrentAssets: float
    growthTotalNonCurrentAssets: float
    growthOtherAssets: float
    growthTotalAssets: float
    growthAccountPayables: float
    growthShortTermDebt: float
    growthTaxPayables: float
    growthDeferredRevenue: float
    growthOtherCurrentLiabilities: float
    growthTotalCurrentLiabilities: float
    growthLongTermDebt: float
    growthDeferredRevenueNonCurrent: float
    growthDeferredTaxLiabilitiesNonCurrent: float
    growthOtherNonCurrentLiabilities: float
    growthTotalNonCurrentLiabilities: float
    growthOtherLiabilities: float
    growthTotalLiabilities: float
    growthPreferredStock: float
    growthCommonStock: float
    growthRetainedEarnings: float
    growthAccumulatedOtherComprehensiveIncomeLoss: float
    growthOthertotalStockholdersEquity: float
    growthTotalStockholdersEquity: float
    growthMinorityInterest: float
    growthTotalEquity: float
    growthTotalLiabilitiesAndStockholdersEquity: float
    growthTotalInvestments: float
    growthTotalDebt: float
    growthNetDebt: float
    growthAccountsReceivables: float
    growthOtherReceivables: float
    growthPrepaids: float
    growthTotalPayables: float
    growthAccruedExpenses: float
    growthCapitalLeaseObligationsCurrent: float
    growthAdditionalPaidInCapital: float
    growthTreasuryStock: float


class FMPCashFlowStatement(FMPBaseModel):
    date: str
    symbol: str
    reportedCurrency: str
    cik: str
    filingDate: str
    acceptedDate: str
    fiscalYear: str
    period: str
    netIncome: LenientInt
    depreciationAndAmortization: LenientInt
    deferredIncomeTax: LenientInt
    stockBasedCompensation: LenientInt
    changeInWorkingCapital: LenientInt
    accountsReceivables: LenientInt
    inventory: LenientInt
    accountsPayables: LenientInt
    otherWorkingCapital: LenientInt
    otherNonCashItems: LenientInt
    netCashProvidedByOperatingActivities: LenientInt
    investmentsInPropertyPlantAndEquipment: LenientInt
    acquisitionsNet: LenientInt
    purchasesOfInvestments: LenientInt
    salesMaturitiesOfInvestments: LenientInt
    otherInvestingActivities: LenientInt
    netCashProvidedByInvestingActivities: LenientInt
    netDebtIssuance: LenientInt
    longTermNetDebtIssuance: LenientInt
    shortTermNetDebtIssuance: LenientInt
    netStockIssuance: Optional[LenientInt] = None
    netCommonStockIssuance: LenientInt
    commonStockIssuance: LenientInt
    commonStockRepurchased: LenientInt
    netPreferredStockIssuance: LenientInt
    netDividendsPaid: LenientInt
    commonDividendsPaid: LenientInt
    preferredDividendsPaid: Optional[LenientInt] = None
    otherFinancingActivities: LenientInt
    netCashProvidedByFinancingActivities: LenientInt
    effectOfForexChangesOnCash: LenientInt
    netChangeInCash: LenientInt
    cashAtEndOfPeriod: LenientInt
    cashAtBeginningOfPeriod: LenientInt
    operatingCashFlow: LenientInt
    capitalExpenditure: LenientInt
    freeCashFlow: LenientInt
    incomeTaxesPaid: LenientInt
    interestPaid: LenientInt


class FMPCashFlowGrowth(FMPBaseModel):
    symbol: str
    date: str
    fiscalYear: str
    period: str
    reportedCurrency: str
    growthNetIncome: float
    growthDepreciationAndAmortization: float
    growthDeferredIncomeTax: float
    growthStockBasedCompensation: float
    growthChangeInWorkingCapital: float
    growthAccountsReceivables: float
    growthInventory: float
    growthAccountsPayables: float
    growthOtherNonCashItems: float
    growthNetCashProvidedByOperatingActivites: float
    growthInvestmentsInPropertyPlantAndEquipment: float
    growthAcquisitionsNet: float
    growthPurchasesOfInvestments: float
    growthSalesMaturitiesOfInvestments: float
    growthOtherInvestingActivites: float
    growthNetCashUsedForInvestingActivites: float
    growthDebtRepayment: float
    growthCommonStockIssued: float
    growthCommonStockRepurchased: float
    growthDividendsPaid: float
    growthOtherFinancingActivites: float
    growthNetCashUsedProvidedByFinancingActivities: float
    growthEffectOfForexChangesOnCash: float
    growthNetChangeInCash: float
    growthCashAtEndOfPeriod: float
    growthCashAtBeginningOfPeriod: float
    growthOperatingCashFlow: float
    growthCapitalExpenditure: float
    growthFreeCashFlow: float
    growthNetDebtIssuance: float
    growthLongTermNetDebtIssuance: float
    growthShortTermNetDebtIssuance: float
    growthNetStockIssuance: float
    growthPreferredDividendsPaid: float
    growthIncomeTaxesPaid: float
    growthInterestPaid: float


class FMPIncomeStatement(FMPBaseModel):
    date: str
    symbol: str
    reportedCurrency: str
    cik: str
    filingDate: str
    acceptedDate: str
    fiscalYear: str
    period: str
    revenue: LenientInt
    costOfRevenue: LenientInt
    grossProfit: LenientInt
    researchAndDevelopmentExpenses: LenientInt
    generalAndAdministrativeExpenses: LenientInt
    sellingAndMarketingExpenses: LenientInt
    sellingGeneralAndAdministrativeExpenses: LenientInt
    otherExpenses: LenientInt
    operatingExpenses: LenientInt
    costAndExpenses: LenientInt
    netInterestIncome: LenientInt
    interestIncome: LenientInt
    interestExpense: LenientInt
    depreciationAndAmortization: LenientInt
    ebitda: LenientInt
    ebit: LenientInt
    nonOperatingIncomeExcludingInterest: LenientInt
    operatingIncome: LenientInt
    totalOtherIncomeExpensesNet: LenientInt
    incomeBeforeTax: LenientInt
    incomeTaxExpense: LenientInt
    netIncomeFromContinuingOperations: LenientInt
    netIncomeFromDiscontinuedOperations: LenientInt
    otherAdjustmentsToNetIncome: Optional[LenientInt] = None
    netIncome: LenientInt
    netIncomeDeductions: LenientInt
    bottomLineNetIncome: LenientInt
    eps: float
    epsDiluted: float
    weightedAverageShsOut: LenientInt
    weightedAverageShsOutDil: LenientInt


class FMPLatestFinancialStatement(FMPBaseModel):
    symbol: str
    calendarYear: LenientInt
    period: str
    date: str
    dateAdded: str


class FMPKeyMetrics(FMPBaseModel):
    symbol: str
    date: str
    fiscalYear: str
    period: str
    reportedCurrency: str
    marketCap: Optional[float] = None
    enterpriseValue: Optional[float] = None
    evToSales: Optional[float] = None
    evToOperatingCashFlow: Optional[float] = None
    evToFreeCashFlow: Optional[float] = None
    evToEBITDA: Optional[float] = None
    netDebtToEBITDA: Optional[float] = None
    currentRatio: Optional[float] = None
    incomeQuality: Optional[float] = None
    grahamNumber: Optional[float] = None
    grahamNetNet: Optional[float] = None
    taxBurden: Optional[float] = None
    interestBurden: Optional[float] = None
    workingCapital: Optional[float] = None
    investedCapital: Optional[float] = None
    returnOnAssets: Optional[float] = None
    operatingReturnOnAssets: Optional[float] = None
    returnOnTangibleAssets: Optional[float] = None
    returnOnEquity: Optional[float] = None
    returnOnInvestedCapital: Optional[float] = None
    returnOnCapitalEmployed: Optional[float] = None
    earningsYield: Optional[float] = None
    freeCashFlowYield: Optional[float] = None
    capexToOperatingCashFlow: Optional[float] = None
    capexToDepreciation: Optional[float] = None
    capexToRevenue: Optional[float] = None
    salesGeneralAndAdministrativeToRevenue: Optional[float] = None
    researchAndDevelopementToRevenue: Optional[float] = None
    stockBasedCompensationToRevenue: Optional[float] = None
    intangiblesToTotalAssets: Optional[float] = None
    averageReceivables: Optional[float] = None
    averagePayables: Optional[float] = None
    averageInventory: Optional[float] = None
    daysOfSalesOutstanding: Optional[float] = None
    daysOfPayablesOutstanding: Optional[float] = None
    daysOfInventoryOutstanding: Optional[float] = None
    operatingCycle: Optional[float] = None
    cashConversionCycle: Optional[float] = None
    freeCashFlowToEquity: Optional[float] = None
    freeCashFlowToFirm: Optional[float] = None
    tangibleAssetValue: Optional[float] = None
    netCurrentAssetValue: Optional[float] = None


class FMPKeyMetricsTTM(FMPBaseModel):
    symbol: str
    marketCap: Optional[float] = None
    enterpriseValueTTM: Optional[float] = None
    evToSalesTTM: Optional[float] = None
    evToOperatingCashFlowTTM: Optional[float] = None
    evToFreeCashFlowTTM: Optional[float] = None
    evToEBITDATTM: Optional[float] = None
    netDebtToEBITDATTM: Optional[float] = None
    currentRatioTTM: Optional[float] = None
    incomeQualityTTM: Optional[float] = None
    grahamNumberTTM: Optional[float] = None
    grahamNetNetTTM: Optional[float] = None
    taxBurdenTTM: Optional[float] = None
    interestBurdenTTM: Optional[float] = None
    workingCapitalTTM: Optional[float] = None
    investedCapitalTTM: Optional[float] = None
    returnOnAssetsTTM: Optional[float] = None
    operatingReturnOnAssetsTTM: Optional[float] = None
    returnOnTangibleAssetsTTM: Optional[float] = None
    returnOnEquityTTM: Optional[float] = None
    returnOnInvestedCapitalTTM: Optional[float] = None
    returnOnCapitalEmployedTTM: Optional[float] = None
    earningsYieldTTM: Optional[float] = None
    freeCashFlowYieldTTM: Optional[float] = None
    capexToOperatingCashFlowTTM: Optional[float] = None
    capexToDepreciationTTM: Optional[float] = None
    capexToRevenueTTM: Optional[float] = None
    salesGeneralAndAdministrativeToRevenueTTM: Optional[float] = None
    researchAndDevelopementToRevenueTTM: Optional[float] = None
    stockBasedCompensationToRevenueTTM: Optional[float] = None
    intangiblesToTotalAssetsTTM: Optional[float] = None
    averageReceivablesTTM: Optional[float] = None
    averagePayablesTTM: Optional[float] = None
    averageInventoryTTM: Optional[float] = None
    daysOfSalesOutstandingTTM: Optional[float] = None
    daysOfPayablesOutstandingTTM: Optional[float] = None
    daysOfInventoryOutstandingTTM: Optional[float] = None
    operatingCycleTTM: Optional[float] = None
    cashConversionCycleTTM: Optional[float] = None
    freeCashFlowToEquityTTM: Optional[float] = None
    freeCashFlowToFirmTTM: Optional[float] = None
    tangibleAssetValueTTM: Optional[float] = None
    netCurrentAssetValueTTM: Optional[float] = None


class FMPFinancialRatios(FMPBaseModel):
    symbol: str
    date: str
    fiscalYear: str
    period: str
    reportedCurrency: str
    grossProfitMargin: Optional[float] = None
    ebitMargin: Optional[float] = None
    ebitdaMargin: Optional[float] = None
    operatingProfitMargin: Optional[float] = None
    pretaxProfitMargin: Optional[float] = None
    continuousOperationsProfitMargin: Optional[float] = None
    netProfitMargin: Optional[float] = None
    bottomLineProfitMargin: Optional[float] = None
    receivablesTurnover: Optional[float] = None
    payablesTurnover: Optional[float] = None
    inventoryTurnover: Optional[float] = None
    fixedAssetTurnover: Optional[float] = None
    assetTurnover: Optional[float] = None
    currentRatio: Optional[float] = None
    quickRatio: Optional[float] = None
    solvencyRatio: Optional[float] = None
    cashRatio: Optional[float] = None
    priceToEarningsRatio: Optional[float] = None
    priceToEarningsGrowthRatio: Optional[float] = None
    forwardPriceToEarningsGrowthRatio: Optional[float] = None
    priceToBookRatio: Optional[float] = None
    priceToSalesRatio: Optional[float] = None
    priceToFreeCashFlowRatio: Optional[float] = None
    priceToOperatingCashFlowRatio: Optional[float] = None
    debtToAssetsRatio: Optional[float] = None
    debtToEquityRatio: Optional[float] = None
    debtToCapitalRatio: Optional[float] = None
    longTermDebtToCapitalRatio: Optional[float] = None
    financialLeverageRatio: Optional[float] = None
    workingCapitalTurnoverRatio: Optional[float] = None
    operatingCashFlowRatio: Optional[float] = None
    operatingCashFlowSalesRatio: Optional[float] = None
    freeCashFlowOperatingCashFlowRatio: Optional[float] = None
    debtServiceCoverageRatio: Optional[float] = None
    interestCoverageRatio: Optional[float] = None
    shortTermOperatingCashFlowCoverageRatio: Optional[float] = None
    operatingCashFlowCoverageRatio: Optional[float] = None
    capitalExpenditureCoverageRatio: Optional[float] = None
    dividendPaidAndCapexCoverageRatio: Optional[float] = None
    dividendPayoutRatio: Optional[float] = None
    dividendYield: Optional[float] = None
    dividendYieldPercentage: Optional[float] = None
    revenuePerShare: Optional[float] = None
    netIncomePerShare: Optional[float] = None
    interestDebtPerShare: Optional[float] = None
    cashPerShare: Optional[float] = None
    bookValuePerShare: Optional[float] = None
    tangibleBookValuePerShare: Optional[float] = None
    shareholdersEquityPerShare: Optional[float] = None
    operatingCashFlowPerShare: Optional[float] = None
    capexPerShare: Optional[float] = None
    freeCashFlowPerShare: Optional[float] = None
    netIncomePerEBT: Optional[float] = None
    ebtPerEbit: Optional[float] = None
    priceToFairValue: Optional[float] = None
    debtToMarketCap: Optional[float] = None
    effectiveTaxRate: Optional[float] = None
    enterpriseValueMultiple: Optional[float] = None
    dividendPerShare: Optional[float] = None


class FMPFinancialRatiosTTM(FMPBaseModel):
    symbol: str
    grossProfitMarginTTM: Optional[float] = None
    ebitMarginTTM: Optional[float] = None
    ebitdaMarginTTM: Optional[float] = None
    operatingProfitMarginTTM: Optional[float] = None
    pretaxProfitMarginTTM: Optional[float] = None
    continuousOperationsProfitMarginTTM: Optional[float] = None
    netProfitMarginTTM: Optional[float] = None
    bottomLineProfitMarginTTM: Optional[float] = None
    receivablesTurnoverTTM: Optional[float] = None
    payablesTurnoverTTM: Optional[float] = None
    inventoryTurnoverTTM: Optional[float] = None
    fixedAssetTurnoverTTM: Optional[float] = None
    assetTurnoverTTM: Optional[float] = None
    currentRatioTTM: Optional[float] = None
    quickRatioTTM: Optional[float] = None
    solvencyRatioTTM: Optional[float] = None
    cashRatioTTM: Optional[float] = None
    priceToEarningsRatioTTM: Optional[float] = None
    priceToEarningsGrowthRatioTTM: Optional[float] = None
    forwardPriceToEarningsGrowthRatioTTM: Optional[float] = None
    priceToBookRatioTTM: Optional[float] = None
    priceToSalesRatioTTM: Optional[float] = None
    priceToFreeCashFlowRatioTTM: Optional[float] = None
    priceToOperatingCashFlowRatioTTM: Optional[float] = None
    debtToAssetsRatioTTM: Optional[float] = None
    debtToEquityRatioTTM: Optional[float] = None
    debtToCapitalRatioTTM: Optional[float] = None
    longTermDebtToCapitalRatioTTM: Optional[float] = None
    financialLeverageRatioTTM: Optional[float] = None
    workingCapitalTurnoverRatioTTM: Optional[float] = None
    operatingCashFlowRatioTTM: Optional[float] = None
    operatingCashFlowSalesRatioTTM: Optional[float] = None
    freeCashFlowOperatingCashFlowRatioTTM: Optional[float] = None
    debtServiceCoverageRatioTTM: Optional[float] = None
    interestCoverageRatioTTM: Optional[float] = None
    shortTermOperatingCashFlowCoverageRatioTTM: Optional[float] = None
    operatingCashFlowCoverageRatioTTM: Optional[float] = None
    capitalExpenditureCoverageRatioTTM: Optional[float] = None
    dividendPaidAndCapexCoverageRatioTTM: Optional[float] = None
    dividendPayoutRatioTTM: Optional[float] = None
    dividendYieldTTM: Optional[float] = None
    revenuePerShareTTM: Optional[float] = None
    netIncomePerShareTTM: Optional[float] = None
    interestDebtPerShareTTM: Optional[float] = None
    cashPerShareTTM: Optional[float] = None
    bookValuePerShareTTM: Optional[float] = None
    tangibleBookValuePerShareTTM: Optional[float] = None
    shareholdersEquityPerShareTTM: Optional[float] = None
    operatingCashFlowPerShareTTM: Optional[float] = None
    capexPerShareTTM: Optional[float] = None
    freeCashFlowPerShareTTM: Optional[float] = None
    netIncomePerEBTTTM: Optional[float] = None
    ebtPerEbitTTM: Optional[float] = None
    priceToFairValueTTM: Optional[float] = None
    debtToMarketCapTTM: Optional[float] = None
    effectiveTaxRateTTM: Optional[float] = None
    enterpriseValueMultipleTTM: Optional[float] = None


class FMPIncomeStatementGrowth(FMPBaseModel):
    symbol: str
    date: str
    fiscalYear: str
    period: str
    reportedCurrency: str
    revenueGrowth: Optional[float] = None
    grossProfitGrowth: Optional[float] = None
    ebitgrowth: Optional[float] = None
    operatingIncomeGrowth: Optional[float] = None
    netIncomeGrowth: Optional[float] = None
    epsgrowth: Optional[float] = None
    epsdilutedGrowth: Optional[float] = None
    weightedAverageSharesGrowth: Optional[float] = None
    weightedAverageSharesDilutedGrowth: Optional[float] = None
    dividendsPerShareGrowth: Optional[float] = None
    operatingCashFlowGrowth: Optional[float] = None
    receivablesGrowth: Optional[float] = None
    inventoryGrowth: Optional[float] = None
    assetGrowth: Optional[float] = None
    bookValueperShareGrowth: Optional[float] = None
    debtGrowth: Optional[float] = None
    rdexpenseGrowth: Optional[float] = None
    sgaexpensesGrowth: Optional[float] = None
    freeCashFlowGrowth: Optional[float] = None
    tenYRevenueGrowthPerShare: Optional[float] = None
    fiveYRevenueGrowthPerShare: Optional[float] = None
    threeYRevenueGrowthPerShare: Optional[float] = None
    tenYOperatingCFGrowthPerShare: Optional[float] = None
    fiveYOperatingCFGrowthPerShare: Optional[float] = None
    threeYOperatingCFGrowthPerShare: Optional[float] = None
    tenYNetIncomeGrowthPerShare: Optional[float] = None
    fiveYNetIncomeGrowthPerShare: Optional[float] = None
    threeYNetIncomeGrowthPerShare: Optional[float] = None
    tenYShareholdersEquityGrowthPerShare: Optional[float] = None
    fiveYShareholdersEquityGrowthPerShare: Optional[float] = None
    threeYShareholdersEquityGrowthPerShare: Optional[float] = None
    tenYDividendperShareGrowthPerShare: Optional[float] = None
    fiveYDividendperShareGrowthPerShare: Optional[float] = None
    threeYDividendperShareGrowthPerShare: Optional[float] = None
    ebitdaGrowth: Optional[float] = None
    growthCapitalExpenditure: Optional[float] = None
    tenYBottomLineNetIncomeGrowthPerShare: Optional[float] = None
    fiveYBottomLineNetIncomeGrowthPerShare: Optional[float] = None
    threeYBottomLineNetIncomeGrowthPerShare: Optional[float] = None


# Market Performance Models
class FMPSectorPerformanceSnapshot(FMPBaseModel):
    sector: str
    date: str
    exchange: str
    changesPercentage: float = Field(alias="averageChange")


class FMPIndustryPerformanceSnapshot(FMPBaseModel):
    industry: str
    date: str
    exchange: str
    averageChange: float
    changesPercentage: Optional[float] = None
    marketCap: Optional[float] = None
    numberOfSymbols: Optional[LenientInt] = None


class FMPHistoricalSectorPerformance(FMPBaseModel):
    date: str
    sector: str
    changesPercentage: Optional[float] = None


class FMPHistoricalIndustryPerformance(FMPBaseModel):
    date: str
    industry: str
    changesPercentage: float


class FMPSectorPESnapshot(FMPBaseModel):
    sector: str
    date: str
    exchange: str
    pe: float
    marketCap: Optional[LenientInt] = None


class FMPIndustryPESnapshot(FMPBaseModel):
    date: str
    industry: str
    exchange: str
    pe: float
    marketCap: Optional[float] = None


class FMPHistoricalSectorPE(FMPBaseModel):
    date: str
    sector: str
    pe: float
    marketCap: Optional[LenientInt] = None


class FMPHistoricalIndustryPE(FMPBaseModel):
    date: str
    industry: str
    pe: float
    marketCap: LenientInt


class FMPMarketMover(FMPBaseModel):
    symbol: str
    name: str
    change: float
    price: float
    changesPercentage: float


class Error(FMPBaseModel):
    error: str
    details: str


# Market Hours Models
class FMPExchangeMarketHours(FMPBaseModel):
    exchange: str
    name: str
    openingHour: str
    closingHour: str
    timezone: str
    isMarketOpen: bool


class FMPExchangeHoliday(FMPBaseModel):
    date: str
    name: str
    exchange: Optional[str] = None


class FMPOwnerEarnings(FMPBaseModel):
    symbol: str
    reportedCurrency: str
    fiscalYear: str
    period: str
    date: str
    averagePPE: float
    maintenanceCapex: float
    ownersEarnings: float
    growthCapex: float
    ownersEarningsPerShare: float


class FMPEnterpriseValue(FMPBaseModel):
    symbol: str
    date: str
    stockPrice: float
    numberOfShares: LenientInt
    marketCapitalization: LenientInt
    minusCashAndCashEquivalents: LenientInt
    addTotalDebt: LenientInt
    enterpriseValue: LenientInt


class FMPTrendingSentiment(FMPBaseModel):
    symbol: str
    name: str
    rank: LenientInt
    sentiment: float
    lastSentiment: float


class FMPHistoricalSentiment(FMPBaseModel):
    date: str
    symbol: str
    stocktwitsPosts: LenientInt
    twitterPosts: LenientInt
    stocktwitsComments: LenientInt
    twitterComments: LenientInt
    stocktwitsLikes: LenientInt
    twitterLikes: LenientInt
    stocktwitsImpressions: LenientInt
    twitterImpressions: LenientInt
    stocktwitsSentiment: float
    twitterSentiment: float

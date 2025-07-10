import os
import sys
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, RootModel

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


class FMPSymbolSearch(BaseModel):
    symbol: str
    name: str
    currency: str
    exchangeFullName: Optional[str] = None
    exchange: Optional[str] = None


class FMPCompanyNameSearch(BaseModel):
    symbol: str
    name: str
    currency: str
    exchangeFullName: Optional[str] = None
    exchange: Optional[str] = None


class FMPCompanyCIKSearch(BaseModel):
    symbol: str
    companyName: str
    cik: str
    exchangeFullName: str
    exchange: str
    currency: str


class FMPCusipSearch(BaseModel):
    symbol: str
    companyName: str
    cusip: str
    marketCap: int


class FMPIsinSearch(BaseModel):
    symbol: str
    name: str
    isin: str
    marketCap: float


class FMPStockScreenerResult(BaseModel):
    symbol: str
    companyName: str
    marketCap: int
    sector: Optional[str] = None
    industry: Optional[str] = None
    beta: Optional[float] = None
    price: float
    lastAnnualDividend: float
    volume: int
    exchange: str
    exchangeShortName: str
    country: Optional[str] = None
    isEtf: bool
    isFund: bool
    isActivelyTrading: bool


class FMPCompanyProfile(BaseModel):
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


class FMPSymbolAndCompanyNameList(BaseModel):
    symbol: str
    companyName: Optional[str] = None


class FMPSymbolAndNameList(BaseModel):
    symbol: str
    name: Optional[str] = None


class FMPFinancialStatementSymbolList(BaseModel):
    symbol: str
    companyName: str
    tradingCurrency: str
    reportingCurrency: Optional[str] = None


class FMPSymbolAndCIKList(BaseModel):
    cik: str
    companyName: str


class FMPSymbolChange(BaseModel):
    date: str
    companyName: str
    oldSymbol: str
    newSymbol: str


class FMPEarningsTranscriptList(BaseModel):
    symbol: str
    companyName: str
    noOfTranscripts: str


class FMPExchangeInfo(BaseModel):
    exchange: str
    name: str
    countryName: str
    countryCode: str
    symbolSuffix: str
    isMarketOpen: Optional[bool] = None
    delay: Optional[str] = None


class FMPSector(BaseModel):
    sector: str


class FMPIndustry(BaseModel):
    industry: str


class FMPCountry(BaseModel):
    country: str

    @property
    def name(self) -> str:
        """Alias for country field to match expected interface."""
        return self.country


class FMPAnalystEstimates(BaseModel):
    symbol: str
    date: str
    revenueLow: int
    revenueHigh: int
    revenueAvg: int
    ebitdaLow: int
    ebitdaHigh: int
    ebitdaAvg: int
    ebitLow: int
    ebitHigh: int
    ebitAvg: int
    netIncomeLow: int
    netIncomeHigh: int
    netIncomeAvg: int
    sgaExpenseLow: int
    sgaExpenseHigh: int
    sgaExpenseAvg: int
    epsAvg: float
    epsHigh: float
    epsLow: float
    numAnalystsRevenue: int
    numAnalystsEps: int


class FMPRatingSnapshot(BaseModel):
    symbol: str
    rating: str
    overallScore: int
    discountedCashFlowScore: int
    returnOnEquityScore: int
    returnOnAssetsScore: int
    debtToEquityScore: int
    priceToEarningsScore: int
    priceToBookScore: int


class FMPPriceTargetSummary(BaseModel):
    symbol: str
    lastMonthCount: int
    lastMonthAvgPriceTarget: float
    lastQuarterCount: int
    lastQuarterAvgPriceTarget: float
    lastYearCount: int
    lastYearAvgPriceTarget: float
    allTimeCount: int
    allTimeAvgPriceTarget: float
    publishers: str


class FMPPriceTargetConsensus(BaseModel):
    symbol: str
    targetHigh: int
    targetLow: int
    targetConsensus: float
    targetMedian: float


class FMPPriceTargetNews(BaseModel):
    symbol: str
    publishedDate: str
    newsURL: str
    newsTitle: str
    analystName: str
    priceTarget: float
    adjPriceTarget: float
    priceWhenPosted: float
    newsPublisher: str
    newsBaseURL: str
    analystCompany: str


class FMPStockGrade(BaseModel):
    symbol: str
    date: str
    gradingCompany: str
    previousGrade: str
    newGrade: str
    action: str


class FMPHistoricalStockGrade(BaseModel):
    symbol: str
    date: str
    analystRatingsStrongBuy: int
    analystRatingsBuy: int
    analystRatingsHold: int
    analystRatingsSell: int
    analystRatingsStrongSell: int


class FMPStockGradeSummary(BaseModel):
    symbol: str
    strongBuy: int
    buy: int
    hold: int
    sell: int
    strongSell: int
    consensus: str


class FMPStockGradeNews(BaseModel):
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


class FMPDividend(BaseModel):
    symbol: str
    date: str
    recordDate: str
    paymentDate: str
    declarationDate: str
    adjDividend: float
    dividend: float
    yield_: Optional[float] = None
    frequency: str


class FMPDividendCalendarEvent(BaseModel):
    symbol: str
    date: str
    recordDate: str
    paymentDate: str
    declarationDate: str
    adjDividend: float
    dividend: float
    yield_: Optional[float] = None
    frequency: str


class FMPEarningsReport(BaseModel):
    symbol: str
    date: str
    epsActual: Optional[float] = None
    epsEstimated: Optional[float] = None
    revenueActual: Optional[float] = None
    revenueEstimated: Optional[float] = None
    lastUpdated: str


class FMPEarningsCalendarEvent(BaseModel):
    symbol: str
    date: str
    epsActual: Optional[float] = None
    epsEstimated: Optional[float] = None
    revenueActual: Optional[float] = None
    revenueEstimated: Optional[float] = None
    lastUpdated: str


class FMPUpcomingIPO(BaseModel):
    symbol: str
    date: str
    daa: str
    company: str
    exchange: str
    actions: str
    shares: Optional[int] = None
    priceRange: Optional[str] = None
    marketCap: Optional[int] = None


class FMPDisclosureFiling(BaseModel):
    symbol: str
    filingDate: str
    acceptedDate: str
    effectivenessDate: str
    cik: str
    form: str
    url: str


class FMPProspectusFiling(BaseModel):
    symbol: str
    acceptedDate: str
    filingDate: str
    ipoDate: str
    cik: str
    pricePublicPerShare: float
    pricePublicTotal: float
    discountsAndCommissionsPerShare: float
    discountsAndCommissionsTotal: float
    proceedsBeforeExpensesPerShare: float
    proceedsBeforeExpensesTotal: float
    form: str
    url: str


class FMPStockSplit(BaseModel):
    symbol: str
    date: str
    numerator: float
    denominator: float


class FMPHistoricalDataPointLight(BaseModel):
    symbol: str
    date: str
    price: float
    volume: int


class FMPHistoricalDataPointFull(BaseModel):
    symbol: str
    date: str
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None
    volume: Optional[int] = None
    change: Optional[float] = None
    changePercent: Optional[float] = None
    vwap: Optional[float] = None


class FMPIntradayDataPoint(BaseModel):
    date: str
    open: float
    low: float
    high: float
    close: float
    volume: int


class FMPCompanyNote(BaseModel):
    cik: str
    symbol: str
    title: str
    exchange: str


class FMPStockPeer(BaseModel):
    symbol: str
    companyName: str
    price: float
    mktCap: int


class FMPDelistedCompany(BaseModel):
    symbol: str
    companyName: str
    exchange: str
    ipoDate: str
    delistedDate: str


class FMPEmployeeCount(BaseModel):
    symbol: str
    cik: str
    acceptanceTime: str
    periodOfReport: str
    companyName: str
    formType: str
    filingDate: str
    employeeCount: int
    source: str


class FMPHistoricalEmployeeCount(BaseModel):
    symbol: str
    cik: str
    acceptanceTime: str
    periodOfReport: str
    companyName: str
    formType: str
    filingDate: str
    employeeCount: int
    source: str


class FMPMarketCap(BaseModel):
    symbol: str
    date: str
    marketCap: int


class FMPShareFloat(BaseModel):
    symbol: str
    date: Optional[str] = None
    freeFloat: float
    floatShares: int
    outstandingShares: int


class FMPMergerAcquisition(BaseModel):
    symbol: str
    companyName: str
    cik: str
    targetedCompanyName: str
    targetedCik: Optional[str] = None
    targetedSymbol: Optional[str] = None
    transactionDate: str
    acceptedDate: str
    link: str


class FMPExecutiveProfile(BaseModel):
    title: str
    name: str
    pay: Optional[float] = None
    currencyPay: str
    gender: str
    yearBorn: Optional[int] = None
    active: Optional[int] = None


class FMPExecutiveCompensation(BaseModel):
    cik: str
    symbol: str
    companyName: str
    filingDate: str
    acceptedDate: str
    nameAndPosition: str
    year: int
    salary: Optional[int] = None
    bonus: Optional[int] = None
    stockAward: Optional[int] = None
    optionAward: Optional[int] = None
    incentivePlanCompensation: Optional[int] = None
    allOtherCompensation: Optional[int] = None
    total: Optional[int] = None
    link: str


class FMPExecutiveCompensationBenchmark(BaseModel):
    industryTitle: str
    year: int
    averageCompensation: float


class FMPCommitmentOfTradersReport(BaseModel):
    symbol: str
    date: str
    name: str
    sector: str
    marketAndExchangeNames: str
    cftcContractMarketCode: str
    cftcMarketCode: str
    cftcRegionCode: str
    cftcCommodityCode: str
    openInterestAll: int
    noncommPositionsLongAll: int
    noncommPositionsShortAll: int
    noncommPositionsSpreadAll: int
    commPositionsLongAll: int
    commPositionsShortAll: int
    totReptPositionsLongAll: int
    totReptPositionsShortAll: int
    nonreptPositionsLongAll: int
    nonreptPositionsShortAll: int
    openInterestOld: int
    noncommPositionsLongOld: int
    noncommPositionsShortOld: int
    noncommPositionsSpreadOld: int
    commPositionsLongOld: int
    commPositionsShortOld: int
    totReptPositionsLongOld: int
    totReptPositionsShortOld: int
    nonreptPositionsLongOld: int
    nonreptPositionsShortOld: int
    openInterestOther: int
    noncommPositionsLongOther: int
    noncommPositionsShortOther: int
    noncommPositionsSpreadOther: int
    commPositionsLongOther: int
    commPositionsShortOther: int
    totReptPositionsLongOther: int
    totReptPositionsShortOther: int
    nonreptPositionsLongOther: int
    nonreptPositionsShortOther: int
    changeInOpenInterestAll: int
    changeInNoncommLongAll: int
    changeInNoncommShortAll: int
    changeInNoncommSpeadAll: int
    changeInCommLongAll: int
    changeInCommShortAll: int
    changeInTotReptLongAll: int
    changeInTotReptShortAll: int
    changeInNonreptLongAll: int
    changeInNonreptShortAll: int
    pctOfOpenInterestAll: int
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
    tradersTotAll: int
    tradersNoncommLongAll: int
    tradersNoncommShortAll: int
    tradersNoncommSpreadAll: int
    tradersCommLongAll: int
    tradersCommShortAll: int
    tradersTotReptLongAll: int
    tradersTotReptShortAll: int
    tradersTotOl: int
    tradersNoncommLongOl: int
    tradersNoncommShortOl: int
    tradersNoncommSpeadOl: int
    tradersCommLongOl: int
    tradersCommShortOl: int
    tradersTotReptLongOl: int
    tradersTotReptShortOl: int
    tradersTotOther: int
    tradersNoncommLongOther: int
    tradersNoncommShortOther: int
    tradersNoncommSpreadOther: int
    tradersCommLongOther: int
    tradersCommShortOther: int
    tradersTotReptLongOther: int
    tradersTotReptShortOther: int
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


class FMPCommitmentOfTradersAnalysis(BaseModel):
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
    netPostion: int
    previousNetPosition: int
    changeInNetPosition: float
    marketSentiment: str
    reversalTrend: bool


class FMPDcfValuation(BaseModel):
    symbol: str
    date: str
    dcf: float
    Stock_Price: float = Field(alias="Stock Price")


class FMPDCFCustomValuation(BaseModel):
    year: str
    symbol: str
    revenue: int
    revenuePercentage: float
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
    capitalExpenditurePercentage: float
    price: float
    beta: float
    dilutedSharesOutstanding: int
    costofDebt: float
    taxRate: float
    afterTaxCostOfDebt: float
    riskFreeRate: float
    marketRiskPremium: float
    costOfEquity: float
    totalDebt: int
    totalEquity: int
    totalCapital: int
    debtWeighting: float
    equityWeighting: float
    wacc: float
    taxRateCash: Optional[int] = None
    ebiat: Optional[float] = None
    ufcf: Optional[int] = None
    sumPvUfcf: Optional[int] = None
    longTermGrowthRate: float
    terminalValue: int
    presentTerminalValue: int
    enterpriseValue: int
    netDebt: int
    equityValue: int
    equityValuePerShare: float
    freeCashFlowT1: int


class FMPTreasuryRates(BaseModel):
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


class FMPEconomicIndicator(BaseModel):
    name: str
    date: str
    value: float


class FMPEconomicCalendarEvent(BaseModel):
    date: str
    country: str
    event: str
    currency: str
    previous: Optional[float] = None
    estimate: Optional[float] = None
    actual: Optional[float] = None
    change: Optional[float] = None
    impact: str
    changePercentage: Optional[float] = None
    unit: Optional[str] = None


class FMPMarketRiskPremium(BaseModel):
    country: str
    continent: str
    countryRiskPremium: float
    totalEquityRiskPremium: float


class FMPESGFiling(BaseModel):
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


class FMPESGRating(BaseModel):
    symbol: str
    cik: str
    companyName: str
    industry: str
    fiscalYear: int
    ESGRiskRating: str
    industryRank: str


class FMPESGBenchmark(BaseModel):
    fiscalYear: int
    sector: str
    environmentalScore: float
    socialScore: float
    governanceScore: float
    ESGScore: float


class FMPFundHolding(BaseModel):
    symbol: str
    asset: str
    name: str
    isin: str
    securityCusip: str
    sharesNumber: int
    weightPercentage: float
    marketValue: float
    updatedAt: str
    updated: str


class FMPFundInfoSectorsListItem(BaseModel):
    industry: str
    exposure: float


class FMPCommodityListItem(BaseModel):
    symbol: str
    name: str
    exchange: Optional[str] = None
    tradeMonth: str
    currency: Optional[str] = None


class FMPCryptocurrencyListItem(BaseModel):
    symbol: str
    name: str
    exchange: str
    icoDate: Optional[str] = None
    circulatingSupply: Optional[float] = None
    totalSupply: Optional[float] = None


class FMPIndexListItem(BaseModel):
    symbol: str
    name: str
    exchange: str
    currency: str


class FMPFundInfo(BaseModel):
    symbol: str
    name: str
    description: str
    isin: str
    assetClass: str
    securityCusip: str
    domicile: str
    website: str
    etfCompany: str
    expenseRatio: float
    assetsUnderManagement: int
    avgVolume: int
    inceptionDate: str
    nav: float
    navCurrency: str
    holdingsCount: int
    updatedAt: str
    sectorsList: List[FMPFundInfoSectorsListItem]


class FMPFundCountryAllocation(BaseModel):
    country: str
    weightPercentage: str


class FMPFundAssetExposure(BaseModel):
    symbol: str
    asset: str
    sharesNumber: int
    weightPercentage: float
    marketValue: int


class FMPFundSectorWeighting(BaseModel):
    symbol: str
    sector: str
    weightPercentage: float


class FMPFundHolder(BaseModel):
    cik: str
    holder: str
    shares: int
    dateReported: str
    change: int
    weightPercent: float


class FMPFundDisclosure(BaseModel):
    cik: str
    date: str
    acceptedDate: str
    symbol: str
    name: str
    lei: str
    title: str
    cusip: str
    isin: str
    balance: int
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


class FMPFundDisclosureNameSearch(BaseModel):
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


class FMPFundDisclosureDate(BaseModel):
    date: str
    year: int
    quarter: int


class FMPCrowdfundingCampaign(BaseModel):
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
    numberOfSecurityOffered: int
    offeringPrice: float
    offeringAmount: float
    overSubscriptionAccepted: str
    overSubscriptionAllocationType: Optional[str] = None
    maximumOfferingAmount: Optional[float] = None
    offeringDeadlineDate: Optional[str] = None
    currentNumberOfEmployees: int
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


class FMPCrowdfundingSearch(BaseModel):
    cik: str
    name: str
    date: Optional[str] = None


class FMPEquityOffering(BaseModel):
    cik: str
    companyName: str
    date: str
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
    relatedPersonFirstName: str
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
    isAmendment: bool
    dateOfFirstSale: str
    durationOfOfferingIsMoreThanYear: bool
    securitiesOfferedAreOfEquityType: Optional[bool] = None
    isBusinessCombinationTransaction: bool
    minimumInvestmentAccepted: int
    totalOfferingAmount: int
    totalAmountSold: int
    totalAmountRemaining: int
    hasNonAccreditedInvestors: bool
    totalNumberAlreadyInvested: int
    salesCommissions: int
    findersFees: int
    grossProceedsUsed: int


class FMPEquityOfferingSearch(BaseModel):
    cik: str
    name: str
    date: str


class FMPForexPair(BaseModel):
    symbol: str
    fromCurrency: str
    toCurrency: str
    fromName: str
    toName: str


class FMPFinancialReportDate(BaseModel):
    symbol: str
    fiscalYear: int
    period: str
    linkJson: str
    linkXlsx: str


# Root model for each dictionary item in a section
class FinancialSectionEntry(RootModel[Dict[str, List[Union[str, float, int, None]]]]):
    pass


# Root model for a section (which is a list of entries)
class FinancialSection(RootModel[List[FinancialSectionEntry]]):
    pass


class FMPFullFinancialReport(BaseModel):
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


class FMPRevenueSegmentation(BaseModel):
    symbol: str
    fiscalYear: int
    period: str
    reportedCurrency: Optional[str] = None
    date: str
    data: Optional[Dict[str, int]] = None


class FMPAsReportedIncomeStatement(BaseModel):
    symbol: str
    fiscalYear: int
    period: str
    reportedCurrency: Optional[str] = None
    date: str
    data: Dict[
        str, Any
    ]  # This can be a complex structure, so using Any for flexibility


class FMPAsReportedBalanceSheet(BaseModel):
    symbol: str
    fiscalYear: int
    period: str
    reportedCurrency: Optional[str] = None
    date: str
    data: Dict[
        str, Any
    ]  # This can be a complex structure, so using Any for flexibility


class FMPAsReportedCashFlowStatement(BaseModel):
    symbol: str
    fiscalYear: int
    period: str
    reportedCurrency: Optional[str] = None
    date: str
    data: Dict[
        str, Any
    ]  # This can be a complex structure, so using Any for flexibility


class FMPAsReportedFullStatement(BaseModel):
    symbol: str
    fiscalYear: int
    period: str
    reportedCurrency: Optional[str] = None
    date: str
    data: Dict[
        str, Any
    ]  # This can be a complex structure, so using Any for flexibility


class FMPForm13FFiling(BaseModel):
    cik: str
    name: str
    date: str
    filingDate: str
    acceptedDate: str
    formType: str
    link: str
    finalLink: str


class FMPForm13FExtract(BaseModel):
    date: str
    filingDate: str
    acceptedDate: str
    cik: str
    securityCusip: str
    symbol: str
    nameOfIssuer: str
    shares: int
    titleOfClass: str
    sharesType: str
    putCallShare: str
    value: int
    link: str
    finalLink: str


class FMPForm13FDate(BaseModel):
    date: str
    year: int
    quarter: int


class FMPForm13FAnalytics(BaseModel):
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
    marketValue: int
    lastMarketValue: int
    changeInMarketValue: int
    changeInMarketValuePercentage: float
    sharesNumber: int
    lastSharesNumber: int
    changeInSharesNumber: int
    changeInSharesNumberPercentage: float
    quarterEndPrice: float
    avgPricePaid: float
    isNew: bool
    isSoldOut: bool
    ownership: float
    lastOwnership: float
    changeInOwnership: float
    changeInOwnershipPercentage: float
    holdingPeriod: int
    firstAdded: str
    performance: int
    performancePercentage: float
    lastPerformance: int
    changeInPerformance: int
    isCountedForPerformance: bool


class FMPHolderPerformance(BaseModel):
    date: str
    cik: str
    investorName: str
    portfolioSize: int
    securitiesAdded: int
    securitiesRemoved: int
    marketValue: int
    previousMarketValue: int
    changeInMarketValue: int
    changeInMarketValuePercentage: float
    averageHoldingPeriod: int
    averageHoldingPeriodTop10: int
    averageHoldingPeriodTop20: int
    turnover: float
    turnoverAlternateSell: float
    turnoverAlternateBuy: float
    performance: int
    performancePercentage: float
    lastPerformance: int
    changeInPerformance: int
    performance1year: int
    performancePercentage1year: float
    performance3year: int
    performancePercentage3year: float
    performance5year: int
    performancePercentage5year: float
    performanceSinceInception: int
    performanceSinceInceptionPercentage: float
    performanceRelativeToSP500Percentage: float
    performance1yearRelativeToSP500Percentage: float
    performance3yearRelativeToSP500Percentage: float
    performance5yearRelativeToSP500Percentage: float
    performanceSinceInceptionRelativeToSP500Percentage: float


class FMPHolderIndustryBreakdown(BaseModel):
    date: str
    cik: str
    investorName: str
    industryTitle: str
    weight: float
    lastWeight: float
    changeInWeight: float
    changeInWeightPercentage: float
    performance: int
    performancePercentage: float
    lastPerformance: int
    changeInPerformance: int


class FMPPositionSummary(BaseModel):
    symbol: str
    cik: str
    date: str
    investorsHolding: int
    lastInvestorsHolding: int
    investorsHoldingChange: int
    numberOf13Fshares: int
    lastNumberOf13Fshares: int
    numberOf13FsharesChange: int
    totalInvested: int
    lastTotalInvested: int
    totalInvestedChange: int
    ownershipPercent: float
    lastOwnershipPercent: float
    ownershipPercentChange: float
    newPositions: int
    lastNewPositions: int
    newPositionsChange: int
    increasedPositions: int
    lastIncreasedPositions: int
    increasedPositionsChange: int
    closedPositions: int
    lastClosedPositions: int
    closedPositionsChange: int
    reducedPositions: int
    lastReducedPositions: int
    reducedPositionsChange: int
    totalCalls: int
    lastTotalCalls: int
    totalCallsChange: int
    totalPuts: int
    lastTotalPuts: int
    totalPutsChange: int
    putCallRatio: float
    lastPutCallRatio: float
    putCallRatioChange: float


class FMPIndustryPerformanceSummary(BaseModel):
    industryTitle: str
    industryValue: int
    date: str


class FMPIndex(BaseModel):
    symbol: str
    name: str
    exchange: Optional[str] = None
    currency: Optional[str] = None


class FMPIndexConstituent(BaseModel):
    symbol: str
    name: str
    sector: str
    subSector: str
    headQuarter: str
    dateFirstAdded: Optional[str] = None
    cik: str
    founded: str


class FMPHistoricalIndexConstituent(BaseModel):
    dateAdded: str
    addedSecurity: str
    removedTicker: Optional[str] = None
    removedSecurity: Optional[str] = None
    date: str
    symbol: str
    reason: Optional[str] = None


class FMPInsiderTrade(BaseModel):
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


class FMPInsiderTransactionType(BaseModel):
    transactionType: str


class FMPInsiderTradeStatistics(BaseModel):
    symbol: str
    cik: str
    year: int
    quarter: int
    acquiredTransactions: int
    disposedTransactions: int
    acquiredDisposedRatio: float
    totalAcquired: float
    totalDisposed: float
    averageAcquired: float
    averageDisposed: float
    totalPurchases: int
    totalSales: int


class FMPAcquisitionOwnership(BaseModel):
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


class FMPNewsArticle(BaseModel):
    symbol: Optional[str] = None
    publishedDate: str
    publisher: Optional[str] = None
    title: Optional[str] = None
    image: Optional[str] = None
    site: Optional[str] = None
    text: Optional[str] = None
    url: Optional[str] = None


class FMPTechnicalIndicator(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: int
    sma: Optional[float] = None
    ema: Optional[float] = None
    wma: Optional[float] = None
    dema: Optional[float] = None
    tema: Optional[float] = None
    rsi: Optional[float] = None
    standardDeviation: Optional[float] = None
    williams: Optional[float] = None
    adx: Optional[float] = None


class FMPCommodity(BaseModel):
    symbol: str
    name: str
    exchange: Optional[str] = None
    tradeMonth: Optional[str] = None
    currency: Optional[str] = None


class FmpFinancialStatementSymbolsListResponse(BaseModel):
    symbol: str
    calendarYear: str
    period: str
    date: str
    dateAdded: str


class FmpFinancialReportDatesListResponse(BaseModel):
    date: str
    period: str
    linkCalendarYear: Optional[str] = None
    filedDate: Optional[str] = None


class FMPQuoteFull(BaseModel):
    symbol: str
    name: str
    price: float
    changePercentage: float
    change: float
    volume: Optional[int] = None
    dayLow: float
    dayHigh: float
    yearHigh: float
    yearLow: float
    marketCap: Optional[int] = None
    priceAvg50: float
    priceAvg200: float
    exchange: str
    open: float
    previousClose: float
    timestamp: int


class FMPQuoteShort(BaseModel):
    symbol: str
    price: float
    change: float
    volume: int


class FMPAftermarketTrade(BaseModel):
    symbol: str
    price: float
    tradeSize: Optional[int] = None
    timestamp: int


class FMPAftermarketQuote(BaseModel):
    symbol: str
    bidSize: int
    bidPrice: float
    askSize: int
    askPrice: float
    volume: int
    timestamp: int


class FMPStockPriceChange(BaseModel):
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


class FMPBulkEOD(BaseModel):
    symbol: str
    date: str
    open: float
    low: float
    high: float
    close: float
    adjClose: float
    volume: int


class FMPPoliticalTrade(BaseModel):
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


class FMPCompanySECFilings(BaseModel):
    symbol: str
    name: str
    cik: str
    sicCode: str
    industryTitle: str
    businessAddress: str
    phoneNumber: Optional[str] = None


class FMPIndustryClassification(BaseModel):
    office: Optional[str] = None
    sicCode: str
    industryTitle: str


class FMPIndustryClassificationSearch(BaseModel):
    symbol: str
    name: str
    cik: str
    sicCode: str
    industryTitle: str
    businessAddress: str
    phoneNumber: str


class FMPEarningsTranscript(BaseModel):
    symbol: str
    period: str
    fiscalYear: int
    date: str
    content: Optional[str] = None


class FMPEarningsTranscriptBySymbol(BaseModel):
    quarter: str
    fiscalYear: int
    date: str


class FMPBulkRating(BaseModel):
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


class FMPBulkDCF(BaseModel):
    symbol: str
    date: str
    discountedCashFlow: float
    dcfPercentDiff: str


class FMPFinancialScores(BaseModel):
    symbol: str
    reportedCurrency: str
    altmanZScore: float
    piotroskiScore: int
    workingCapital: float
    totalAssets: float
    retainedEarnings: float
    ebit: float
    marketCap: float
    totalLiabilities: float
    revenue: float


class FMPBulkPriceTargetSummary(BaseModel):
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


class FMPBulkETFHolder(BaseModel):
    symbol: str
    sharesNumber: str
    asset: str
    weightPercentage: str
    cusip: str
    isin: str
    name: str
    marketValue: str
    updatedAt: str


class FMPBulkUpgradeDowngradeConsensus(BaseModel):
    symbol: str
    strongBuy: str
    buy: str
    hold: str
    sell: str
    strongSell: str
    consensus: str


class FMPBulkStockPeers(BaseModel):
    symbol: str
    peers: str


class FMPBulkEarningsSurprise(BaseModel):
    symbol: str
    date: str
    epsActual: str
    epsEstimated: str
    lastUpdated: str


class FMPBalanceSheetStatement(BaseModel):
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
    capitalLeaseObligationsCurrent: float
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
    treasuryStock: float
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


class FMPBalanceSheetGrowth(BaseModel):
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


class FMPCashFlowStatement(BaseModel):
    date: str
    symbol: str
    reportedCurrency: str
    cik: str
    filingDate: str
    acceptedDate: str
    fiscalYear: str
    period: str
    netIncome: int
    depreciationAndAmortization: int
    deferredIncomeTax: int
    stockBasedCompensation: int
    changeInWorkingCapital: int
    accountsReceivables: int
    inventory: int
    accountsPayables: int
    otherWorkingCapital: int
    otherNonCashItems: int
    netCashProvidedByOperatingActivities: int
    investmentsInPropertyPlantAndEquipment: int
    acquisitionsNet: int
    purchasesOfInvestments: int
    salesMaturitiesOfInvestments: int
    otherInvestingActivities: int
    netCashProvidedByInvestingActivities: int
    netDebtIssuance: int
    longTermNetDebtIssuance: int
    shortTermNetDebtIssuance: int
    netStockIssuance: int
    netCommonStockIssuance: int
    commonStockIssuance: int
    commonStockRepurchased: int
    netPreferredStockIssuance: int
    netDividendsPaid: int
    commonDividendsPaid: int
    preferredDividendsPaid: int
    otherFinancingActivities: int
    netCashProvidedByFinancingActivities: int
    effectOfForexChangesOnCash: int
    netChangeInCash: int
    cashAtEndOfPeriod: int
    cashAtBeginningOfPeriod: int
    operatingCashFlow: int
    capitalExpenditure: int
    freeCashFlow: int
    incomeTaxesPaid: int
    interestPaid: int


class FMPCashFlowGrowth(BaseModel):
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


class FMPIncomeStatement(BaseModel):
    date: str
    symbol: str
    reportedCurrency: str
    cik: str
    filingDate: str
    acceptedDate: str
    fiscalYear: str
    period: str
    revenue: int
    costOfRevenue: int
    grossProfit: int
    researchAndDevelopmentExpenses: int
    generalAndAdministrativeExpenses: int
    sellingAndMarketingExpenses: int
    sellingGeneralAndAdministrativeExpenses: int
    otherExpenses: int
    operatingExpenses: int
    costAndExpenses: int
    netInterestIncome: int
    interestIncome: int
    interestExpense: int
    depreciationAndAmortization: int
    ebitda: int
    ebit: int
    nonOperatingIncomeExcludingInterest: int
    operatingIncome: int
    totalOtherIncomeExpensesNet: int
    incomeBeforeTax: int
    incomeTaxExpense: int
    netIncomeFromContinuingOperations: int
    netIncomeFromDiscontinuedOperations: int
    otherAdjustmentsToNetIncome: int
    netIncome: int
    netIncomeDeductions: int
    bottomLineNetIncome: int
    eps: float
    epsDiluted: float
    weightedAverageShsOut: int
    weightedAverageShsOutDil: int


class FMPLatestFinancialStatement(BaseModel):
    symbol: str
    calendarYear: int
    period: str
    date: str
    dateAdded: str


class FMPKeyMetrics(BaseModel):
    symbol: str
    date: str
    fiscalYear: str
    period: str
    reportedCurrency: str
    marketCap: Optional[float] = None
    enterpriseValue: Optional[float] = None
    evToSales: float
    evToOperatingCashFlow: float
    evToFreeCashFlow: float
    evToEBITDA: float
    netDebtToEBITDA: float
    currentRatio: float
    incomeQuality: float
    grahamNumber: float
    grahamNetNet: float
    taxBurden: float
    interestBurden: float
    workingCapital: int
    investedCapital: int
    returnOnAssets: float
    operatingReturnOnAssets: float
    returnOnTangibleAssets: float
    returnOnEquity: float
    returnOnInvestedCapital: float
    returnOnCapitalEmployed: float
    earningsYield: float
    freeCashFlowYield: float
    capexToOperatingCashFlow: float
    capexToDepreciation: float
    capexToRevenue: float
    salesGeneralAndAdministrativeToRevenue: Optional[float] = None
    researchAndDevelopementToRevenue: float
    stockBasedCompensationToRevenue: float
    intangiblesToTotalAssets: Optional[float] = None
    averageReceivables: float
    averagePayables: float
    averageInventory: int
    daysOfSalesOutstanding: float
    daysOfPayablesOutstanding: float
    daysOfInventoryOutstanding: float
    operatingCycle: float
    cashConversionCycle: float
    freeCashFlowToEquity: int
    freeCashFlowToFirm: float
    tangibleAssetValue: int
    netCurrentAssetValue: int


class FMPKeyMetricsTTM(BaseModel):
    symbol: str
    marketCap: Optional[float] = None
    enterpriseValueTTM: Optional[float] = None
    evToSalesTTM: float
    evToOperatingCashFlowTTM: float
    evToFreeCashFlowTTM: float
    evToEBITDATTM: float
    netDebtToEBITDATTM: float
    currentRatioTTM: float
    incomeQualityTTM: float
    grahamNumberTTM: float
    grahamNetNetTTM: float
    taxBurdenTTM: float
    interestBurdenTTM: float
    workingCapitalTTM: int
    investedCapitalTTM: int
    returnOnAssetsTTM: float
    operatingReturnOnAssetsTTM: float
    returnOnTangibleAssetsTTM: float
    returnOnEquityTTM: float
    returnOnInvestedCapitalTTM: float
    returnOnCapitalEmployedTTM: float
    earningsYieldTTM: float
    freeCashFlowYieldTTM: float
    capexToOperatingCashFlowTTM: float
    capexToDepreciationTTM: float
    capexToRevenueTTM: float
    salesGeneralAndAdministrativeToRevenueTTM: Optional[float] = None
    researchAndDevelopementToRevenueTTM: float
    stockBasedCompensationToRevenueTTM: float
    intangiblesToTotalAssetsTTM: Optional[float] = None
    averageReceivablesTTM: float
    averagePayablesTTM: float
    averageInventoryTTM: int
    daysOfSalesOutstandingTTM: float
    daysOfPayablesOutstandingTTM: float
    daysOfInventoryOutstandingTTM: float
    operatingCycleTTM: float
    cashConversionCycleTTM: float
    freeCashFlowToEquityTTM: int
    freeCashFlowToFirmTTM: float
    tangibleAssetValueTTM: int
    netCurrentAssetValueTTM: int


class FMPFinancialRatios(BaseModel):
    symbol: str
    date: str
    fiscalYear: str
    period: str
    reportedCurrency: str
    grossProfitMargin: float
    ebitMargin: float
    ebitdaMargin: float
    operatingProfitMargin: float
    pretaxProfitMargin: float
    continuousOperationsProfitMargin: float
    netProfitMargin: float
    bottomLineProfitMargin: float
    receivablesTurnover: float
    payablesTurnover: float
    inventoryTurnover: float
    fixedAssetTurnover: float
    assetTurnover: float
    currentRatio: float
    quickRatio: float
    solvencyRatio: float
    cashRatio: float
    priceToEarningsRatio: float
    priceToEarningsGrowthRatio: float
    forwardPriceToEarningsGrowthRatio: float
    priceToBookRatio: float
    priceToSalesRatio: float
    priceToFreeCashFlowRatio: float
    priceToOperatingCashFlowRatio: float
    debtToAssetsRatio: float
    debtToEquityRatio: float
    debtToCapitalRatio: float
    longTermDebtToCapitalRatio: float
    financialLeverageRatio: float
    workingCapitalTurnoverRatio: float
    operatingCashFlowRatio: float
    operatingCashFlowSalesRatio: float
    freeCashFlowOperatingCashFlowRatio: float
    debtServiceCoverageRatio: float
    interestCoverageRatio: float
    shortTermOperatingCashFlowCoverageRatio: float
    operatingCashFlowCoverageRatio: float
    capitalExpenditureCoverageRatio: float
    dividendPaidAndCapexCoverageRatio: float
    dividendPayoutRatio: float
    dividendYield: float
    dividendYieldPercentage: float
    revenuePerShare: float
    netIncomePerShare: float
    interestDebtPerShare: float
    cashPerShare: float
    bookValuePerShare: float
    tangibleBookValuePerShare: float
    shareholdersEquityPerShare: float
    operatingCashFlowPerShare: float
    capexPerShare: float
    freeCashFlowPerShare: float
    netIncomePerEBT: float
    ebtPerEbit: float
    priceToFairValue: float
    debtToMarketCap: float
    effectiveTaxRate: float
    enterpriseValueMultiple: float
    dividendPerShare: float


class FMPFinancialRatiosTTM(BaseModel):
    symbol: str
    grossProfitMarginTTM: float
    ebitMarginTTM: float
    ebitdaMarginTTM: float
    operatingProfitMarginTTM: float
    pretaxProfitMarginTTM: float
    continuousOperationsProfitMarginTTM: float
    netProfitMarginTTM: float
    bottomLineProfitMarginTTM: float
    receivablesTurnoverTTM: float
    payablesTurnoverTTM: float
    inventoryTurnoverTTM: float
    fixedAssetTurnoverTTM: float
    assetTurnoverTTM: float
    currentRatioTTM: float
    quickRatioTTM: float
    solvencyRatioTTM: float
    cashRatioTTM: float
    priceToEarningsRatioTTM: float
    priceToEarningsGrowthRatioTTM: float
    forwardPriceToEarningsGrowthRatioTTM: float
    priceToBookRatioTTM: float
    priceToSalesRatioTTM: float
    priceToFreeCashFlowRatioTTM: float
    priceToOperatingCashFlowRatioTTM: float
    debtToAssetsRatioTTM: float
    debtToEquityRatioTTM: float
    debtToCapitalRatioTTM: float
    longTermDebtToCapitalRatioTTM: float
    financialLeverageRatioTTM: float
    workingCapitalTurnoverRatioTTM: float
    operatingCashFlowRatioTTM: float
    operatingCashFlowSalesRatioTTM: float
    freeCashFlowOperatingCashFlowRatioTTM: float
    debtServiceCoverageRatioTTM: float
    interestCoverageRatioTTM: float
    shortTermOperatingCashFlowCoverageRatioTTM: float
    operatingCashFlowCoverageRatioTTM: float
    capitalExpenditureCoverageRatioTTM: float
    dividendPaidAndCapexCoverageRatioTTM: float
    dividendPayoutRatioTTM: float
    dividendYieldTTM: float
    revenuePerShareTTM: float
    netIncomePerShareTTM: float
    interestDebtPerShareTTM: float
    cashPerShareTTM: float
    bookValuePerShareTTM: float
    tangibleBookValuePerShareTTM: float
    shareholdersEquityPerShareTTM: float
    operatingCashFlowPerShareTTM: float
    capexPerShareTTM: float
    freeCashFlowPerShareTTM: float
    netIncomePerEBTTTM: float
    ebtPerEbitTTM: float
    priceToFairValueTTM: float
    debtToMarketCapTTM: float
    effectiveTaxRateTTM: float
    enterpriseValueMultipleTTM: float


class FMPIncomeStatementGrowth(BaseModel):
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
class FMPSectorPerformanceSnapshot(BaseModel):
    sector: str
    date: str
    exchange: str
    changesPercentage: float = Field(alias="averageChange")


class FMPIndustryPerformanceSnapshot(BaseModel):
    industry: str
    date: str
    exchange: str
    averageChange: float
    changesPercentage: Optional[float] = None
    marketCap: Optional[float] = None
    numberOfSymbols: Optional[int] = None


class FMPHistoricalSectorPerformance(BaseModel):
    date: str
    sector: str
    changesPercentage: Optional[float] = None


class FMPHistoricalIndustryPerformance(BaseModel):
    date: str
    industry: str
    changesPercentage: float


class FMPSectorPESnapshot(BaseModel):
    sector: str
    date: str
    exchange: str
    pe: float
    marketCap: Optional[int] = None


class FMPIndustryPESnapshot(BaseModel):
    date: str
    industry: str
    exchange: str
    pe: float
    marketCap: Optional[float] = None


class FMPHistoricalSectorPE(BaseModel):
    date: str
    sector: str
    pe: float
    marketCap: Optional[int] = None


class FMPHistoricalIndustryPE(BaseModel):
    date: str
    industry: str
    pe: float
    marketCap: int


class FMPMarketMover(BaseModel):
    symbol: str
    name: str
    change: float
    price: float
    changesPercentage: float


class Error(BaseModel):
    error: str
    details: str


# Market Hours Models
class FMPExchangeMarketHours(BaseModel):
    exchange: str
    name: str
    openingHour: str
    closingHour: str
    timezone: str
    isMarketOpen: bool


class FMPExchangeHoliday(BaseModel):
    date: str
    name: str
    exchange: Optional[str] = None


class FMPOwnerEarnings(BaseModel):
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


class FMPEnterpriseValue(BaseModel):
    symbol: str
    date: str
    stockPrice: float
    numberOfShares: int
    marketCapitalization: int
    minusCashAndCashEquivalents: int
    addTotalDebt: int
    enterpriseValue: int


class FMPTrendingSentiment(BaseModel):
    symbol: str
    name: str
    rank: int
    sentiment: float
    lastSentiment: float


class FMPHistoricalSentiment(BaseModel):
    date: str
    symbol: str
    stocktwitsPosts: int
    twitterPosts: int
    stocktwitsComments: int
    twitterComments: int
    stocktwitsLikes: int
    twitterLikes: int
    stocktwitsImpressions: int
    twitterImpressions: int
    stocktwitsSentiment: float
    twitterSentiment: float

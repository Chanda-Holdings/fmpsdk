import os
import sys
from typing import Any, List, Optional

from pydantic import BaseModel, RootModel

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


class FMPSymbolSearch(BaseModel):
    symbol: str
    name: str
    currency: str
    exchangeFullName: str
    exchange: str

class FMPCompanyNameSearch(BaseModel):
    symbol: str
    name: str
    currency: str
    exchangeFullName: str
    exchange: str

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
    marketCap: int

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
    volAvg: Optional[int] = None
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
    companyName: str

class FMPSymbolAndNameList(BaseModel):
    symbol: str
    name: str

class FMPFinancialStatementSymbolList(BaseModel):
    symbol: str
    companyName: str
    tradingCurrency: str
    reportingCurrency: str

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
    delay: Optional[str] = None

class FMPSector(BaseModel):
    sector: str

class FMPIndustry(BaseModel):
    industry: str

class FMPCountry(BaseModel):
    country: str

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

class FMPHistoricalRating(BaseModel):
    symbol: str
    date: str
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
    targetMedian: int

class FMPPriceTargetNews(BaseModel):
    symbol: str
    publishedDate: str
    newsURL: str
    newsTitle: str
    analystName: str
    priceTarget: int
    adjPriceTarget: int
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
    previousGrade: str
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
    pricePublicTotal: int
    discountsAndCommissionsPerShare: float
    discountsAndCommissionsTotal: int
    proceedsBeforeExpensesPerShare: float
    proceedsBeforeExpensesTotal: int
    form: str
    url: str

class FMPStockSplit(BaseModel):
    symbol: str
    date: str
    numerator: int
    denominator: int

class FMPStockSplitCalendarEvent(BaseModel):
    symbol: str
    date: str
    numerator: int
    denominator: int

class FMPHistoricalDataPointLight(BaseModel):
    symbol: str
    date: str
    price: float
    volume: int

class FMPHistoricalDataPointFull(BaseModel):
    symbol: str
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: int
    change: float
    changePercent: float
    vwap: float

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

class FMPHistoricalMarketCap(BaseModel):
    symbol: str
    date: str
    marketCap: int

class FMPShareFloat(BaseModel):
    symbol: str
    date: str
    freeFloat: float
    floatShares: int
    outstandingShares: int
    source: str

class FMPAllShareFloat(BaseModel):
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
    targetedCik: str
    targetedSymbol: str
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
    active: Optional[bool] = None

class FMPExecutiveCompensation(BaseModel):
    cik: str
    symbol: str
    companyName: str
    filingDate: str
    acceptedDate: str
    nameAndPosition: str
    year: int
    salary: int
    bonus: int
    stockAward: int
    optionAward: int
    incentivePlanCompensation: int
    allOtherCompensation: int
    total: int
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
    pctOfOpenInterestOl: int
    pctOfOiNoncommLongOl: float
    pctOfOiNoncommShortOl: float
    pctOfOiNoncommSpreadOl: float
    pctOfOiCommLongOl: float
    pctOfOiCommShortOl: float
    pctOfOiTotReptLongOl: float
    pctOfOiTotReptShortOl: float
    pctOfOiNonreptLongOl: float
    pctOfOiNonreptShortOl: float
    pctOfOpenInterestOther: int
    pctOfOiNoncommLongOther: int
    pctOfOiNoncommShortOther: int
    pctOfOiNoncommSpreadOther: int
    pctOfOiCommLongOther: int
    pctOfOiCommShortOther: int
    pctOfOiTotReptLongOther: int
    pctOfOiTotReptShortOther: int
    pctOfOiNonreptLongOther: int
    pctOfOiNonreptShortOther: int
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
    concGrossLe4TdrLongOther: int
    concGrossLe4TdrShortOther: int
    concGrossLe8TdrLongOther: int
    concGrossLe8TdrShortOther: int
    concNetLe4TdrLongOther: int
    concNetLe4TdrShortOther: int
    concNetLe8TdrLongOther: int
    concNetLe8TdrShortOther: int
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
    Stock_Price: float

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
    previous: Optional[str] = None
    estimate: Optional[str] = None
    actual: Optional[str] = None
    change: Optional[str] = None
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
    companyName: str
    date: Optional[str] = None
    filingDate: str
    acceptedDate: str
    formType: str
    formSignification: str
    nameOfIssuer: str
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
    date: str

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

class FMPFullFinancialReport(BaseModel):
    symbol: str
    period: str
    year: str
    Cover_Page: List[Any]
    Auditor_Information: List[Any]
    CONSOLIDATED_STATEMENTS_OF_OPER: List[Any]
    CONSOLIDATED_STATEMENTS_OF_COMP: List[Any]
    CONSOLIDATED_BALANCE_SHEETS: List[Any]
    CONSOLIDATED_BALANCE_SHEETS_Pa: List[Any]
    CONSOLIDATED_STATEMENTS_OF_SHAR: List[Any]
    CONSOLIDATED_STATEMENTS_OF_CASH: List[Any]
    Summary_of_Significant_Accounti: List[Any]
    Revenue: List[Any]
    Financial_Instruments: List[Any]
    Consolidated_Financial_Statemen: List[Any]
    Income_Taxes: List[Any]
    Leases: List[Any]
    Debt: List[Any]
    Shareholders_Equity: List[Any]
    Benefit_Plans: List[Any]
    Commitments_and_Contingencies: List[Any]
    Segment_Information_and_Geograp: List[Any]
    Summary_of_Significant_Accoun_2: List[Any]
    Summary_of_Significant_Accoun_3: List[Any]
    Revenue__Tables_: List[Any]
    Revenue___Additional_Informatio: List[Any]
    Revenue___Deferred_Revenue__Exp: List[Any]
    Financial_Instruments___Cash__C: List[Any]
    Financial_Instruments___Non_Cur: List[Any]
    Financial_Instruments___Additio: List[Any]
    Financial_Instruments___Notiona: List[Any]
    Financial_Instruments___Gross_F: List[Any]
    Financial_Instruments___Derivat: List[Any]
    Consolidated_Financial_Statem_2: List[Any]
    Consolidated_Financial_Statem_3: List[Any]
    Consolidated_Financial_Statem_4: List[Any]
    Income_Taxes__Tables_: List[Any]
    Income_Taxes___Reconciliation_o: List[Any]
    Income_Taxes___Significant_Comp: List[Any]
    Income_Taxes___Aggregate_Change: List[Any]
    Leases__Tables_: List[Any]
    Leases___ROU_Assets_and_Lease_L: List[Any]
    Leases___Lease_Liability_Maturi: List[Any]
    Debt__Tables_: List[Any]
    Debt___Summary_of_Cash_Flows_As: List[Any]
    Debt___Summary_of_Term_Debt__De: List[Any]
    Debt___Future_Principal_Payment: List[Any]
    Shareholders_Equity__Tables_: List[Any]
    Shareholders_Equity___Shares_o: List[Any]
    Benefit_Plans__Tables_: List[Any]
    Benefit_Plans___Restricted_Stoc: List[Any]
    Benefit_Plans___Summary_of_Shar: List[Any]
    Commitments_and_Contingencies__: List[Any]
    Segment_Information_and_Geogr_2: List[Any]
    Segment_Information_and_Geogr_3: List[Any]
    Segment_Information_and_Geogr_4: List[Any]
    Summary_of_Significant_Accoun_4: List[Any]
    Summary_of_Significant_Accoun_5: List[Any]

class FMPRevenueSegmentationData(BaseModel):
    Mac: int
    Service: int
    Wearables__Home_and_Accessories: int
    iPad: int
    iPhone: int

class FMPRevenueSegmentation(BaseModel):
    symbol: str
    fiscalYear: int
    period: str
    reportedCurrency: Optional[str] = None
    date: str
    data: FMPRevenueSegmentationData

class FMPAsReportedIncomeStatementData(BaseModel):
    revenuefromcontractwithcustomerexcludingassessedtax: int
    costofgoodsandservicessold: int
    grossprofit: int
    researchanddevelopmentexpense: int
    sellinggeneralandadministrativeexpense: int
    operatingexpenses: int
    operatingincomeloss: int
    nonoperatingincomeexpense: int
    incomelossfromcontinuingoperationsbeforeincometaxesextraordinaryitemsnoncontrollinginterest: int
    incometaxexpensebenefit: int
    netincomeloss: int
    earningspersharebasic: float
    earningspersharediluted: float
    weightedaveragenumberofsharesoutstandingbasic: int
    weightedaveragenumberofdilutedsharesoutstanding: int
    othercomprehensiveincomelossforeigncurrencytransactionandtranslationadjustmentnetoftax: int
    othercomprehensiveincomelossderivativeinstrumentgainlossbeforereclassificationaftertax: int
    othercomprehensiveincomelossderivativeinstrumentgainlossreclassificationaftertax: int
    othercomprehensiveincomelossderivativeinstrumentgainlossafterreclassificationandtax: int
    othercomprehensiveincomeunrealizedholdinggainlossonsecuritiesarisingduringperiodnetoftax: int
    othercomprehensiveincomelossreclassificationadjustmentfromaociforsaleofsecuritiesnetoftax: int
    othercomprehensiveincomelossavailableforsalesecuritiesadjustmentnetoftax: int
    othercomprehensiveincomelossnetoftaxportionattributabletoparent: int
    comprehensiveincomenetoftax: int

class FMPAsReportedIncomeStatement(BaseModel):
    symbol: str
    fiscalYear: int
    period: str
    reportedCurrency: Optional[str] = None
    date: str
    data: FMPAsReportedIncomeStatementData

class FMPAsReportedBalanceSheetData(BaseModel):
    cashandcashequivalentsatcarryingvalue: int
    marketablesecuritiescurrent: int
    accountsreceivablenetcurrent: int
    nontradereceivablescurrent: int
    inventorynet: int
    otherassetscurrent: int
    assetscurrent: int
    marketablesecuritiesnoncurrent: int
    propertyplantandequipmentnet: int
    otherassetsnoncurrent: int
    assetsnoncurrent: int
    assets: int
    accountspayablecurrent: int
    otherliabilitiescurrent: int
    contractwithcustomerliabilitycurrent: int
    commercialpaper: int
    longtermdebtcurrent: int
    liabilitiescurrent: int
    longtermdebtnoncurrent: int
    otherliabilitiesnoncurrent: int
    liabilitiesnoncurrent: int
    liabilities: int
    commonstocksharesoutstanding: int
    commonstocksharesissued: int
    commonstocksincludingadditionalpaidincapital: int
    retainedearningsaccumulateddeficit: int
    accumulatedothercomprehensiveincomelossnetoftax: int
    stockholdersequity: int
    liabilitiesandstockholdersequity: int
    commonstockparorstatedvaluepershare: float
    commonstocksharesauthorized: int

class FMPAsReportedBalanceSheet(BaseModel):
    symbol: str
    fiscalYear: int
    period: str
    reportedCurrency: Optional[str] = None
    date: str
    data: FMPAsReportedBalanceSheetData

class FMPAsReportedCashFlowStatementData(BaseModel):
    cashcashequivalentsrestrictedcashandrestrictedcashequivalents: int
    netincomeloss: int
    depreciationdepletionandamortization: int
    sharebasedcompensation: int
    othernoncashincomeexpense: int
    increasedecreaseinaccountsreceivable: int
    increasedecreaseinotherreceivables: int
    increasedecreaseininventories: int
    increasedecreaseinotheroperatingassets: int
    increasedecreaseinaccountspayable: int
    increasedecreaseinotheroperatingliabilities: int
    netcashprovidedbyusedinoperatingactivities: int
    paymentstoacquireavailableforsalesecuritiesdebt: int
    proceedsfrommaturitiesprepaymentsandcallsofavailableforsalesecurities: int
    proceedsfromsaleofavailableforsalesecuritiesdebt: int
    paymentstoacquirepropertyplantandequipment: int
    paymentsforproceedsfromotherinvestingactivities: int
    netcashprovidedbyusedininvestingactivities: int
    paymentsrelatedtotaxwithholdingforsharebasedcompensation: int
    paymentsofdividends: int
    paymentsforrepurchaseofcommonstock: int
    repaymentsoflongtermdebt: int
    proceedsfromrepaymentsofcommercialpaper: int
    proceedsfrompaymentsforotherfinancingactivities: int
    netcashprovidedbyusedinfinancingactivities: int
    cashcashequivalentsrestrictedcashandrestrictedcashequivalentsperiodincreasedecreaseincludingexchangerateeffect: int
    incometaxespaidnet: int

class FMPAsReportedCashFlowStatement(BaseModel):
    symbol: str
    fiscalYear: int
    period: str
    reportedCurrency: Optional[str] = None
    date: str
    data: FMPAsReportedCashFlowStatementData

class FMPAsReportedFullStatementData(BaseModel):
    documenttype: str
    documentannualreport: str
    currentfiscalyearenddate: str
    documentperiodenddate: str
    documenttransitionreport: str
    entityfilenumber: str
    entityregistrantname: str
    entityincorporationstatecountrycode: str
    entitytaxidentificationnumber: str
    entityaddressaddressline1: str
    entityaddresscityortown: str
    entityaddressstateorprovince: str
    entityaddresspostalzipcode: int
    cityareacode: int
    localphonenumber: str
    security12btitle: str
    tradingsymbol: str
    notradingsymbolflag: str
    securityexchangename: str
    entitywellknownseasonedissuer: str
    entityvoluntaryfilers: str
    entitycurrentreportingstatus: str
    entityinteractivedatacurrent: str
    entityfilercategory: str
    entitysmallbusiness: str
    entityemerginggrowthcompany: str
    icfrauditorattestationflag: str
    documentfinstmterrorcorrectionflag: str
    entityshellcompany: str
    amendmentflag: str
    documentfiscalyearfocus: int
    documentfiscalperiodfocus: str
    entitycentralindexkey: int
    auditorname: str
    auditorlocation: str
    auditorfirmid: int
    revenuefromcontractwithcustomerexcludingassessedtax: int
    costofgoodsandservicessold: int
    grossprofit: int
    researchanddevelopmentexpense: int
    sellinggeneralandadministrativeexpense: int
    operatingexpenses: int
    operatingincomeloss: int
    nonoperatingincomeexpense: int
    incomelossfromcontinuingoperationsbeforeincometaxesextraordinaryitemsnoncontrollinginterest: int
    incometaxexpensebenefit: int
    netincomeloss: int
    earningspersharebasic: float
    earningspersharediluted: float
    weightedaveragenumberofsharesoutstandingbasic: int
    weightedaveragenumberofdilutedsharesoutstanding: int
    othercomprehensiveincomelossforeigncurrencytransactionandtranslationadjustmentnetoftax: int
    othercomprehensiveincomelossderivativeinstrumentgainlossbeforereclassificationaftertax: int
    othercomprehensiveincomelossderivativeinstrumentgainlossreclassificationaftertax: int
    othercomprehensiveincomelossderivativeinstrumentgainlossafterreclassificationandtax: int
    othercomprehensiveincomeunrealizedholdinggainlossonsecuritiesarisingduringperiodnetoftax: int
    othercomprehensiveincomelossreclassificationadjustmentfromaociforsaleofsecuritiesnetoftax: int
    othercomprehensiveincomelossavailableforsalesecuritiesadjustmentnetoftax: int
    othercomprehensiveincomelossnetoftaxportionattributabletoparent: int
    comprehensiveincomenetoftax: int
    cashandcashequivalentsatcarryingvalue: int
    marketablesecuritiescurrent: int
    accountsreceivablenetcurrent: int
    nontradereceivablescurrent: int
    inventorynet: int
    otherassetscurrent: int
    assetscurrent: int
    marketablesecuritiesnoncurrent: int
    propertyplantandequipmentnet: int
    otherassetsnoncurrent: int
    assetsnoncurrent: int
    assets: int
    accountspayablecurrent: int
    otherliabilitiescurrent: int
    contractwithcustomerliabilitycurrent: int
    commercialpaper: int
    longtermdebtcurrent: int
    liabilitiescurrent: int
    longtermdebtnoncurrent: int
    otherliabilitiesnoncurrent: int
    liabilitiesnoncurrent: int
    liabilities: int
    commonstocksharesoutstanding: int
    commonstocksharesissued: int
    commonstocksincludingadditionalpaidincapital: int
    retainedearningsaccumulateddeficit: int
    accumulatedothercomprehensiveincomelossnetoftax: int
    stockholdersequity: int
    liabilitiesandstockholdersequity: int
    commonstockparorstatedvaluepershare: float
    commonstocksharesauthorized: int
    stockissuedduringperiodvaluenewissues: int
    adjustmentsrelatedtotaxwithholdingforsharebasedcompensation: int
    adjustmentstoadditionalpaidincapitalsharebasedcompensationrequisiteserviceperiodrecognitionvalue: int
    dividends: int
    stockrepurchasedandretiredduringperiodvalue: int
    commonstockdividendspersharedeclared: float
    cashcashequivalentsrestrictedcashandrestrictedcashequivalents: int
    depreciationdepletionandamortization: int
    sharebasedcompensation: int
    othernoncashincomeexpense: int
    increasedecreaseinaccountsreceivable: int
    increasedecreaseinotherreceivables: int
    increasedecreaseininventories: int
    increasedecreaseinotheroperatingassets: int
    increasedecreaseinaccountspayable: int
    increasedecreaseinotheroperatingliabilities: int
    netcashprovidedbyusedinoperatingactivities: int
    paymentstoacquireavailableforsalesecuritiesdebt: int
    proceedsfrommaturitiesprepaymentsandcallsofavailableforsalesecurities: int
    proceedsfromsaleofavailableforsalesecuritiesdebt: int
    paymentstoacquirepropertyplantandequipment: int
    paymentsforproceedsfromotherinvestingactivities: int
    netcashprovidedbyusedininvestingactivities: int
    paymentsrelatedtotaxwithholdingforsharebasedcompensation: int
    paymentsofdividends: int
    paymentsforrepurchaseofcommonstock: int
    repaymentsoflongtermdebt: int
    proceedsfromrepaymentsofcommercialpaper: int
    proceedsfrompaymentsforotherfinancingactivities: int
    netcashprovidedbyusedinfinancingactivities: int
    cashcashequivalentsrestrictedcashandrestrictedcashequivalentsperiodincreasedecreaseincludingexchangerateeffect: int
    incometaxespaidnet: int
    commercialpapercashflowsummarytabletextblock: str
    contractwithcustomerliabilityrevenuerecognized: int
    contractwithcustomerliability: int
    revenueremainingperformanceobligationpercentage: float
    revenueremainingperformanceobligationexpectedtimingofsatisfactionperiod1: str
    incrementalcommonsharesattributabletosharebasedpaymentarrangements: int
    cash: int
    equitysecuritiesfvnicost: int
    equitysecuritiesfvniaccumulatedgrossunrealizedgainbeforetax: int
    equitysecuritiesfvniaccumulatedgrossunrealizedlossbeforetax: int
    equitysecuritiesfvnicurrentandnoncurrent: int
    availableforsaledebtsecuritiesamortizedcostbasis: int
    availableforsaledebtsecuritiesaccumulatedgrossunrealizedgainbeforetax: int
    availableforsaledebtsecuritiesaccumulatedgrossunrealizedlossbeforetax: int
    availableforsalesecuritiesdebtsecurities: int
    cashcashequivalentsandmarketablesecuritiescost: int
    cashequivalentsandmarketablesecuritiesaccumulatedgrossunrealizedgainbeforetax: int
    cashequivalentsandmarketablesecuritiesaccumulatedgrossunrealizedlossbeforetax: int
    cashcashequivalentsandmarketablesecurities: int
    restrictedcashandcashequivalents: int
    debtsecuritiesavailableforsalerestricted: int
    debtsecuritiesavailableforsalematurityallocatedandsinglematuritydaterollingafteronethroughfiveyearspercentage: float
    debtsecuritiesavailableforsalematurityallocatedandsinglematuritydaterollingafterfivethroughtenyearspercentage: float
    debtsecuritiesavailableforsalematurityallocatedandsinglematuritydaterollingaftertenyearspercentage: float
    maximumlengthoftimeforeigncurrencycashflowhedge: str
    concentrationriskpercentage1: float
    numberofsignificantvendors: int
    derivativenotionalamount: int
    hedgedassetstatementoffinancialpositionextensibleenumeration: str
    hedgedliabilityfairvaluehedge: int
    hedgedliabilitystatementoffinancialpositionextensibleenumeration: str
    propertyplantandequipmentgross: int
    accumulateddepreciationdepletionandamortizationpropertyplantandequipment: int
    depreciation: int
    deferredincometaxassetsnet: int
    otherassetsmiscellaneousnoncurrent: int
    accruedincometaxescurrent: int
    otheraccruedliabilitiescurrent: int
    accruedincometaxesnoncurrent: int
    otheraccruedliabilitiesnoncurrent: int
    totalrestrictedcashcashequivalentsandavailableforsaledebtsecurities: int
    currentforeigntaxexpensebenefit: int
    currentfederaltaxexpensebenefitcontinuingoperations: int
    unrecognizedtaxbenefitsdecreasesresultingfromsettlementswithtaxingauthorities: int
    incomelossfromcontinuingoperationsbeforeincometaxesforeign: int
    effectiveincometaxratereconciliationatfederalstatutoryincometaxrate: float
    deferredtaxassetstaxcreditcarryforwardsforeign: int
    deferredtaxassetstaxcreditcarryforwardsresearch: int
    unrecognizedtaxbenefits: int
    unrecognizedtaxbenefitsthatwouldimpacteffectivetaxrate: int
    decreaseinunrecognizedtaxbenefitsisreasonablypossible: int
    deferredfederalincometaxexpensebenefit: int
    federalincometaxexpensebenefitcontinuingoperations: int
    currentstateandlocaltaxexpensebenefit: int
    deferredstateandlocalincometaxexpensebenefit: int
    stateandlocalincometaxexpensebenefitcontinuingoperations: int
    deferredforeignincometaxexpensebenefit: int
    foreignincometaxexpensebenefitcontinuingoperations: int
    incometaxreconciliationincometaxexpensebenefitatfederalstatutoryincometaxrate: int
    incometaxreconciliationstateandlocalincometaxes: int
    effectiveincometaxratereconciliationimpactofthestateaiddecisionamount: int
    incometaxreconciliationforeignincometaxratedifferential: int
    incometaxreconciliationtaxcreditsresearch: int
    effectiveincometaxratereconciliationsharebasedcompensationexcesstaxbenefitamount: int
    incometaxreconciliationotheradjustments: int
    effectiveincometaxratecontinuingoperations: float
    deferredtaxassetscapitalizedresearchanddevelopment: int
    deferredtaxassetstaxcreditcarryforwards: int
    deferredtaxassetstaxdeferredexpensereservesandaccruals: int
    deferredtaxassetsdeferredincome: int
    deferredtaxassetsleaseliabilities: int
    deferredtaxassetsothercomprehensiveloss: int
    deferredtaxassetsother: int
    deferredtaxassetsgross: int
    deferredtaxassetsvaluationallowance: int
    deferredtaxassetsnet: int
    deferredtaxliabilitiespropertyplantandequipment: int
    deferredtaxliabilitiesleasingarrangements: int
    deferredtaxliabilitiesminimumtaxonforeignearnings: int
    deferredtaxliabilitiesother: int
    deferredincometaxliabilities: int
    deferredtaxassetsliabilitiesnet: int
    unrecognizedtaxbenefitsincreasesresultingfrompriorperiodtaxpositions: int
    unrecognizedtaxbenefitsdecreasesresultingfrompriorperiodtaxpositions: int
    unrecognizedtaxbenefitsincreasesresultingfromcurrentperiodtaxpositions: int
    unrecognizedtaxbenefitsreductionsresultingfromlapseofapplicablestatuteoflimitations: int
    lesseeoperatingandfinanceleasetermofcontract: str
    operatingleasecost: int
    variableleasecost: int
    operatingleasepayments: int
    rightofuseassetsobtainedinexchangeforoperatingandfinanceleaseliabilities: int
    operatingandfinanceleaseweightedaverageremainingleaseterm: str
    operatingandfinanceleaseweightedaveragediscountratepercent: float
    unrecordedunconditionalpurchaseobligationbalancesheetamount: int
    lesseeoperatingandfinanceleaseleasenotyetcommencedtermofcontract: str
    operatingleaserightofuseasset: int
    operatingleaserightofuseassetstatementoffinancialpositionextensiblelist: str
    financeleaserightofuseasset: int
    financeleaserightofuseassetstatementoffinancialpositionextensiblelist: str
    operatingandfinanceleaserightofuseasset: int
    operatingleaseliabilitycurrent: int
    operatingleaseliabilitycurrentstatementoffinancialpositionextensiblelist: str
    operatingleaseliabilitynoncurrent: int
    operatingleaseliabilitynoncurrentstatementoffinancialpositionextensiblelist: str
    financeleaseliabilitycurrent: int
    financeleaseliabilitycurrentstatementoffinancialpositionextensiblelist: str
    financeleaseliabilitynoncurrent: int
    financeleaseliabilitynoncurrentstatementoffinancialpositionextensiblelist: str
    operatingandfinanceleaseliability: int
    lesseeoperatingleaseliabilitypaymentsduenexttwelvemonths: int
    lesseeoperatingleaseliabilitypaymentsdueyeartwo: int
    lesseeoperatingleaseliabilitypaymentsdueyearthree: int
    lesseeoperatingleaseliabilitypaymentsdueyearfour: int
    lesseeoperatingleaseliabilitypaymentsdueyearfive: int
    lesseeoperatingleaseliabilitypaymentsdueafteryearfive: int
    lesseeoperatingleaseliabilitypaymentsdue: int
    lesseeoperatingleaseliabilityundiscountedexcessamount: int
    operatingleaseliability: int
    financeleaseliabilitypaymentsduenexttwelvemonths: int
    financeleaseliabilitypaymentsdueyeartwo: int
    financeleaseliabilitypaymentsdueyearthree: int
    financeleaseliabilitypaymentsdueyearfour: int
    financeleaseliabilitypaymentsdueyearfive: int
    financeleaseliabilitypaymentsdueafteryearfive: int
    financeleaseliabilitypaymentsdue: int
    financeleaseliabilityundiscountedexcessamount: int
    financeleaseliability: int
    lesseeoperatingandfinanceleaseliabilitytobepaidyearone: int
    lesseeoperatingandfinanceleaseliabilitytobepaidyeartwo: int
    lesseeoperatingandfinanceleaseliabilitytobepaidyearthree: int
    lesseeoperatingandfinanceleaseliabilitytobepaidyearfour: int
    lesseeoperatingandfinanceleaseliabilitytobepaidyearfive: int
    lesseeoperatingandfinanceleaseliabilitytobepaidafteryearfive: int
    lesseeoperatingandfinanceleaseliabilitytobepaid: int
    lesseeoperatingandfinanceleaseliabilityundiscountedexcessamount: int
    debtinstrumentterm: str
    shorttermdebtweightedaverageinterestrate: float
    longtermdebtfairvalue: int
    proceedsfromrepaymentsofshorttermdebtmaturinginthreemonthsorless: int
    debtinstrumentcarryingamount: int
    debtinstrumentunamortizeddiscountpremiumanddebtissuancecostsnet: int
    hedgeaccountingadjustmentsrelatedtolongtermdebt: int
    longtermdebt: int
    debtinstrumentmaturityyearrangestart: int
    debtinstrumentmaturityyearrangeend: int
    debtinstrumentinterestratestatedpercentage: float
    debtinstrumentinterestrateeffectivepercentage: float
    longtermdebtmaturitiesrepaymentsofprincipalinnexttwelvemonths: int
    longtermdebtmaturitiesrepaymentsofprincipalinyeartwo: int
    longtermdebtmaturitiesrepaymentsofprincipalinyearthree: int
    longtermdebtmaturitiesrepaymentsofprincipalinyearfour: int
    longtermdebtmaturitiesrepaymentsofprincipalinyearfive: int
    longtermdebtmaturitiesrepaymentsofprincipalafteryearfive: int
    stockrepurchasedandretiredduringperiodshares: int
    stockissuedduringperiodsharessharebasedpaymentarrangementnetofshareswithheldfortaxes: int
    sharebasedcompensationarrangementbysharebasedpaymentawardawardvestingperiod1: str
    sharebasedcompensationarrangementbysharebasedpaymentawardequityinstrumentsotherthanoptionsnumberofsharesofcommonstockissuedperunituponvesting: int
    sharebasedcompensationarrangementbysharebasedpaymentawardequityinstrumentsotherthanoptionsvestedinperiodtotalfairvalue: int
    sharespaidfortaxwithholdingforsharebasedcompensation: int
    employeeservicesharebasedcompensationnonvestedawardstotalcompensationcostnotyetrecognized: int
    employeeservicesharebasedcompensationnonvestedawardstotalcompensationcostnotyetrecognizedperiodforrecognition1: str
    sharebasedcompensationarrangementbysharebasedpaymentawardequityinstrumentsotherthanoptionsnonvestednumber: int
    sharebasedcompensationarrangementbysharebasedpaymentawardequityinstrumentsotherthanoptionsgrantsinperiod: int
    sharebasedcompensationarrangementbysharebasedpaymentawardequityinstrumentsotherthanoptionsvestedinperiod: int
    sharebasedcompensationarrangementbysharebasedpaymentawardequityinstrumentsotherthanoptionsforfeitedinperiod: int
    sharebasedcompensationarrangementbysharebasedpaymentawardequityinstrumentsotherthanoptionsnonvestedweightedaveragegrantdatefairvalue: float
    sharebasedcompensationarrangementbysharebasedpaymentawardequityinstrumentsotherthanoptionsgrantsinperiodweightedaveragegrantdatefairvalue: float
    sharebasedcompensationarrangementbysharebasedpaymentawardequityinstrumentsotherthanoptionsvestedinperiodweightedaveragegrantdatefairvalue: float
    sharebasedcompensationarrangementbysharebasedpaymentawardequityinstrumentsotherthanoptionsforfeituresweightedaveragegrantdatefairvalue: float
    sharebasedcompensationarrangementbysharebasedpaymentawardequityinstrumentsotherthanoptionsaggregateintrinsicvaluenonvested: int
    allocatedsharebasedcompensationexpense: int
    employeeservicesharebasedcompensationtaxbenefitfromcompensationexpense: int
    unrecordedunconditionalpurchaseobligationbalanceonfirstanniversary: int
    unrecordedunconditionalpurchaseobligationbalanceonsecondanniversary: int
    unrecordedunconditionalpurchaseobligationbalanceonthirdanniversary: int
    unrecordedunconditionalpurchaseobligationbalanceonfourthanniversary: int
    unrecordedunconditionalpurchaseobligationbalanceonfifthanniversary: int
    unrecordedunconditionalpurchaseobligationdueafterfiveyears: int
    othergeneralandadministrativeexpense: int
    noncurrentassets: int
    trdarrsecuritiesaggavailamt: int
    insidertrdpoliciesprocadoptedflag: bool

class FMPAsReportedFullStatement(BaseModel):
    symbol: str
    fiscalYear: int
    period: str
    reportedCurrency: Optional[str] = None
    date: str
    data: FMPAsReportedFullStatementData

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

class FMPIndexConstituent(BaseModel):
    symbol: str
    name: str
    sector: str
    subSector: str
    headQuarter: str
    dateFirstAdded: str
    cik: str
    founded: str

class FMPHistoricalIndexConstituent(BaseModel):
    dateAdded: str
    addedSecurity: str
    removedTicker: str
    removedSecurity: str
    date: str
    symbol: str
    reason: str

class FMPInsiderTrade(BaseModel):
    symbol: str
    filingDate: str
    transactionDate: str
    reportingCik: str
    companyCik: str
    transactionType: str
    securitiesOwned: int
    reportingName: str
    typeOfOwner: str
    acquisitionOrDisposition: str
    directOrIndirect: str
    formType: str
    securitiesTransacted: int
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
    citizenshipOrPlaceOfOrganization: str
    soleVotingPower: str
    sharedVotingPower: str
    soleDispositivePower: str
    sharedDispositivePower: str
    amountBeneficiallyOwned: str
    percentOfClass: str
    typeOfReportingPerson: str
    url: str

class FMPPressRelease(BaseModel):
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

class FMPQuoteFull(BaseModel):
    symbol: str
    name: str
    price: float
    changePercentage: float
    change: float
    volume: int
    dayLow: float
    dayHigh: float
    yearHigh: float
    yearLow: float
    marketCap: int
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
    tradeSize: int
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
    _1D: float
    _5D: float
    _1M: float
    _3M: float
    _6M: float
    ytd: float
    _1Y: float
    _3Y: float
    _5Y: float
    _10Y: float
    max: float

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
    phoneNumber: str

class FMPIndustryClassification(BaseModel):
    office: str
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
    year: int
    date: str
    content: str

class FMPEarningsTranscriptDate(BaseModel):
    quarter: int
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

class FMPBulkFinancialScores(BaseModel):
    symbol: str
    reportedCurrency: str
    altmanZScore: str
    piotroskiScore: str
    workingCapital: str
    totalAssets: str
    retainedEarnings: str
    ebit: str
    marketCap: str
    totalLiabilities: str
    revenue: str

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

class FMPBulkIncomeStatement(BaseModel):
    date: str
    symbol: str
    reportedCurrency: str
    cik: str
    filingDate: str
    acceptedDate: str
    fiscalYear: str
    period: str
    revenue: str
    costOfRevenue: str
    grossProfit: str
    researchAndDevelopmentExpenses: str
    generalAndAdministrativeExpenses: str
    sellingAndMarketingExpenses: str
    sellingGeneralAndAdministrativeExpenses: str
    otherExpenses: str
    operatingExpenses: str
    costAndExpenses: str
    netInterestIncome: Optional[str] = None
    interestIncome: str
    interestExpense: str
    depreciationAndAmortization: str
    ebitda: str
    ebit: Optional[str] = None
    nonOperatingIncomeExcludingInterest: Optional[str] = None
    operatingIncome: str
    totalOtherIncomeExpensesNet: str
    incomeBeforeTax: str
    incomeTaxExpense: str
    netIncomeFromContinuingOperations: Optional[str] = None
    netIncomeFromDiscontinuedOperations: Optional[str] = None
    otherAdjustmentsToNetIncome: Optional[str] = None
    netIncome: str
    netIncomeDeductions: Optional[str] = None
    bottomLineNetIncome: Optional[str] = None
    eps: str
    epsDiluted: str
    weightedAverageShsOut: str
    weightedAverageShsOutDil: str

class FMPBulkIncomeStatementGrowth(BaseModel):
    symbol: str
    date: str
    fiscalYear: str
    period: str
    reportedCurrency: str
    growthRevenue: str
    growthCostOfRevenue: str
    growthGrossProfit: str
    growthGrossProfitRatio: str
    growthResearchAndDevelopmentExpenses: str
    growthGeneralAndAdministrativeExpenses: str
    growthSellingAndMarketingExpenses: str
    growthOtherExpenses: str
    growthOperatingExpenses: str
    growthCostAndExpenses: str
    growthInterestIncome: str
    growthInterestExpense: str
    growthDepreciationAndAmortization: str
    growthEBITDA: str
    growthOperatingIncome: str
    growthIncomeBeforeTax: str
    growthIncomeTaxExpense: str
    growthNetIncome: str
    growthEPS: str
    growthEPSDiluted: str
    growthWeightedAverageShsOut: str
    growthWeightedAverageShsOutDil: str

class FMPBulkBalanceSheetStatement(BaseModel):
    date: str
    symbol: str
    reportedCurrency: str
    cik: str
    filingDate: str
    acceptedDate: str
    fiscalYear: str
    period: str
    cashAndCashEquivalents: str
    shortTermInvestments: str
    cashAndShortTermInvestments: str
    netReceivables: str
    inventory: str
    otherCurrentAssets: str
    totalCurrentAssets: str
    propertyPlantEquipmentNet: str
    goodwill: str
    intangibleAssets: str
    goodwillAndIntangibleAssets: str
    longTermInvestments: str
    taxAssets: str
    otherNonCurrentAssets: str
    totalNonCurrentAssets: str
    otherAssets: str
    totalAssets: str
    accountPayables: str
    shortTermDebt: str
    taxPayables: str
    deferredRevenue: str
    otherCurrentLiabilities: str
    totalCurrentLiabilities: str
    longTermDebt: str
    otherNonCurrentLiabilities: str
    totalNonCurrentLiabilities: str
    otherLiabilities: str
    capitalLeaseObligations: str
    totalLiabilities: str
    preferredStock: str
    commonStock: str
    retainedEarnings: str
    accumulatedOtherComprehensiveIncomeLoss: str
    otherTotalStockholdersEquity: str
    totalStockholdersEquity: str
    totalEquity: str
    minorityInterest: str
    totalLiabilitiesAndTotalEquity: str
    totalInvestments: str
    totalDebt: str
    netDebt: str

class FMPBulkBalanceSheetGrowth(BaseModel):
    symbol: str
    date: str
    fiscalYear: str
    period: str
    reportedCurrency: str
    growthCashAndCashEquivalents: str
    growthShortTermInvestments: str
    growthCashAndShortTermInvestments: str
    growthNetReceivables: str
    growthInventory: str
    growthOtherCurrentAssets: str
    growthTotalCurrentAssets: str
    growthPropertyPlantEquipmentNet: str
    growthGoodwill: str
    growthIntangibleAssets: str
    growthGoodwillAndIntangibleAssets: str
    growthLongTermInvestments: str
    growthTaxAssets: str
    growthOtherNonCurrentAssets: str
    growthTotalNonCurrentAssets: str
    growthOtherAssets: str
    growthTotalAssets: str
    growthAccountPayables: str
    growthShortTermDebt: str
    growthTaxPayables: str
    growthDeferredRevenue: str
    growthOtherCurrentLiabilities: str
    growthTotalCurrentLiabilities: str
    growthLongTermDebt: str
    growthDeferredRevenueNonCurrent: str
    growthDeferredTaxLiabilitiesNonCurrent: str
    growthOtherNonCurrentLiabilities: str
    growthTotalNonCurrentLiabilities: str
    growthOtherLiabilities: str
    growthTotalLiabilities: str
    growthPreferredStock: str
    growthCommonStock: str
    growthRetainedEarnings: str
    growthAccumulatedOtherComprehensiveIncomeLoss: str
    growthOthertotalStockholdersEquity: str
    growthTotalStockholdersEquity: str
    growthMinorityInterest: str
    growthTotalEquity: str
    growthTotalLiabilitiesAndStockholdersEquity: str
    growthTotalInvestments: str
    growthTotalDebt: str
    growthNetDebt: str

class FMPBulkCashFlowStatement(BaseModel):
    date: str
    symbol: str
    reportedCurrency: str
    cik: str
    filingDate: str
    acceptedDate: str
    fiscalYear: str
    period: str
    netIncome: str
    depreciationAndAmortization: str
    deferredIncomeTax: str
    stockBasedCompensation: str
    changeInWorkingCapital: str
    otherNonCashItems: str
    netCashProvidedByOperatingActivities: str
    investmentsInPropertyPlantAndEquipment: str
    acquisitionsNet: str
    purchasesOfInvestments: str
    salesMaturitiesOfInvestments: str
    otherInvestingActivities: str
    netCashProvidedByInvestingActivities: str
    commonStockRepurchased: str
    netDividendsPaid: str
    otherFinancingActivities: str
    netCashProvidedByFinancingActivities: str
    effectOfForexChangesOnCash: str
    netChangeInCash: str
    cashAtEndOfPeriod: str
    cashAtBeginningOfPeriod: str
    operatingCashFlow: str
    capitalExpenditure: str
    freeCashFlow: str

class FMPBulkCashFlowGrowth(BaseModel):
    symbol: str
    date: str
    fiscalYear: str
    period: str
    reportedCurrency: str
    growthNetIncome: str
    growthDepreciationAndAmortization: str
    growthDeferredIncomeTax: str
    growthStockBasedCompensation: str
    growthChangeInWorkingCapital: str
    growthOtherNonCashItems: str
    growthNetCashProvidedByOperatingActivites: str
    growthInvestmentsInPropertyPlantAndEquipment: str
    growthAcquisitionsNet: str
    growthPurchasesOfInvestments: str
    growthSalesMaturitiesOfInvestments: str
    growthOtherInvestingActivites: str
    growthNetCashUsedForInvestingActivites: str
    growthDebtRepayment: str
    growthCommonStockIssued: str
    growthCommonStockRepurchased: str
    growthDividendsPaid: str
    growthOtherFinancingActivites: str
    growthNetCashUsedProvidedByFinancingActivities: str
    growthEffectOfForexChangesOnCash: str
    growthNetChangeInCash: str
    growthCashAtEndOfPeriod: str
    growthCashAtBeginningOfPeriod: str
    growthOperatingCashFlow: str
    growthCapitalExpenditure: str
    growthFreeCashFlow: str

class FMPFinancialStatement(BaseModel):
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
    # Balance Sheet Fields
    cashAndCashEquivalents: Optional[int] = None
    shortTermInvestments: Optional[int] = None
    cashAndShortTermInvestments: Optional[int] = None
    netReceivables: Optional[int] = None
    accountsReceivables: Optional[str] = None # Can be empty string
    otherReceivables: Optional[str] = None # Can be empty string
    inventory: Optional[int] = None
    prepaids: Optional[str] = None # Can be empty string
    otherCurrentAssets: Optional[int] = None
    totalCurrentAssets: Optional[int] = None
    propertyPlantEquipmentNet: Optional[int] = None
    goodwill: Optional[int] = None
    intangibleAssets: Optional[int] = None
    goodwillAndIntangibleAssets: Optional[int] = None
    longTermInvestments: Optional[int] = None
    taxAssets: Optional[int] = None
    otherNonCurrentAssets: Optional[int] = None
    totalNonCurrentAssets: Optional[int] = None
    otherAssets: Optional[int] = None
    totalAssets: Optional[int] = None
    totalPayables: Optional[str] = None # Can be empty string
    accountPayables: Optional[str] = None # Can be empty string
    otherPayables: Optional[str] = None # Can be empty string
    accruedExpenses: Optional[str] = None # Can be empty string
    shortTermDebt: Optional[int] = None
    capitalLeaseObligationsCurrent: Optional[str] = None # Can be empty string
    taxPayables: Optional[str] = None # Can be empty string
    deferredRevenue: Optional[int] = None
    otherCurrentLiabilities: Optional[int] = None
    totalCurrentLiabilities: Optional[int] = None
    longTermDebt: Optional[int] = None
    capitalLeaseObligationsNonCurrent: Optional[str] = None # Can be empty string
    deferredRevenueNonCurrent: Optional[int] = None
    deferredTaxLiabilitiesNonCurrent: Optional[int] = None
    otherNonCurrentLiabilities: Optional[int] = None
    totalNonCurrentLiabilities: Optional[int] = None
    otherLiabilities: Optional[int] = None
    capitalLeaseObligations: Optional[str] = None # Can be empty string
    totalLiabilities: Optional[int] = None
    treasuryStock: Optional[str] = None # Can be empty string
    preferredStock: Optional[int] = None
    commonStock: Optional[int] = None
    retainedEarnings: Optional[int] = None
    additionalPaidInCapital: Optional[str] = None # Can be empty string
    accumulatedOtherComprehensiveIncomeLoss: Optional[int] = None
    otherTotalStockholdersEquity: Optional[int] = None
    totalStockholdersEquity: Optional[int] = None
    totalEquity: Optional[int] = None
    minorityInterest: Optional[int] = None
    totalLiabilitiesAndTotalEquity: Optional[int] = None
    totalInvestments: Optional[int] = None
    totalDebt: Optional[int] = None
    netDebt: Optional[int] = None
    # Cash Flow Fields
    deferredIncomeTax: Optional[int] = None
    stockBasedCompensation: Optional[int] = None
    changeInWorkingCapital: Optional[int] = None
    otherNonCashItems: Optional[int] = None
    netCashProvidedByOperatingActivities: Optional[int] = None
    investmentsInPropertyPlantAndEquipment: Optional[int] = None
    acquisitionsNet: Optional[int] = None
    purchasesOfInvestments: Optional[int] = None
    salesMaturitiesOfInvestments: Optional[int] = None
    otherInvestingActivities: Optional[int] = None
    netCashProvidedByInvestingActivities: Optional[int] = None
    netDebtIssuance: Optional[str] = None # Can be empty string
    longTermNetDebtIssuance: Optional[str] = None # Can be empty string
    shortTermNetDebtIssuance: Optional[str] = None # Can be empty string
    netStockIssuance: Optional[str] = None # Can be empty string
    netCommonStockIssuance: Optional[str] = None # Can be empty string
    commonStockIssuance: Optional[int] = None
    commonStockRepurchased: Optional[int] = None
    netPreferredStockIssuance: Optional[str] = None # Can be empty string
    netDividendsPaid: Optional[int] = None
    commonDividendsPaid: Optional[str] = None # Can be empty string
    preferredDividendsPaid: Optional[str] = None # Can be empty string
    otherFinancingActivities: Optional[int] = None
    netCashProvidedByFinancingActivities: Optional[int] = None
    effectOfForexChangesOnCash: Optional[int] = None
    netChangeInCash: Optional[int] = None
    cashAtEndOfPeriod: Optional[int] = None
    cashAtBeginningOfPeriod: Optional[int] = None
    operatingCashFlow: Optional[int] = None
    capitalExpenditure: Optional[int] = None
    freeCashFlow: Optional[int] = None
    incomeTaxesPaid: Optional[str] = None # Can be empty string
    interestPaid: Optional[str] = None # Can be empty string

class FMPFinancialStatementTTM(BaseModel):
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
    # Balance Sheet Fields
    cashAndCashEquivalents: Optional[int] = None
    shortTermInvestments: Optional[int] = None
    cashAndShortTermInvestments: Optional[int] = None
    netReceivables: Optional[int] = None
    accountsReceivables: Optional[int] = None
    otherReceivables: Optional[int] = None
    inventory: Optional[int] = None
    prepaids: Optional[int] = None
    otherCurrentAssets: Optional[int] = None
    totalCurrentAssets: Optional[int] = None
    propertyPlantEquipmentNet: Optional[int] = None
    goodwill: Optional[int] = None
    intangibleAssets: Optional[int] = None
    goodwillAndIntangibleAssets: Optional[int] = None
    longTermInvestments: Optional[int] = None
    taxAssets: Optional[int] = None
    otherNonCurrentAssets: Optional[int] = None
    totalNonCurrentAssets: Optional[int] = None
    otherAssets: Optional[int] = None
    totalAssets: Optional[int] = None
    totalPayables: Optional[int] = None
    accountPayables: Optional[int] = None
    otherPayables: Optional[int] = None
    accruedExpenses: Optional[int] = None
    shortTermDebt: Optional[int] = None
    capitalLeaseObligationsCurrent: Optional[int] = None
    taxPayables: Optional[int] = None
    deferredRevenue: Optional[int] = None
    otherCurrentLiabilities: Optional[int] = None
    totalCurrentLiabilities: Optional[int] = None
    longTermDebt: Optional[int] = None
    deferredRevenueNonCurrent: Optional[int] = None
    deferredTaxLiabilitiesNonCurrent: Optional[int] = None
    otherNonCurrentLiabilities: Optional[int] = None
    totalNonCurrentLiabilities: Optional[int] = None
    otherLiabilities: Optional[int] = None
    capitalLeaseObligations: Optional[int] = None
    totalLiabilities: Optional[int] = None
    treasuryStock: Optional[int] = None
    preferredStock: Optional[int] = None
    commonStock: Optional[int] = None
    retainedEarnings: Optional[int] = None
    additionalPaidInCapital: Optional[int] = None
    accumulatedOtherComprehensiveIncomeLoss: Optional[int] = None
    otherTotalStockholdersEquity: Optional[int] = None
    totalStockholdersEquity: Optional[int] = None
    totalEquity: Optional[int] = None
    minorityInterest: Optional[int] = None
    totalLiabilitiesAndTotalEquity: Optional[int] = None
    totalInvestments: Optional[int] = None
    totalDebt: Optional[int] = None
    netDebt: Optional[int] = None
    # Cash Flow Fields
    deferredIncomeTax: Optional[int] = None
    stockBasedCompensation: Optional[int] = None
    changeInWorkingCapital: Optional[int] = None
    accountsReceivables: Optional[int] = None
    inventory: Optional[int] = None
    accountsPayables: Optional[int] = None
    otherWorkingCapital: Optional[int] = None
    otherNonCashItems: Optional[int] = None
    netCashProvidedByOperatingActivities: Optional[int] = None
    investmentsInPropertyPlantAndEquipment: Optional[int] = None
    acquisitionsNet: Optional[int] = None
    purchasesOfInvestments: Optional[int] = None
    salesMaturitiesOfInvestments: Optional[int] = None
    otherInvestingActivities: Optional[int] = None
    netCashProvidedByInvestingActivities: Optional[int] = None
    netDebtIssuance: Optional[int] = None
    longTermNetDebtIssuance: Optional[int] = None
    shortTermNetDebtIssuance: Optional[int] = None
    netStockIssuance: Optional[int] = None
    netCommonStockIssuance: Optional[int] = None
    commonStockIssuance: Optional[int] = None
    commonStockRepurchased: Optional[int] = None
    netPreferredStockIssuance: Optional[int] = None
    netDividendsPaid: Optional[int] = None
    commonDividendsPaid: Optional[int] = None
    preferredDividendsPaid: Optional[int] = None
    otherFinancingActivities: Optional[int] = None
    netCashProvidedByFinancingActivities: Optional[int] = None
    effectOfForexChangesOnCash: Optional[int] = None
    netChangeInCash: Optional[int] = None
    cashAtEndOfPeriod: Optional[int] = None
    cashAtBeginningOfPeriod: Optional[int] = None
    operatingCashFlow: Optional[int] = None
    capitalExpenditure: Optional[int] = None
    freeCashFlow: Optional[int] = None
    incomeTaxesPaid: Optional[int] = None
    interestPaid: Optional[int] = None

class FMPKeyMetrics(BaseModel):
    symbol: str
    date: str
    fiscalYear: str
    period: str
    reportedCurrency: str
    marketCap: int
    enterpriseValue: int
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
    salesGeneralAndAdministrativeToRevenue: int
    researchAndDevelopementToRevenue: float
    stockBasedCompensationToRevenue: float
    intangiblesToTotalAssets: int
    averageReceivables: int
    averagePayables: int
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
    interestCoverageRatio: int
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

class FMPFinancialStatementGrowth(BaseModel):
    symbol: str
    date: str
    fiscalYear: str
    period: str
    reportedCurrency: str
    revenueGrowth: float
    grossProfitGrowth: float
    ebitgrowth: float
    operatingIncomeGrowth: float
    netIncomeGrowth: float
    epsgrowth: float
    epsdilutedGrowth: float
    weightedAverageSharesGrowth: float
    weightedAverageSharesDilutedGrowth: float
    dividendsPerShareGrowth: float
    operatingCashFlowGrowth: float
    receivablesGrowth: float
    inventoryGrowth: float
    assetGrowth: float
    bookValueperShareGrowth: float
    debtGrowth: float
    rdexpenseGrowth: float
    sgaexpensesGrowth: float
    freeCashFlowGrowth: float
    tenYRevenueGrowthPerShare: float
    fiveYRevenueGrowthPerShare: float
    threeYRevenueGrowthPerShare: float
    tenYOperatingCFGrowthPerShare: float
    fiveYOperatingCFGrowthPerShare: float
    threeYOperatingCFGrowthPerShare: float
    tenYNetIncomeGrowthPerShare: float
    fiveYNetIncomeGrowthPerShare: float
    threeYNetIncomeGrowthPerShare: float
    tenYShareholdersEquityGrowthPerShare: float
    fiveYShareholdersEquityGrowthPerShare: float
    threeYShareholdersEquityGrowthPerShare: float
    tenYDividendperShareGrowthPerShare: float
    fiveYDividendperShareGrowthPerShare: float
    threeYDividendperShareGrowthPerShare: float
    ebitdaGrowth: Optional[float] = None
    growthCapitalExpenditure: Optional[float] = None
    tenYBottomLineNetIncomeGrowthPerShare: Optional[float] = None
    fiveYBottomLineNetIncomeGrowthPerShare: Optional[float] = None
    threeYBottomLineNetIncomeGrowthPerShare: Optional[float] = None


class Error(BaseModel):
    error: str
    details: str
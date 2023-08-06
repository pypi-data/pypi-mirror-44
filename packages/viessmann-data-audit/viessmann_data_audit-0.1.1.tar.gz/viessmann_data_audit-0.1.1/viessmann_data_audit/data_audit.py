# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 08:50:36 2019
@author: strq
"""

import numpy as np # Vectors and vectorized functions
import pandas as pd # DataFrames and DataSeries
import matplotlib.pyplot as plt # Plots
import seaborn as sns # Improving Plots
import warnings # Create or Hide Warnings
import sklearn.decomposition as skd
from sklearn.cluster import KMeans
from sklearn.cluster import SpectralClustering
from sklearn import metrics
from sklearn.preprocessing import MinMaxScaler


def data_type_mapper(strDT):
    """
    Parameters
    #---------
    strDT    String telling data type in pandas language
             (pandas.DataFrame.dtype.name)
    
    Returns
    #------
    String telling data type in english
    
    Description
    #----------
    """
    # List for non numerical data types
    lstNonNumDT = ["object", "datetime64[ns]", "bool", "timedelta[ns]",
                  "category"]
    lstNonNumNamDT = ["datetime64[ns]", "bool", "timedelta[ns]"]
    lstTime = ["datetime64[ns]"]
    # only numerical and categorical
    if(strDT not in lstNonNumDT):
        return "Numeric"
    # only objects
    elif(strDT not in lstNonNumNamDT):
        return "Name"
    elif(strDT in lstTime):
        return "Datetime"
    else:
        return "Undefined"

def data_description(dfData):
    """
    Parameters
    #---------
    dfData    pandas.DataFrame containing data
    
    Return
    #-----
    dfDesc    pandas.DataFrame
    
    Description
    #----------
    General overview over properties of data frame.
    Properties shown are about datatype, number of missing values and unique 
    values, range of values.
    """
    lstNonNumCatDT = ["object", "datetime64[ns]", "bool", "timedelta[ns]",
                      "category"]
    dfDesc = pd.DataFrame(columns = ["Name",
                                     "Data_Type_pd",
                                     "Data_Type",
                                     "Number_Missing_Values",
                                     "Proportion_Missing_Values",
                                     "Number_Unique_Values",
                                     "Proportion_Unique_Values",
                                     "Range_Values"])
    intDateTimeCounter = 0
    # Number of data points
    intNumDatPoi = len(dfData.iloc[:,0])
    for j in dfData.columns:
        # Number Missing Values
        intNumMV = np.array(dfData[j].isnull()).sum()
        # Proportion Missing Values
        intProMV = intNumMV/intNumDatPoi
        # Number Unique Values
        intNumUV = dfData[j].nunique()
        # Proportion Unique Values
        intPropUV = intNumUV/intNumDatPoi
        if(dfData.dtypes[j].name not in lstNonNumCatDT):
            #max und min
            intMin = dfData.loc[:,j].min()
            intMax = dfData.loc[:,j].max()
            rngVal = list()
            rngVal.append(intMin), rngVal.append(intMax)
        elif dfData.dtypes[j].name in ["category", "object"]:
            #distinct values
            rngVal = dfData.loc[:,j].unique()
        else:
            rngVal = -1
        dfDesc = dfDesc.append({"Name": j,
                                "Data_Type_pd": dfData[j].dtype.name,
                                "Data_Type":
                                    data_type_mapper(dfData[j].dtype.name),
                                "Number_Missing_Values": intNumMV,
                                "Proportion_Missing_Values": intProMV,
                                "Number_Unique_Values": intNumUV,
                                "Proportion_Unique_Values": intPropUV,
                                "Range_Values": rngVal},
                                 ignore_index=True)
        
        if dfData[j].dtype.name == "datetime64[ns]":
            intDateTimeCounter = intDateTimeCounter + 1
    if(intDateTimeCounter == 0):
        warnings.warn("No column in datetime found")
    return dfDesc

def value_range_of_features(dfData):
    """
    Parameters
    #---------
    dfData    pandas.DataFrame containing data
    
    Returns
    #---------
    serFeatures    pandas.Series with information about range for each feature.
    
    Description
    #----------
    For numerical and ordinal data there are two values. First for lower and
    second for upper bound of range. For nominal data there are lists with
    distinct values.
    """
    dictFeatures = dict()
    lstNonNumCatDT = ["object", "datetime64[ns]", "bool", "timedelta[ns]",
                      "category"]
    for j in dfData.columns:
        if(dfData.dtypes[j].name not in lstNonNumCatDT):
            #max und min
            intMin = dfData.loc[:,j].min()
            intMax = dfData.loc[:,j].max()
            lst = list()
            lst.append(intMin), lst.append(intMax)
            dictFeatures.update({j:lst})
        elif dfData.dtypes[j].name in ["category", "object"]:
            #distinct values
            arrUnique = dfData.loc[:,j].unique()
            dictFeatures.update({j:arrUnique})
    serFeatures = pd.Series(dictFeatures)
    return serFeatures

def classify_data_type_logic(dfDataCol):
    """
    Parameters
    #---------
    dfDataCol    pandas.DataFrame column of a data set
    
    Returns
    #------
    string with data type classification
    
    Description
    #----------
    oc    ordered category
    uc    unordered category
    num    numeric
    obj    python object
    undefined    boolean, datetime, timedelta
    
    undefined type classes stay undefined, for they are all not useful for
    further analysis in the here implemented methods. For later use you can
    of course change this, if needed.
    """
    # List for non numerical or categorical data types
    lstNonNumCatDT = ["object", "datetime64[ns]", "bool", "timedelta[ns]"]

    # only numerical and categorical
    if(dfDataCol.dtypes.name not in lstNonNumCatDT):
        # only categorical
        if(dfDataCol.dtypes.name == "category"):
            # only ordered categorical
            if(dfDataCol.dtypes.ordered):
                return "oc"
            else:
                return "uc"
        # only numerical
        else:
            return "num"
    # only objects
    elif(dfDataCol.dtypes.name == "object"):
        return "obj"
    elif(dfDataCol.dtypes.name == "bool"):
        return "bool"
    else:
        return "Timedata"

def proportion_of_missing_values(dfData):
    """
    Parameters
    #---------
    dfData    pandas.DataFrame containing data
    
    Returns
    #---------
    serProportions    pandas.Series containing values between 0 and 1 for each
    feature.
    
    Description
    #----------
    Computes the proportion of missing values to all values for each feature
    """
    numberOfRows = len(dfData)
    serNumberOfNans = dfData.isnull().sum()
    serProportions = serNumberOfNans/numberOfRows
    return serProportions

def heatmap_missing_values(dfData, tplFigSize = (10, 5)):
    """
    Parameters
    #---------
    dfData    pandas.DataFrame containing data
    
    tplFigSize    tuple telling the size of the figure for the plot

    Description
    #----------
    Plot Heatmap for missing values
    """
    plt.figure(figsize = tplFigSize)
    sns.heatmap(dfData.isnull(), cbar=False)
    return

def get_numericals(dfData):
    """
    Parameters
    #---------
    dfData    pandas.DataFrame containing data
    
    Returns
    #------
    dfDataCopy    pandas.DataFrame containing only numerical columns
    
    Description
    #----------
    Drop all non numeric columns
    """
    lstNonNumCatDT = ["object", "datetime64[ns]", "bool", "timedelta[ns]",
                      "category"]
    dfDataCopy = dfData.copy(deep = True)
    for j in dfDataCopy.columns:
        if(dfDataCopy.dtypes[j].name in lstNonNumCatDT):
            dfDataCopy = dfDataCopy.drop(columns = j)
    return dfDataCopy

def count_invalid_values(dfData, dctValidValues, strColType):
    """
    Parameters
    #---------
    dfData    pandas.DataFrame containing data
    
    Returns
    #------
    intInvalidValues    Integer: count of invalid values based on input.
    
    Description
    #----------
    Internal Method using boolean mask to decide which Values are valid
    depending on upper and lower bounds from dictionary and summing up ones
    and zeros.
    """
    intInvalidValues = 0
    if dfData.name in dctValidValues:
        if strColType == "num":
            assert len(dctValidValues[dfData.name]) == 2
            assert isinstance(dctValidValues[dfData.name][0],(int, float))
            assert isinstance(dctValidValues[dfData.name][1],(int, float))
            intInvalidValues = (
                (dfData >= (dctValidValues[dfData.name][0])) &
                (dfData <= (dctValidValues[dfData.name][1]))
                ).sum()
        else:
            if len(dctValidValues[dfData.name]) == 2:
                intInvalidValues = (
                (dfData >= (dctValidValues[dfData.name][0])) &
                (dfData <= (dctValidValues[dfData.name][1]))
                ).sum()
            else:
                intInvalidValues = 0
    else:
        intInvalidValues = 0
    return intInvalidValues

def invalid_value_helper(dfData, dctValidValues):
    """
    Parameters
    #---------
    dfData    pandas.DataFrame containing data
    
    dctValidValues    dictionary containing characteristic lists for each
    feature
    
    Returns
    #------
    intInvalidValues    Integer
    
    Description
    #----------
    Takes a column, distinguishes between data types and counts invalid 
    values depending on 2-lists for numeric and ordered categoric values and 
    lists for nominal data. 2-lists are like an interval defining a range.
    Lists for nominal data just states which values are valid. Every value
    not contained in list counts as invalid.
    """
    strColType = classify_data_type_logic(dfData)
    # switch case for data type
    if(strColType in ["oc", "num"]):
        if dfData.name in dctValidValues:
            intInvalidValues = count_invalid_values(dfData,
                                                    dctValidValues,
                                                    strColType)
            return intInvalidValues
    elif(strColType in ["obj", "uc"]):
        if dfData.name in dctValidValues:
            intInvalidValues = (dfData.isin(dctValidValues[dfData.name])).sum()
            return intInvalidValues
    else:
        if dfData.name in dctValidValues:
            intInvalidValues = 2*len(dfData)
            return intInvalidValues

def proportion_of_invalid_values(dfData, dctValidValues):
    """
    Parameters
    #---------
    dfData    pandas.DataFrame containing data
    
    dctValidValues    dictionary containing characteristic lists for each 
                      feature
    
    Returns
    #------
    serProportionInvalidValues    pandas.Series representing proportion of
    invalid values for each feature.
    
    Description
    #----------
    Define a list for each feature. For numerical and categorical use two
    values to describe an interval. First value is lower and second is upper
    bound of interval. For nominal data use a list of valid values. Respect
    the order of features for this list.
    """
    dfDesc = pd.DataFrame(columns = ["Name",
                                     "Proportion_Invalid_Values"])
    if isinstance(dfData, pd.Series):
        if dfData.name in dctValidValues:
            intVal = invalid_value_helper(dfData, dctValidValues)
            dfDesc = dfDesc.append({"Name": dfData.name,
                                "Proportion_Invalid_Values": intVal},
                                ignore_index=True)
    elif isinstance(dfData, pd.DataFrame):
        for j in dfData.columns:
            if j in dctValidValues:
                intVal = invalid_value_helper(dfData[j], dctValidValues)
                dfDesc = dfDesc.append({"Name": j,
                                "Proportion_Invalid_Values": intVal},
                                ignore_index=True)
    else:
        raise ValueError("No correct Dateformat given")
    # Normalize
    dfDesc["Proportion_Invalid_Values"] = 1 \
    - dfDesc["Proportion_Invalid_Values"] / len(dfData)
    return dfDesc

def outlier_helper(dfData, dctOutliers):
    """
    Parameters
    #---------
    dfData    pandas.DataFrame containing data
    
    dctOutliers    dictionary containing characteristic lists for each
    feature
    
    Returns
    #------
    intOutlier    Integer. Count of outliers based on input.
    
    Description
    #----------
    Creates boolean mask for both values lying above upper bound and values
    lying under lower bound. Adding both sums gives all outliers.
    """
    # List for non numerical or categorical data types
    lstNonNumCatDT = ["object", "datetime64[ns]", "bool", "timedelta[ns]",
                      "category"]
    
    if(dfData.dtypes.name not in lstNonNumCatDT):
        if dfData.name in dctOutliers:
            assert len(dctOutliers[dfData.name]) == 2
            assert isinstance(dctOutliers[dfData.name][0],(int, float))
            assert isinstance(dctOutliers[dfData.name][1],(int, float))
            intUpperOutlier = (
                    dfData>dctOutliers[dfData.name][1]
                    ).sum()
            intLowerOutlier = (
                    dfData<dctOutliers[dfData.name][0]
                    ).sum()
            intOutlier = intUpperOutlier + intLowerOutlier
    else:
        intOutlier = -1
    return intOutlier

def proportion_of_outliers(dfData, dctOutliers):
    """
    Parameters
    #---------
    dfData    pandas.DataFrame containing data
    
    Returns
    #------
    dfDesc    pandas.DataFrame with information about outliers for 
    each feature.
    
    Description
    #----------
    Define intervals only for numerical features. Use this style:
    [x,y] for x < y and x,y are real numbers.
    For nominal/categorical data try out another method called
    proportion_of_invalid_values. The defined intervals are given as lists of 
    two within another list. So the argument for the function is a nested list.
    Put the 2-lists in order of the features.
    """
    numberOfRows = len(dfData)
    dfDesc = pd.DataFrame(columns = ["Name",
                                     "Proportion_Outliers"])
    if isinstance(dfData, pd.Series):
        if dfData.name in dctOutliers:
            intVal = outlier_helper(dfData, dctOutliers)
            dfDesc = dfDesc.append({"Name": dfData.name,
                                "Proportion_Outliers": intVal},
                                ignore_index=True)
    elif isinstance(dfData, pd.DataFrame):
        for j in dfData.columns:
            if j in dctOutliers:
                intVal = outlier_helper(dfData[j], dctOutliers)
                dfDesc = dfDesc.append({"Name": j,
                                "Proportion_Outliers": intVal},
                                ignore_index=True)
    else:
        raise ValueError("No correct Dateformat given")
    if not dfDesc.empty:
        dfDesc["Proportion_Outliers"] = dfDesc["Proportion_Outliers"]/numberOfRows
    return dfDesc

def valid_outlier_helper(dfData, dctOutliers, dctValidValues):
    """
    Parameters
    #---------
    dfData    pandas.DataFrame containing data
    
    dctOutliers    Dictionary containing for numeric feature columns intervals,
    which define the normal interval of the values.
    
    dctValidValues    Dictionary containing for numeric feature columns 
    intervals, defining the valid range of values and for nominal data a list
    of valid values.
    
    Returns
    #------
    intOutlier    Integer
    
    Description
    #----------
    Creates boolean mask for both values lying above upper bound and values
    lying under lower bound. Both times the values getting checked, if they
    are valid values. Adding both sums gives all outliers.
    """
    # List for non numerical or categorical data types
    lstNonNumCatDT = ["object", "datetime64[ns]", "bool", "timedelta[ns]",
                      "category"]
    if(dfData.dtypes.name not in lstNonNumCatDT):
        if dfData.name in dctOutliers:
            intUpperOutlier = (
                    (dfData >  dctOutliers[dfData.name][1]) &
                    (dfData <= dctValidValues[dfData.name][1]) &
                    (dfData >= dctValidValues[dfData.name][0])
                    ).sum()
            intLowerOutlier = (
                    (dfData <  dctOutliers[dfData.name][0]) &
                    (dfData <= dctValidValues[dfData.name][1]) &
                    (dfData >= dctValidValues[dfData.name][0])
                    ).sum()
            intOutlier = intUpperOutlier + intLowerOutlier
    return intOutlier

def proportion_valid_outliers(dfData, dctOutliers, dctValidValues):
    """
    Parameters
    #---------
    dfData    pandas.DataFrame containing data
    
    dctOutliers    Dictionary containing for numeric feature columns intervals,
    which define the normal interval of the values.
    
    dctValidValues    Dictionary containing for numeric feature columns 
    intervals, defining the valid range of values and for nominal data a list
    of valid values.
    
    Returns
    #------
    dfDesc    pandas.DataFrame with information about outliers for 
    each feature.
    
    Description
    #----------
    Checking for Series, DataFrame or invalid data format.
    Processing data column-wise via helper method.
    Helper-method delivers information via DataFrame.
    Appending DataFrame of individual columns to one large DataFrame.
    """
    numberOfRows = len(dfData)
    dfDesc = pd.DataFrame(columns = ["Name",
                                     "Proportion_Valid_Outliers"])
    if isinstance(dfData, pd.Series):
        if (dfData.name in dctOutliers) and (dfData.name in dctValidValues):
            intVal = valid_outlier_helper(dfData, dctOutliers, dctValidValues)
            dfDesc = dfDesc.append({"Name": dfData.name,
                                "Proportion_Valid_Outliers": intVal},
                                ignore_index=True)
    elif isinstance(dfData, pd.DataFrame):
        for j in dfData.columns:
            if (j in dctOutliers and j in dctValidValues):
                intVal = valid_outlier_helper(dfData[j], dctOutliers, dctValidValues)
                dfDesc = dfDesc.append({"Name": j,
                                "Proportion_Valid_Outliers": intVal},
                                ignore_index=True)
    else:
        raise ValueError("No correct Dataformat given")
    dfDesc["Proportion_Valid_Outliers"] = dfDesc["Proportion_Valid_Outliers"]/numberOfRows
    return dfDesc

def number_of_unique_values(dfData):
    """
    Parameters
    #---------
    dfData    pandas.DataFrame containing data
    
    Returns
    #---------
    serUniqueValues    pandas.Series containing number of unique values for 
    each feature
    
    Description
    #----------
    Checking for Series, DataFrame or invalid data format.
    Processing data column-wise.
    Built-in function delivers information via Dictionary.
    Appending Dictionary of individual columns to one large Series.
    """
    dictFeatures = dict()
    if isinstance(dfData, pd.Series):
        intUnique = dfData.nunique()
        dictFeatures.update({dfData.name:intUnique}) 
    elif isinstance(dfData, pd.DataFrame):
        for j in dfData.columns:
            intUnique = dfData.loc[:,j].nunique()
            dictFeatures.update({j:intUnique}) 
    else:
        raise ValueError("No correct Dateformat given")
    serUniqueValues = pd.Series(dictFeatures)
    return serUniqueValues

def statistical_moments_of_features(dfData):
    """
    Parameters
    #---------
    dfData    pandas.DataFrame containing data
    
    Returns
    #---------
    pandas.DataFrame
    
    Description
    #----------
    Built-in statistical description from Pandas
    Only for numerical data
    For other data try out visualizations like histogram
    """
    return dfData.describe()

def create_a_correlation_matrix(dfData):
    """
    Parameters
    #---------
    dfData    pandas.DataFrame containing data
    
    Returns
    #------
    matCorrelation    pandas.DataFrame
    
    Description
    #----------
    Uses pandas builtin function for computing matCorrelation
    """
    matCorrelation = dfData.corr()
    return matCorrelation

def visualize_a_correlation_matrix_heatmap(dfData,
                                           tplFigSize = (10,5)):
    """
    Parameters
    #---------
    dfData    pandas.DataFrame containing data
    
    tplFigSize    tuple telling the size of the figure for the plot
    
    Description
    #----------
    Uses pandas builtin function for computing matCorrelation and heatmap
    """
    plt.figure(figsize = tplFigSize)
    matCorrelation = dfData.corr()
    sns.heatmap(matCorrelation, xticklabels = matCorrelation.columns,
                yticklabels = matCorrelation.columns)
    return

def visualize_a_correlation_matrix_scatter_plot_matrix(dfData,
                                                       tplFigSize = (10,5)):
    """
    Parameters
    #---------
    dfData    pandas.DataFrame containing data
    
    tplFigSize    tuple telling the size of the figure for the plot
    
    Description
    #---------
    Uses pandas builtin function for computing matCorrelation and scatter
    matrix
    """
    pd.plotting.scatter_matrix(dfData, figsize=tplFigSize)
    return

def cross_correlation(dfData, strColA, strColB, lag=0, method = "pearson"):
    """
    Parameters
    #---------
    dfData    pandas.DataFrame containing data
    
    strColA, strColB    String indicating name of column taken in to
        correlation
    
    lag    int default 0
    
    method    String "pearson", "kendall", "spearman"
    
    Returns
    #---------
    dfDesc    pandas.DataFrame containing information about names of columns,
    lag and the correlation coefficient in a table view
    
    Description
    #----------
    Uses pandas builtin function for computing Lag-N cross correlation for all
    lags from -N to N with N as any natural number representing the lag 
    parameter.
    """
    serA = dfData[strColA]
    serB = dfData[strColB]
    dfDesc = pd.DataFrame(columns = ["Name_1",
                                     "Name_2",
                                     "Correlation",
                                     "Timeshift"])
    if lag == 0:
        corrPosLag = serA.corr(serB, method)
        dfDesc = dfDesc.append({"Name_1": strColA,
                        "Name_2": strColB,
                        "Correlation": corrPosLag,
                        "Timeshift": 0},
                        ignore_index=True)
    for i in range(0,lag):
        if i != 0:
            corrPosLag = serA.corr(serB.shift(i), method)
            dfDesc = dfDesc.append({"Name_1": strColA,
                            "Name_2": strColB,
                            "Correlation": corrPosLag,
                            "Timeshift": i},
                            ignore_index=True)
        corrNegLag = serA.corr(serB.shift(-i), method)
        dfDesc = dfDesc.append({"Name_1": strColA,
                            "Name_2": strColB,
                            "Correlation": corrNegLag,
                            "Timeshift": -i},
                            ignore_index=True)
    return dfDesc

def granularity_of_timestamp_helper(dfData, timeConversion):
    """
    Parameters
    #---------
    dfData    pandas.DataFrame containing only one column with datetime
    
    timeConversion    String: 's' seconds, 'D' days, 'M' months, 'Y' years
    
    Returns
    #---------
    dctGT    Dictionary with statistical information about timedelta
    
    Description
    #----------
    Computes timedelta via shift of one column in datetime format
    """
    dfA = dfData.diff().dropna() / np.timedelta64(1, timeConversion)
    arrA = np.array(dfA)
    intMean = arrA.mean()
    intMin = arrA.min()
    intMax = arrA.max()
    if timeConversion == "Y":
        strTime = "Years"
    elif timeConversion == "M":
        strTime = "Months"
    elif timeConversion == "W":
        strTime = "Weeks"
    elif timeConversion == "D":
        strTime = "Days"
    elif timeConversion == "h":
        strTime = "Hours"
    elif timeConversion == "m":
        strTime = "Minutes"
    elif timeConversion == "s":
        strTime = "Seconds"
    else:
        strTime = "Undefined"    
    dctGT = {"Name": dfData.name,
             "Minimum": intMin,
             "Mean": intMean,
             "Maximum": intMax,
             "Timescale": strTime}
    return dctGT

def convert_time_column_and_granularity_of_timestamp(dfData,
                        lstCols,
                        timeConversion = "D",
                        timMin = pd.Timestamp('1970-01-01 00:00:00')):
    """
    Parameters
    #---------
    dfData    pandas.DataFrame containing data with one column specifying the
        timestamp
    
    lstCols    list of columns with information about time
    
    timeConversion    letter indicating time scale
                        "s" second
                        "D" day
                        "M" month
                        "Y" year
    
    timMin    pd.TimeStamp (optional) telling minimum valid date
    
    Returns
    #------
    DataFrame containing statistics about time gaps in time information columns
    
    Description
    #----------
    Three Transformations plus application of package own method 
    granularity_of_timestamp_feature(dfCol, timeConversion)
    """
    # True Copy to prevent mutable operations on data set
    dfTimeData = dfData.copy(deep = True)
    dfRes = pd.DataFrame()    
    for j in lstCols:
        # convert col j to datetime
        dfTimeData[j] = pd.to_datetime(dfTimeData[j])
        # sort ascending with respect to time in col j
        dfTimeData = dfTimeData.sort_values(by = j)
        # filter downwards by timMin
        dfTimeData = dfTimeData[dfTimeData[j] > timMin]
        # use only the column
        dfCol = dfTimeData[j]
        # compute time gaps
        dfRes_j = granularity_of_timestamp_feature(dfCol, timeConversion)
        dfRes = dfRes.append(dfRes_j, ignore_index=True)
    return dfRes

def granularity_of_timestamp_feature(dfData, lstTimeConversion):
    """
    Parameters
    #---------
    dfData    pandas.DataFrame containing data with one column specifying the
        timestamp
    
    lstTimeConversion    List containing information about time scale
        's' seconds, 'D' days, 'M' months, 'Y' years
    
    Returns
    #------
    dfStats    pandas.DataFrame containing statistical information about each 
    feature.
    
    Description
    #----------
    Checking for Series, DataFrame or invalid data format.
    Processing data column-wise.
    Helper function delivers information as DataFrame.
    Appending DataFrame of individual columns to one large DataFrame.
    """
    dfStats = pd.DataFrame(columns = ["Name",
                                      "Minimum",
                                      "Mean",
                                      "Maximum",
                                      "Timescale"])
    if isinstance(dfData, pd.Series):
        if(dfData.dtypes.name == 'datetime64[ns]'):
            for i in lstTimeConversion:
                dctGT = granularity_of_timestamp_helper(dfData, i)
                dfStats = dfStats.append(dctGT, ignore_index=True)
    elif isinstance(dfData, pd.DataFrame):
        for j in dfData.columns:
            if(dfData[j].dtypes.name == 'datetime64[ns]'):
                for i in lstTimeConversion:
                    dctGT = granularity_of_timestamp_helper(dfData[j], i)
                    dfStats = dfStats.append(dctGT, ignore_index=True)
    else:
        raise ValueError("No correct Dateformat given") 
    return dfStats

def rank_obj_data(serData):
    """
    Parameters
    #---------
    serData    pandas.Series containing one Column from data set
    
    Returns
    #------
    serFirstTwentyData    pandas.Series with first twenty highest counts
        of classes from column.
    
    Description
    #----------
    Groupby classes in column. Count number per class. Sort values descending.
    Take only first twenty. Helper method for plotting only most important
    classes of a feature. Helps keeping overview.
    """
    serCount = serData.groupby(by = serData).count()
    serSortData = serCount.sort_values(ascending = False)
    serFirstTwentyData = serSortData[:20]
    return serFirstTwentyData

def histogram_barplot(serData, bins, tplFigSize, intFontSize, strName,
                      boolSave):
    """
    Parameters
    #---------
    
    tplFigSize    tuple telling the size of the figure for the plot
    
    Description
    #----------
    Help function of distribution_of_feature_histogram
    """
    lstNonNumCatDT = ["object", "datetime64[ns]", "bool", "timedelta[ns]"]
    fig = plt.figure(figsize = tplFigSize)
    ax = plt.gca()
    ax.get_xaxis().get_major_formatter().set_useOffset(False)
    ax.get_yaxis().get_major_formatter().set_useOffset(False)
    plt.xlabel('Wertigkeiten von ' + serData.name)
    plt.ylabel('Häufigkeiten der Werte')
    plt.grid(True)
    plt.rcParams.update({'font.size': intFontSize})
    if serData.dtype.name in lstNonNumCatDT:
        serRankedData = rank_obj_data(serData)
        plt.title("Barplot_" + serRankedData.name)
        serRankedData.value_counts().plot(kind = 'bar')
        if boolSave == True:
            fig.savefig(strName + "_Barplot_" + serData.name + ".pdf")
    else:
        plt.title("Histogramm_" + serData.name)
        serData.hist(bins = bins)
        if boolSave == True:
            fig.savefig(strName + "_Histogram_" + serData.name + ".pdf") 
    return 

def distribution_of_feature_histogram(dfData,
                                      bins = 10,
                                      tplFigSize = (10,5),
                                      intFontSize = 22,
                                      strName = "Test",
                                      boolSave = False):
    """
    Parameters
    #---------
    dfData    Pandas.DataFrame containing data
    
    bins    Integer telling the number of bins to use for the histogram.
    
    tplFigSize    tuple telling the size of the figure for the plot.
    
    intFontSize    Integer for scaling size of font of text in the plot.
    
    strName    String giving the plot a name.
    
    boolSave    Boolean determin if the plots get saved or not.
    
    Description
    #----------
    Uses pandas builtin function for computing histogram
    """
    if isinstance(dfData, pd.Series):
        histogram_barplot(dfData, bins, tplFigSize, intFontSize, strName, 
                          boolSave)
    elif isinstance(dfData, pd.DataFrame):
        for j in dfData.columns:
            histogram_barplot(dfData[j], bins, tplFigSize, intFontSize,
                              strName, boolSave)
    else:
        raise ValueError("No correct Dateformat given")
    return


def box_plot(dfData, tplFigSize, intFontSize, strName, boolSave):
    """
    Parameters
    #---------
    
    tplFigSize    tuple telling the size of the figure for the plot.
    
    intFontSize    Integer for scaling size of font of text in the plot.
    
    strName    String giving the plot a name.
    
    boolSave    Boolean determin if the plots get saved or not.
    
    Description
    #----------
    Help function of distribution_of_feature_box_plot
    """
    lstNonNumCatDT = ["object", "datetime64[ns]", "bool", "timedelta[ns]",
                      "category"]
    if(dfData.dtypes.name not in lstNonNumCatDT):
        fig = plt.figure(figsize = tplFigSize)
        ax = plt.gca()
        ax.get_xaxis().get_major_formatter().set_useOffset(False)
        plt.title("Boxplot_" + dfData.name)
        #plt.xlabel('Keine Bedeutung')
        plt.ylabel('Wertigkeiten von ' + dfData.name)
        plt.grid(True)
        plt.rcParams.update({'font.size': intFontSize})
        plt.boxplot(dfData)
        if boolSave == True:
            fig.savefig(strName + "_Boxplot_" + dfData.name + ".pdf")
    return

def distribution_of_feature_box_plot(dfData,
                                     tplFigSize = (10,5),
                                     intFontSize = 22,
                                     strName = "Test",
                                     boolSave = False):
    """
    Parameters
    #---------
    dfData    Pandas.DataFrame containing data
    
    tplFigSize    tuple telling the size of the figure for the plot.
    
    intFontSize    Integer for scaling size of font of text in the plot.
    
    strName    String giving the plot a name.
    
    boolSave    Boolean determin if the plots get saved or not.
    
    Description
    #----------
    Uses pandas builtin function for computing boxplot
    """
    """
    
    for j in dfData.columns:
        
   
    lstTimeBoolDT = ["datetime64[ns]", "bool", "timedelta[ns]"]
    
        if(dfData.dtypes[j].name in lstTimeBoolDT):
            dfData.drop(labels = j, axis = 1)
    """
    if isinstance(dfData, pd.Series):
        box_plot(dfData, tplFigSize, intFontSize, strName, boolSave)
    elif isinstance(dfData, pd.DataFrame):
        for j in dfData.columns:
            box_plot(dfData[j], tplFigSize, intFontSize, strName, boolSave)
    else:
        raise ValueError("No correct Dateformat given")
    return

def density_plot(dfData, tplFigSize, intFontSize, strName, boolSave):
    """
    Parameters
    #---------
    
    tplFigSize    tuple telling the size of the figure for the plot.
    
    intFontSize    Integer for scaling size of font of text in the plot.
    
    strName    String giving the plot a name.
    
    boolSave    Boolean determin if the plots get saved or not.
    
    Description
    #----------
    Help function of distribution_of_feature_density_plot
    """
    lstNonNumCatDT = ["object", "datetime64[ns]", "bool", "timedelta[ns]",
                      "category"]
    if(dfData.dtypes.name not in lstNonNumCatDT):
        fig = plt.figure(figsize = tplFigSize)
        ax = plt.gca()
        ax.get_xaxis().get_major_formatter().set_useOffset(False)
        ax.get_yaxis().get_major_formatter().set_useOffset(False)
        plt.title("Density_Plot_" + dfData.name)
        plt.ylabel('Wertigkeiten von ' + dfData.name)
        plt.ylabel('Dichte der Wertigkeiten')
        plt.grid(True)
        plt.rcParams.update({'font.size': intFontSize})
        sns.distplot(dfData, hist=True, kde=True, color = 'darkblue', 
                     hist_kws={'edgecolor':'black'}, kde_kws={'linewidth': 4})
        if boolSave == True:
            fig.savefig(strName + "_Density_Plot_" + dfData.name + ".pdf")
    return

def distribution_of_feature_density_plot(dfData,
                                         tplFigSize = (10,5),
                                         intFontSize = 22,
                                         strName = "Test",
                                         boolSave = False):
    """
    Parameters
    #---------
    dfData    Pandas.DataFrame containing data
    
    tplFigSize    tuple telling the size of the figure for the plot.
    
    intFontSize    Integer for scaling size of font of text in the plot.
    
    strName    String giving the plot a name.
    
    boolSave    Boolean determin if the plots get saved or not.
    
    Description
    #----------
    Uses pandas builtin function for computing
    """
    if isinstance(dfData, pd.Series):
        density_plot(dfData, tplFigSize, intFontSize, strName, boolSave)
    elif isinstance(dfData, pd.DataFrame):
        for j in dfData.columns:
            density_plot(dfData[j], tplFigSize, intFontSize, strName, boolSave)
    else:
        raise ValueError("No correct Dateformat given")
    return

#-------------#
# Projections #
#-------------#
    

def pca(dfData, n_components = 2, whiten = False, boolPlot = False, 
        boolVerbose = False):
    """
    Parameters
    #---------
    dfData    Pandas.DataFrame containing data
    
    n_components    Integer: number of components for which information is 
        outputted.
    
    Returns
    #------
    arrVarianceRatio    numpy.Array
    
    arrSingularValues    numpy.Array
    
    matCovariance    numpy.ndarray
    
    Description
    #----------
    Uses sklearn builtin function for computing.
    Maximize the variance and output those
    """
    dfNum = get_numericals(dfData)
    dfNum = dfNum.dropna(axis = 1)
    min_max_scaler = MinMaxScaler()
    dfNum = min_max_scaler.fit_transform(dfNum)
    #PCA
    pca = skd.PCA(n_components, whiten)
    pca.fit(dfNum)
    dfData_pca = pca.transform(dfNum)
    arrVarianceRatio = pca.explained_variance_ratio_
    arrSingularValues = pca.singular_values_
    matCovariance = pca.get_covariance()
    #res = pca.fit_transform(intNumRows, intNumCols)
    if boolPlot == True:
        if n_components == 2:
            plt.scatter(dfData_pca[:, 0], dfData_pca[:, 1], alpha=0.8)
        else:
            print("Plotting is only implemented for 2 components")
    if boolVerbose == True:
        print("original shape:   ", dfNum.shape)
        print("transformed shape:", dfData_pca.shape)
        print("Explained variance ratio:", arrVarianceRatio)
        print("Singular values:", arrSingularValues)
        #print(pca.get_precision)
        print(matCovariance)
        #print(pca.get_params())
    return arrVarianceRatio, arrSingularValues, matCovariance

def ica(dfData, n_components = 2, boolPlot = False):
    """
    Parameters
    #---------
    dfData    Pandas.DataFrame containing data
    
    n_components    Integer: number of components for which information is 
        outputted.
    
    Description
    #----------
    Uses sklearn builtin function for computing.
    Maximizes independency between n_components
    """
    dfNum = get_numericals(dfData)
    dfNum = dfNum.dropna(axis = 1)
    min_max_scaler = MinMaxScaler()
    dfNum = min_max_scaler.fit_transform(dfNum)
    ica = skd.FastICA(n_components)
    ica.fit(dfNum)
    S_ = ica.fit_transform(dfNum)
    A_ = ica.mixing_
    
    if boolPlot == True:
        if n_components == 2:
            plt.scatter(S_[:, 0], S_[:, 1], alpha=0.8)
        else:
            print("Plotting is only implemented for 2 components")
    
    print(S_.shape)
    print(A_)
    return S_, A_

#------------#
# Clustering #
#------------#

def proj_kMeans(dfData, n_clusters = 2, boolPlot = False, method='pca'):
    """
    Parameters
    #---------
    
    dfData    pandas.DataFrame
    
    n_clusters    Integer
    
    Description
    #----------
    
    """
    dfNum = get_numericals(dfData)
    dfNum = dfNum.dropna(axis = 1)
    if method == 'pca':
        pca = skd.PCA(2, "whiten")
        dfData_pca = pca.fit_transform(dfNum)
    if method == 'ica':
        ica = skd.FastICA(2)
        ica.fit(dfNum)
        dfData_pca = ica.fit_transform(dfNum)
    min_max_scaler = MinMaxScaler()
    dfData_pca = min_max_scaler.fit_transform(dfData_pca)
    kmeans = KMeans(n_clusters)
    kmeans.fit(dfData_pca)
    y_kmeans = kmeans.predict(dfData_pca)
    if boolPlot == True:
        centers = kmeans.cluster_centers_
        plt.scatter(dfData_pca[:, 0], dfData_pca[:, 1],
                    c=y_kmeans, s=50, cmap='viridis')
        plt.scatter(centers[:, 0], centers[:, 1],
                    c='black', s=200, alpha=0.5)
    labels = kmeans.labels_
    intScore = metrics.silhouette_score(dfData_pca, labels, metric='euclidean')
    return intScore, labels

def kMeans(dfData, n_clusters = 2):
    """
    Parameters
    #---------
    
    dfData    pandas.DataFrame
    
    n_clusters    Integer
    
    Description
    #----------
    
    """
    dfNum = get_numericals(dfData)
    dfNum = dfNum.dropna(axis = 1)
    min_max_scaler = MinMaxScaler()
    dfNum = min_max_scaler.fit_transform(dfNum)
    kmeans = KMeans(n_clusters)
    kmeans.fit(dfNum)
    labels = kmeans.labels_
    intScore = metrics.silhouette_score(dfNum, labels, metric='euclidean')
    return intScore, labels

def proj_spectral_clustering(dfData, n_clusters = 2, method='pca'):
    """
    Parameters
    #---------
    
    dfData    pandas.DataFrame
    
    n_clusters    Integer
    
    Description
    #----------
    
    """
    dfNum = get_numericals(dfData)
    dfNum = dfNum.dropna(axis = 1)
    if method == 'pca':
        pca = skd.PCA(2, "whiten")
        dfNum = pca.fit_transform(dfNum)
    if method == 'ica':
        ica = skd.FastICA(2)
        ica.fit(dfNum)
        dfNum = ica.fit_transform(dfNum)
    min_max_scaler = MinMaxScaler()
    dfNum = min_max_scaler.fit_transform(dfNum)
    model = SpectralClustering(n_clusters = n_clusters,
                               affinity='nearest_neighbors',
                               assign_labels='kmeans')
    labels = model.fit_predict(dfNum)
    plt.scatter(dfNum[:, 0], dfNum[:, 1],
                c=labels, s=50, cmap='viridis')
    intScore = metrics.silhouette_score(dfNum, labels, metric='euclidean')
    return intScore, labels
    
def spectral_clustering(dfData, n_clusters = 2):
    """
    Parameters
    #---------
    
    dfData    pandas.DataFrame
    
    n_clusters    Integer
    
    Description
    #----------
    
    """
    dfNum = get_numericals(dfData)
    dfNum = dfNum.dropna(axis = 1)
    min_max_scaler = MinMaxScaler()
    dfNum = min_max_scaler.fit_transform(dfNum)
    model = SpectralClustering(n_clusters = n_clusters,
                               affinity='nearest_neighbors',
                               assign_labels='kmeans')
    labels = model.fit_predict(dfNum)
    intScore = metrics.silhouette_score(dfNum, labels, metric='euclidean')
    return intScore, labels
from backtesting import Backtest, Strategy

import pandas as pd
import numpy as np
import json

#for testing
#from backtesting.test import GOOG
import pdb

np.random.seed(42)

data_file = "data.txt"
min_fvg_height = .07
min_risk_reward_ratio = 1


def get_data(file_path):
    try:
        with open(file_path, "r") as file:
            data = json.load(file)  # Load JSON data from the file
            return data
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


def munge_polygon_api_data(data_file):
    data = get_data(data_file)
    data = pd.DataFrame(data['results'])
    data = data.drop(['v','vw','n'], axis=1)
    new_column_names = ['Open', 'Close', 'High', 'Low', 'Time']
    data.columns = new_column_names
    data.Time = pd.to_datetime(data.Time, unit='ms')
    data = data.set_index('Time')
    return data

class FVGStrategy(Strategy):
    def init(self):
        self.swing_highs = self.I(get_swing_highs_arr, self.data, color="blue")
        self.swing_lows = self.I(get_swing_lows_arr, self.data, color="green")
        self.fvg_arrays = self.I(get_last_fvg_arrays, self.data, overlay=True, color='purple') #returns 2 sets of 1n arrays: fvg top and fvg bottom
        
    def next(self):
        last_fvg_top = self.fvg_arrays[0][-1]
        last_fvg_bottom = self.fvg_arrays[1][-1]

        if(last_fvg_top
           and last_fvg_bottom 
           and self.data.Low[-1] < last_fvg_top
           and self.data.Low[-1] >= last_fvg_bottom):
           try:
              reward = self.swing_highs[-1] - last_fvg_top
              risk = last_fvg_top - self.swing_lows[-1]
              if reward > (risk * min_risk_reward_ratio):
                 self.buy(sl=self.swing_lows[-1] , tp=self.swing_highs[-1], limit=last_fvg_top) #in a try/catch because in many cases swing low is greater than price backtesting.py is trying to buy at)
           except:
               pass

def get_swing_highs_arr(data):
    length_data = data.High.shape[0]
    last_swing_high = data.High[0]
    swing_high_arr = [last_swing_high]
    for i in range(1, length_data - 1 ):
        if( (data.High[i-1] <  data.High[i]) and
            ( data.High[i+1] < data.High[i] )
           ):
            last_swing_high = data.High[i]
        swing_high_arr.append(last_swing_high)
    swing_high_arr.append(last_swing_high)

    return swing_high_arr

def get_swing_lows_arr(data):
   length_data = data.Low.shape[0]
   last_swing_low = data.Low[0]
   swing_low_arr = [last_swing_low]
   for i in range(1, length_data - 1 ):
      if( (data.Low[i-1] >  data.Low[i]) and
            ( data.Low[i+1] > data.Low[i] )
         ):
         last_swing_low = data.Low[i]
      swing_low_arr.append(last_swing_low)
   swing_low_arr.append(last_swing_low)

   return swing_low_arr

    
def get_last_fvg_arrays(data):
    row_number_candlestick_1 = 0
    fvg_top = None
    fvg_bottom = None
    fvg_arr_top = [None, None, None]
    fvg_arr_bottom = [None, None, None]

    rows = data.Open.shape[0]

    while row_number_candlestick_1 < (rows-3):
        row_number_candlestick_2 = row_number_candlestick_1 + 1
        row_number_candlestick_3 = row_number_candlestick_1 + 2

        fvg_bottom_check = data.High[row_number_candlestick_1]
        fvg_top_check = data.Low[row_number_candlestick_3]
        second_candle_is_green = data.Open[row_number_candlestick_2] < data.Close[row_number_candlestick_2]

        if( fvg_bottom_check < (fvg_top_check + min_fvg_height) 
            and second_candle_is_green):
            fvg_top = fvg_top_check
            fvg_bottom = fvg_bottom_check
        elif(fvg_top and fvg_top_check < fvg_top):
          fvg_top = None
          fvg_bottom = None
        fvg_arr_top.append(fvg_top)
        fvg_arr_bottom.append(fvg_bottom)
          
        row_number_candlestick_1 = row_number_candlestick_2

    fvg_arr_bottom = munge_bottom_array(fvg_arr_bottom)

    return fvg_arr_top, fvg_arr_bottom

def munge_bottom_array(fvg_arr_bottom):
    munged_array = []
    for item in fvg_arr_bottom:
        if item is None:
            munged_array.append(None)
        else:
            if(munged_array[-1]):
                munged_array.append(munged_array[-1])
            else:
                munged_array.append(item)
    return munged_array

def get_last_not_none_element(arr):
    for item in reversed(arr):
        if item is not None:
            return item
    return None  # Return None if no non-None element is found


def get_last_fvg_top_array(data):
   arr = get_last_fvg_arrays(data)
   return arr[0]

def get_last_fvg_bottom_array(data):
   arr = get_last_fvg_arrays(data)
   return arr[1]

#price_data = GOOG.truncate(before=pd.Timestamp("2010-01-28"), after=pd.Timestamp("2011-05-05"))
data = munge_polygon_api_data(data_file)
bt = Backtest(data, FVGStrategy , cash=10_000)
results = bt.run()
print(results)
bt.plot()

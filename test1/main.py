import datetime
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader.data as web

class try_day:
 def __init__(self, codes=[], in_date="2014-01-01", time=time.strftime('%Y-%m-%d', time.localtime(time.time())),time_span_inc=13, time_span_avg=13, funds=100000, path="D:/"):
  self.codes = codes # 所需要获取的股票
  self.in_date = in_date # 数据处理开始日期
  self.time = time # 数据处理结束日期
  self.time_span_inc = time_span_inc # 涨幅跨度
  self.time_span_avg = time_span_avg # 平均值跨度
  self.funds = funds # 现有资金
  self.path = path # 获取股票数据保存的地址
  self.df = None
  self.the_code = {"code": None, "price": None}
  self.change = {"funds": [], "date": []}

  # 获取相关数据
  def get_all_data(self):
      end = datetime.date.today()

  for code in self.codes:
      stock = web.DataReader(code, "yahoo", self.in_date)
      stock.rename(columns={"Close": code}, inplace=True)
      stock[code].to_csv(self.path + code + ".csv")  # 保存到本地

  # 获取Excel中数据 ，并存到data列表中
  def get_data(self):
      self.df = pd.read_csv(self.path + self.codes[0] + ".csv")

  for code in self.codes[1:]:
      df = pd.read_csv(self.path + code + ".csv")
  self.df = pd.merge(self.df, df, left_on="Date", right_on="Date", how="outer")
  self.df.set_index('Date', inplace=True)

  # 获取那n天的数据,格式是numpy
  def get_n_day(self, in_data):
       try:
          position_index = self.df.index.get_loc(in_data)
       except position_index >= max(self.time_span_avg, self.time_span_inc):
          code_list = []
       for code in range(len(self.codes)):
        i_list = []
       for i in range(max(self.time_span_avg, self.time_span_inc)):
          i_list.append(self.df.iloc[position_index - i - 1, code])
          code_list.append(i_list)
          return np.array(code_list)
       else:return np.array([0])
       except Exception as e:
       return np.array([0])

# 计算涨幅
  def get_increase(self, result):
      inc = []
      for code in range(len(self.codes)):
          increase = (result[code][0] / result[code][self.time_span_inc - 1]) - 1
          inc.append(increase)
          return inc, inc.index(max(inc))
# 计算平均价格
  def get_avg(self, result):
      avg_result = result[:, :self.time_span_avg].mean(axis=1)
      return avg_result
# 判断实行买卖
  def buy_sell(self, increase, avg, result):
      new_price = result[increase[1]]
      avg_price = avg[increase[1]]
      if self.the_code["code"] is None:
          if new_price > avg_price:
              self.buy(self.codes[increase[1]], new_price)
          elif (self.the_code["code"] != self.codes[increase[1]]) | (new_price avg_price) & (increase[0][increase[1]] > 0):
              self.buy(self.codes[increase[1]], new_price)
      else:
          print(self.in_date + "继续持有 ：", self.the_code["code"])

  def sell(self, result):
      print("卖" + "*" * 30)
      print("在" + self.in_date + "卖出")
      print("全部卖出 ：", self.the_code["code"])
      sell_price = result[self.codes.index(str(self.the_code["code"]))]
      print("卖出价格", sell_price)
      self.funds = self.funds * (sell_price / self.the_code["price"])
      self.change["funds"].append(self.funds)
      self.change["date"].append(self.in_date)
      self.the_code["code"] = None
      self.the_code["price"] = None
      print("资金持有变为 ：", self.funds)
      print("*" * 30)
  def buy(self, code, new_price):
      self.the_code["code"] = code
      self.the_code["price"] = new_price
      self.change["funds"].append(self.funds)
      self.change["date"].append(self.in_date)
      print("在" + self.in_date + "买入")
      print("将资金全部买入", self.the_code["code"])
      print("买入价格 ：", self.the_code["price"])
      print("资金持有变为 ：", self.funds)
      print("*" * 30)
# 画图
  def draw(self):
      x = self.change["date"]
      y = self.change["funds"]
      plt.figure(figsize=(12, 8), dpi=80)
      plt.plot(x, y, color="red", linewidth=2, alpha=0.6)
      plt.xticks(list(x)[::20], x[::20], rotation=45) # rotation 为旋转角度
      plt.show()
# 主函数
  def the_main(self):
      self.get_data()
      while self.in_date != self.time:
       np_result = self.get_n_day(self.in_date)
      if np_result.any():
         increase = self.get_increase(np_result)
      if increase != 0:
         avg = self.get_avg(np_result)
         self.buy_sell(increase, avg, np_result[:, 0])

# 进入下一天
         self.get_next_day()
         print("现在持有", self.funds)
         print(max(self.change["funds"]))
         self.draw()
# 输入某天获取到第二天的str
  def get_next_day(self, tim=1):
      timeArray = time.strptime(self.in_date, "%Y-%m-%d")
      timeStamp = int(time.mktime(timeArray))
      timeStamp = timeStamp + 84600 * tim
      timeArray = time.localtime(timeStamp)
      self.in_date = time.strftime("%Y-%m-%d", timeArray)

     if __name__ == '__main__':
       codes = ['159915.SZ', '510300.SS', '510500.SS']
       p = try_day(path="D ：/", codes=codes, time='2019- 12-31')
# p.get_all_data()
       p.the_main()

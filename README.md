# Stock Trader

Hallym Univ. Reinforcement Project

- korea stock market : KOSPI200
- reinforcement learning

## Day Bot

그날에 투자할 회사를 선택해주는 Bot

# Data

- KRX 한국 거래소에서 수집

### Download

```shell script
python main.py --download
```

### File Structure

```
data | KOSPI200 | company 1
     |          | company 2
     |          | ...
     |
     | KOSPI200_list
     | KRX_list
```

# Env

### Reward
```
# lib/env/market.py

보상(대비율) : $\frac{Change_{t}}{Close_{t-1}}$
                    |
                  표준화
```

- 수정 요망

### Render

- 실시간 Confusion Matrix 준비중


# Model

- Policy Gradient

### Input Data


- Input Shape : (num company, window size, num feature)

- Num company : 200 -> 200개의 회사 데이터
- Window size : 10  -> 10일씩 본다. 즉, 2주
- Num feature : CO, HO, LO, OO, 거래율, 대비율
    + CO : $\frac{Close_{t-1}}{Open_{t-1}}$
    + HO : $\frac{High_{t-1}}{Open_{t-1}}$
    + LO : $\frac{Low_{t-1}}{Open_{t-1}}$
    + OO : $\frac{Open_{t}}{Open_{t-1}}$
    + 거래율 : $\frac{Volume_{t}}{Total_Share}$
    + 대비율 : $\frac{Change_{t}}{Close_{t-1}}$
    

### Structure

```python
# lib/agent/PG.py

Cmodel = tf.keras.Sequential()
            model.add(Conv2D(128, kernel_size=(1, 3), strides=1, activation="relu", input_shape=input_shape))
            model.add(MaxPool2D(pool_size=(1, 2)))
            model.add(Conv2D(64, kernel_size=(1, 4), strides=1, activation="relu"))
            model.add(Conv2D(1, kernel_size=1, activation="sigmoid"))
            model.add(Flatten())

Optimizer = Adam

Loss = Binary CrossEntropy
```

## Reference 
- [http://www.krx.co.kr/main/main.jsp](http://www.krx.co.kr/main/main.jsp)
- [https://github.com/gyusu/Policy_Gradient_ETF_Portfolio_Manager](https://github.com/gyusu/Policy_Gradient_ETF_Portfolio_Manager)
- [https://github.com/selimamrouni/Deep-Portfolio-Management-Reinforcement](https://github.com/selimamrouni/Deep-Portfolio-Management-Reinforcement)
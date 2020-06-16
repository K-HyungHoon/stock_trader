# ⏰ Stock Trader 

Hallym Univ. Reinforcement Project

- korea stock market : KOSPI200
- reinforcement learning

---

## 🌈 Data

- KRX 한국 거래소에서 수집

#### Download

```shell script
python download --start_date [DATE] --end_date [DATE]
```

---

## 📳 Day Bot 

KOSPI200에서 투자할 회사를 선택해주는 Bot

#### Train

```shell script
python train.py
```

#### Test

```shell script
python test.py --load_path [./checkpoint/YOUR_MODEL]
```

---

## 🍩 Env

#### Reward

- 한 회사의 확률 값

```
reward = change(CC) * action(one-hot encoding vector)
```

#### State

```math
- Input Shape : (num company, window size, num feature)

- Num company : 200 -> 200개의 회사 데이터
- Window size : 10  -> 10일씩 본다. 즉, 2주
- Num feature : CO, HO, LO, OO, CC, HC, LC, OC, 거래율, 대비율
    + CO : Close(T-1) / Open(T-1)
    + HO : High(T-1) / Open(T-1)
    + LO : Low(T-1) / Open(T-1)
    + OO : Open(T) / Open(T-1)
    + CC : (Close(T)-Close(T-1)) / Close(T-1)
    + HC : (High(T)-Close(T)) / Close(T)
    + LC : (Low(T)-Close(T)) / Close(T)
    + OC : (Open(T)-Close(T-1)) / Close(T-1)
    + 거래율 : Volume(T) / Total Share
    + 대비율 : Change(T) / Close(T-1)
```

---

## 🤖 Agent

#### Model

```python
# lib/agent/agents.py

model = tf.keras.Sequential()
            model.add(Conv2D(128, kernel_size=(1, 3), strides=1, activation="relu", input_shape=input_shape))
            model.add(MaxPool2D(pool_size=(1, 2)))
            model.add(Conv2D(64, kernel_size=(1, 4), strides=1, activation="relu"))
            model.add(Conv2D(1, kernel_size=1, activation="sigmoid"))
            model.add(Flatten())

Optimizer = Adam
```

## Reference 
- [http://www.krx.co.kr/main/main.jsp](http://www.krx.co.kr/main/main.jsp)
- [https://github.com/gyusu/Policy_Gradient_ETF_Portfolio_Manager](https://github.com/gyusu/Policy_Gradient_ETF_Portfolio_Manager)
- [https://github.com/selimamrouni/Deep-Portfolio-Management-Reinforcement](https://github.com/selimamrouni/Deep-Portfolio-Management-Reinforcement)

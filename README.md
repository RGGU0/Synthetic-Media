# Synthetic-Media
## Графики обучения
Далее представлены метрики accuracy и loss для нескольких проведенных экспериментов. Эксперименты отличаются размерами batch и процентом dropout


## Графики обучения при batch равном 28
![auc28](https://github.com/RGGU0/Synthetic-Media/assets/89143056/05a194b3-7e9f-4a19-bb48-c70692915af7)
Рисунок 1 - accuracy при batch равном 28
![loss28](https://github.com/RGGU0/Synthetic-Media/assets/89143056/7bb8f51c-b912-4ef0-9c54-a7374420cc34)
Рисунок 2 - loss при batch равном 28

## Графики обучения при batch равном 32.
![auc32](https://github.com/RGGU0/Synthetic-Media/assets/89143056/86d3b57a-a094-4b7b-a131-edbec2917a0b)
Рисунок 3 - accuracy при batch равном 32
![loss32](https://github.com/RGGU0/Synthetic-Media/assets/89143056/1836e4dd-9bba-40c3-9b1f-fe95995abf6e)
Рисунок 4 - loss при batch равном 32

## Графики обучения при dropout равном 10.
![auc_d10](https://github.com/RGGU0/Synthetic-Media/assets/89143056/b57f1322-85d6-479e-9f71-8bd51406c035)
Рисунок 5 - accuracy при dropout равном 10
![loss_d10](https://github.com/RGGU0/Synthetic-Media/assets/89143056/e3f546f1-69d2-4611-ad2c-00f5bf5f5e84)
Рисунок 6 - loss при dropout равном 10

## Графики обучения при dropout равном 15.
![auc_d15](https://github.com/RGGU0/Synthetic-Media/assets/89143056/45a11ab3-2871-4d26-8d48-d0312edbaec1)
Рисунок 7 - accuracy при dropout равном 15
![loss_d15](https://github.com/RGGU0/Synthetic-Media/assets/89143056/2d0a16ae-774c-45ba-b944-a2cf49fc6ba4)
Рисунок 8 - loss при dropout равном 15

## Вывод
Наилучшее accuracy равное 72% было при batch равном 28 и отсутствии dropout. Основываясь на приведенных графиках, можно сделать вывод о том, что модель начинает переучаться уже на начальных эпохах. Предположительно, причиной такого результата является недостаточный объем обучающих данных.

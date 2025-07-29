def interpret_result(y_test, y_pred):
    if y_pred[-1] > y_test[-1]:
        return "📈 The model predicts an **increase** in the exchange rate."
    elif y_pred[-1] < y_test[-1]:
        return "📉 The model predicts a **decrease** in the exchange rate."
    else:
        return "⏸️ The model predicts the exchange rate will **remain stable**."
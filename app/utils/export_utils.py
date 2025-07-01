import pandas as pd
from io import BytesIO
from datetime import datetime

import matplotlib.pyplot as plt
from io import BytesIO
import base64

def export_to_csv(transactions):
    df = pd.DataFrame([{
        'Дата': t.created_at,
        'Тип': 'Доход' if t.amount > 0 else 'Расход',
        'Категория': t.category.name,
        'Сумма (₽)': abs(t.amount),
        'Описание': t.description or ''
    } for t in transactions])
    
    output = BytesIO()
    df.to_csv(output, index=False, encoding='utf-8-sig')
    output.seek(0)
    return output

def export_to_excel(transactions):
    df = pd.DataFrame([{
        'Дата': t.created_at,
        'Тип': 'Доход' if t.amount > 0 else 'Расход',
        'Категория': t.category.name,
        'Сумма (₽)': abs(t.amount),
        'Описание': t.description or ''
    } for t in transactions])
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Транзакции')
        
        # Добавляем автофильтр
        worksheet = writer.sheets['Транзакции']
        worksheet.autofilter(0, 0, len(transactions), 4)
        
        # Настраиваем ширину колонок
        for i, col in enumerate(df.columns):
            width = max(len(col), df[col].astype(str).str.len().max())
            worksheet.set_column(i, i, width + 2)
    
    output.seek(0)
    return output


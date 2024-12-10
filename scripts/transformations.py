import pandas as pd

def convert_date_columns(df, date_columns):
    """Converte colunas de data para o formato correto."""
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce').dt.date
            df[col] = df[col].where(df[col].notnull(), None)

def transform_datasets(data_files):
    """Aplica as transformações necessárias para cada dataset."""
    # Dimensões e transformações de tabelas
    customer_df = pd.read_csv(data_files.get('olist_customers_dataset.csv', '')).rename(columns={
        'customer_id': 'customer_id',
        'customer_unique_id': 'customer_unique_id',
        'customer_zip_code_prefix': 'customer_zip_code',
        'customer_city': 'customer_city',
        'customer_state': 'customer_state'
    })[['customer_id', 'customer_unique_id', 'customer_zip_code', 'customer_city', 'customer_state']]

    orders_df = pd.read_csv(data_files.get('olist_orders_dataset.csv', '')).rename(columns={
        'order_id': 'order_id',
        'customer_id': 'customer_id',
        'order_purchase_timestamp': 'order_purchase_date',
        'order_approved_at': 'order_approved_date',
        'order_delivered_carrier_date': 'order_delivered_carrier_date',
        'order_delivered_customer_date': 'order_delivered_customer_date',
        'order_estimated_delivery_date': 'order_estimated_delivery_date'
    })[['order_id', 'customer_id', 'order_purchase_date', 'order_approved_date',
         'order_delivered_carrier_date', 'order_delivered_customer_date', 'order_estimated_delivery_date']]
    convert_date_columns(orders_df, [
        'order_purchase_date', 'order_approved_date', 'order_delivered_carrier_date',
        'order_delivered_customer_date', 'order_estimated_delivery_date'
    ])

    reviews_df = pd.read_csv(data_files.get('olist_order_reviews_dataset.csv', '')).rename(columns={
        'review_id': 'review_id',
        'order_id': 'order_id',
        'review_score': 'review_score'
    })[['review_id', 'order_id', 'review_score']]

    sellers_df = pd.read_csv(data_files.get('olist_sellers_dataset.csv', '')).rename(columns={
        'seller_id': 'seller_id',
        'seller_zip_code_prefix': 'seller_zip_code',
        'seller_city': 'seller_city',
        'seller_state': 'seller_state'
    })[['seller_id', 'seller_zip_code', 'seller_city', 'seller_state']]

    order_items_df = pd.read_csv(data_files.get('olist_order_items_dataset.csv', '')).rename(columns={
        'order_id': 'order_id',
        'product_id': 'product_id',
        'seller_id': 'seller_id',
        'shipping_limit_date': 'shipping_limit_date',
        'price': 'price',
        'freight_value': 'freight_value'
    })[['order_id', 'product_id', 'seller_id', 'shipping_limit_date', 'price', 'freight_value']]
    convert_date_columns(order_items_df, ['shipping_limit_date'])

    products_df = pd.read_csv(data_files.get('olist_products_dataset.csv', '')).rename(columns={
        'product_id': 'product_id',
        'product_category_name': 'product_category_name'
    })[['product_id', 'product_category_name']]
    products_df['product_category_name'] = products_df['product_category_name'].fillna('unknown')

    payments_df = pd.read_csv(data_files.get('olist_order_payments_dataset.csv', '')).rename(columns={
        'order_id': 'order_id',
        'payment_sequential': 'payment_sequential',
        'payment_type': 'payment_type',
        'payment_installments': 'payment_installments',
        'payment_value': 'payment_value'
    })[['order_id', 'payment_sequential', 'payment_type', 'payment_installments', 'payment_value']]

    f_sale_df = pd.merge(order_items_df, orders_df[['order_id', 'customer_id']], on='order_id', how='inner')
    f_sale_df = pd.merge(f_sale_df, reviews_df[['order_id', 'review_id']], on='order_id', how='inner')
    f_sale_df = f_sale_df[['order_id', 'product_id', 'seller_id', 'customer_id', 'review_id']]

    return {
        'dim_customer': customer_df,
        'dim_order': orders_df,
        'dim_reviews': reviews_df,
        'dim_seller': sellers_df,
        'dim_item': order_items_df,
        'dim_product': products_df,
        'dim_payment': payments_df,
        'f_sale': f_sale_df,
    }
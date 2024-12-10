-- dim_customer
CREATE TABLE dim_customer (
    customer_id VARCHAR PRIMARY KEY,
    customer_unique_id VARCHAR NOT NULL,
    customer_zip_code INT NOT NULL,
    customer_city VARCHAR NOT NULL,
    customer_state VARCHAR NOT NULL
);

-- dim_product
CREATE TABLE dim_product (
    product_id VARCHAR PRIMARY KEY,
    product_category_name VARCHAR NOT NULL
);

-- dim_seller
CREATE TABLE dim_seller (
    seller_id VARCHAR PRIMARY KEY,
    seller_zip_code INT NOT NULL,
    seller_city VARCHAR NOT NULL,
    seller_state VARCHAR NOT NULL
);

-- dim_order
CREATE TABLE dim_order (
    order_id VARCHAR PRIMARY KEY,
    customer_id VARCHAR NOT NULL,
    order_purchase_date DATE NOT NULL,
    order_approved_date DATE,
    order_delivered_carrier_date DATE,
    order_delivered_customer_date DATE,
    order_estimated_delivery_date DATE,
    FOREIGN KEY (customer_id) REFERENCES dim_customer (customer_id)
);

-- dim_reviews
CREATE TABLE dim_reviews (
    review_id VARCHAR PRIMARY KEY,
    order_id VARCHAR NOT NULL,
    review_score INT CHECK (review_score BETWEEN 1 AND 5),
    FOREIGN KEY (order_id) REFERENCES dim_order (order_id)
);

-- dim_payment
CREATE TABLE dim_payment (
    order_id VARCHAR NOT NULL,
    payment_sequential INT NOT NULL,
    payment_type VARCHAR NOT NULL,
    payment_installments INT NOT NULL,
    payment_value NUMERIC(10, 2) NOT NULL,
    PRIMARY KEY (order_id, payment_sequential),
    FOREIGN KEY (order_id) REFERENCES dim_order (order_id)
);

-- dim_item
CREATE TABLE dim_item (
    order_id VARCHAR NOT NULL,
    product_id VARCHAR NOT NULL,
    seller_id VARCHAR NOT NULL,
    shipping_limit_date DATE NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    freight_value NUMERIC(10, 2) NOT NULL,
    PRIMARY KEY (order_id, product_id, seller_id),
    FOREIGN KEY (order_id) REFERENCES dim_order (order_id),
    FOREIGN KEY (product_id) REFERENCES dim_product (product_id),
    FOREIGN KEY (seller_id) REFERENCES dim_seller (seller_id)
);

-- f_sale
CREATE TABLE f_sale (
    sale_id SERIAL PRIMARY KEY,
    seller_id VARCHAR NOT NULL,
    product_id VARCHAR NOT NULL,
    customer_id VARCHAR NOT NULL,
    review_id VARCHAR NOT NULL,
    order_id VARCHAR NOT NULL,
    category_price NUMERIC(10, 2),
    category_rating NUMERIC(3, 2),
    delivery_time INTERVAL,
    FOREIGN KEY (seller_id) REFERENCES dim_seller (seller_id),
    FOREIGN KEY (product_id) REFERENCES dim_product (product_id),
    FOREIGN KEY (customer_id) REFERENCES dim_customer (customer_id),
    FOREIGN KEY (review_id) REFERENCES dim_reviews (review_id),
    FOREIGN KEY (order_id) REFERENCES dim_order (order_id)
);
